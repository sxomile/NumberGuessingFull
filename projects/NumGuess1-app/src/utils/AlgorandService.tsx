import * as algokit from '@algorandfoundation/algokit-utils'
import { Algodv2, Indexer, Transaction } from 'algosdk';
import { PogadjanjeClient } from '../contracts/Pogadjanje'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from './network/getAlgoClientConfigs'
import { AppDetails } from '@algorandfoundation/algokit-utils/types/app-client';

class AlgorandService {
  private algodClient: Algodv2;
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

  public getAlogdClient(){
    return this.algodClient;
  }

  public fetchAdress(){
    return this.appAdress;
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

  public async fetchAlgoBalance(activeAddress: string) {
    try {
      const accountInfo = await this.algodClient.accountInformation(activeAddress).do();
      const balance = accountInfo.amount / 1e6;
      return balance
    } catch (error) {
      console.error('Failed to fetch account balance:', error);
      throw error;
    }
  }

  public async optInToApp(): Promise<string> {
    try {
        this.appClient?.optIn.bare()

        return `Opt-in successful for appId: ${this.appId} `;
    } catch (error) {
        throw new Error(`Error during opt-in: ${((error) as Error).message}`);
    }
}

  public async zapocniIgru(): Promise<string> {
    try {
      this.appClient?.zapocniIgru(this.appClient)

      return "App started succesfully"
  } catch (error) {
      throw new Error(`Error during starting: ${((error) as Error).message}`);
  }
  }

  public async pogodi(uplata: Transaction, broj: number): Promise<any> {

    if (!this.appClient) throw new Error('appClient not initialized');
    try {

      await this.appClient.pogodi({ uplata: uplata, broj: broj });
      const odgovor = await this.appClient.rezultatIgre.call
      return odgovor;
    } catch (error) {
      throw new Error(`${((error) as Error).message}`);
    }
  }

}
export default new AlgorandService();
