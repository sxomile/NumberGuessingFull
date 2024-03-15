import * as algokit from '@algorandfoundation/algokit-utils'
import { Algodv2, Indexer, SignedTransaction, Transaction, TransactionWithSigner } from 'algosdk';
import { PogadjanjeClient } from '../contracts/Pogadjanje'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from './network/getAlgoClientConfigs'
import { AppDetails } from '@algorandfoundation/algokit-utils/types/app-client';
import algosdk from 'algosdk';
import { useWallet } from '@txnlab/use-wallet';
import { TransactionToSign } from '@algorandfoundation/algokit-utils/types/transaction';

export interface PogadjanjeGameState {
  skriveniBroj: number,
  rezultat: number,
  brojac: number
}

class AlgorandService {
  public algodClient: Algodv2;
  private indexer: Indexer;
  private appClient: PogadjanjeClient | null = null;
  private appId: number = 0;
  private appAdress: string = "";

  constructor() {
    const algodConfig = getAlgodConfigFromViteEnvironment();
    this.algodClient = algokit.getAlgoClient(algodConfig) as Algodv2;
    const indexerConfig = getIndexerConfigFromViteEnvironment();
    this.indexer = algokit.getAlgoIndexerClient(indexerConfig) as Indexer;
  }

  public async initializeAppClient(activeAdress: string, signer: any): Promise<void> {
    const appDetails = {
      resolveBy: 'creatorAndName',
      name: 'Pogadjanje',
      sender: { signer, addr: activeAdress },
      creatorAddress: activeAdress,
      findExistingUsing: this.indexer
    } as AppDetails;
    this.appClient = new PogadjanjeClient(appDetails, this.algodClient)
  }

  public async fetchAlgoBalance(activeAddress: string) {
    try {
      const accountInfo = await this.algodClient.accountInformation(activeAddress).do();
      const balance = accountInfo.amount / 1e6;
      console.log(`Balance: ${balance} Algo`);
      return balance
    } catch (error) {
      console.error('Failed to fetch account balance:', error);
      throw error;
    }
  }

  public fetchAdress(){
    return this.appAdress;
  }

  public async deployContract(deployParams: any, activeAddress: string, signer: any): Promise<string> {
    if (!this.appClient) {
      await this.initializeAppClient(activeAddress, signer);
    }
    try {
      const response = await this.appClient?.deploy(deployParams)
      this.appId = Number(response?.appId);
      this.appAdress = response?.appAddress + "";
      return `Contract deployed successfully with appId: ${this.appId}`;
    } catch (error) {
      throw new Error(`Error deploying the contract: ${((error) as Error).message}`);
    }
  }

  public async optInToApp(): Promise<string> {
    if (this.appId === 0) {
        throw new Error('App is not deployed yet!');
    }

    try {
        this.appClient?.optIn.bare()

        return `Opt-in successful for appId: ${this.appId} `;
    } catch (error) {
        throw new Error(`Error during opt-in: ${((error) as Error).message}`);
    }
}

  public async zapocni_igru(): Promise<string> {
    try {
      const start = this.appClient?.zapocniIgru(this.appClient)

      return "App started succesfully"
  } catch (error) {
      throw new Error(`Error during starting: ${((error) as Error).message}`);
  }
  }

  public async pogodi(uplata: Transaction, broj: number): Promise<any> {

    if (!this.appClient) throw new Error('appClient not initialized');
    try {

      const response = await this.appClient.pogodi({ uplata: uplata, broj: broj });
      const odgovor = await this.appClient.rezultatIgre.call
      return odgovor;
    } catch (error) {
      throw new Error(`${((error) as Error).message}`);
    }
  }

  public async getApplicationState(): Promise<PogadjanjeGameState> {
    if (this.appId === 0) {
      throw new Error('App is not deployed yet!');
    }

    try {
      const appInfo = await this.algodClient.getApplicationByID(this.appId).do();
      const stateData: Partial<PogadjanjeGameState> = {};

      appInfo.params['global-state'].forEach((state) => {
        const key = decodeBase64(state.key);
        const value = state.value.type === 2 ? state.value.uint : decodeBase64(state.value.bytes);

        switch (key) {
          case 'rezultat':
            stateData.rezultat = value as number;
            break;
          case 'skriveni_broj':
            stateData.skriveniBroj = value as number;
            break;
        }
      },
      appInfo.params['local-state'].forEach((state) => {
        const key = decodeBase64(state.key);
        const value = state.value.type === 2 ? state.value.uint : decodeBase64(state.value.bytes)

        switch(key){
          case 'brojac':
            stateData.brojac = value as number
            break;
        }
      })
      );

      return stateData as PogadjanjeGameState;
    } catch (e) {
      console.error('Error retrieving application state:', e);
      throw e;
    }
  }
}

function decodeBase64(base64String: string): string {
  return typeof Buffer !== 'undefined'
    ? Buffer.from(base64String, 'base64').toString()
    : atob(base64String);
}

export default new AlgorandService();
