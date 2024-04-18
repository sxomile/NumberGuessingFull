import React, { useState } from 'react';
import { useSnackbar } from 'notistack';
import { useWallet } from '@txnlab/use-wallet';
import ConnectWallet from './components/ConnectWallet';
import AppCalls from './components/AppCalls';
import AlgorandService from './utils/AlgorandService';
import { Transaction } from 'algosdk';

const Home: React.FC = () => {
  const [appCreated, setAppCreated] = useState<number>(0);
  const [openWalletModal, setOpenWalletModal] = useState<boolean>(false);
  const [appCallsDemoModal, setAppCallsDemoModal] = useState<boolean>(false);

  const { activeAddress, signer } = useWallet();
  const { enqueueSnackbar } = useSnackbar();

  const toggleWalletModal = () => setOpenWalletModal(!openWalletModal)
  const toggleAppCallsModal = () => setAppCallsDemoModal(!appCallsDemoModal)

  const fetchAdress = () => {
    return AlgorandService.fetchAdress()
  }

  const fetchBalance = async () => {
    return AlgorandService.fetchAlgoBalance("" + activeAddress)
  }

  const handleOptInClick = async () => {
    try {
        const response = await AlgorandService.optInToApp();
        enqueueSnackbar(response, { variant: 'success' });
    } catch (error) {
        enqueueSnackbar(`Opt-in failed: ${((error)as Error).message}`, { variant: 'error' });
    }
};

const handleZapocniClick = async () => {
  try{
    const response = await AlgorandService.zapocniIgru()
    enqueueSnackbar(response, {variant: 'success'})
  } catch(error){
    enqueueSnackbar(`Starting game failed: ${error}`)
  }
}

  const handleDeployClick = async () => {
    try {
      const deployParams = {
        onSchemaBreak: 'append',
        onUpdate: 'append',
      }
      const response = await AlgorandService.deployContract(deployParams, activeAddress || "", signer)

      enqueueSnackbar(`Message: ${response}`, { variant: 'success' })

    } catch (error) {
      enqueueSnackbar(`Deployment failed: ${((error)as Error).message}`, { variant: 'error' })
    }

  };

  async function actions(){
    if(appCreated == 0){
      await handleDeployClick();
      await handleOptInClick();
      await handleZapocniClick();
      setAppCreated(1);
    }
    toggleAppCallsModal();
  }

  const secretGuess = async (uplata: Transaction, guess: number): Promise<string> => {

    const response = await AlgorandService.pogodi(uplata, guess);
    return response;
  }

  return (
    <div className="hero min-h-screen bg-teal-400">
      <div className="hero-content text-center rounded-lg p-6 max-w-md bg-white mx-auto">

        <h2 className="text-4xl">Welcome to Number Guessing Game!</h2>
        <div>Please connect your wallet and place your bid :)</div>
        <div className="grid">
          <div className="divider" />
          <button className="btn m-2" onClick={toggleWalletModal}>Wallet Connection</button>
          {activeAddress && <button className="btn m-2" onClick={actions}>Let's play!</button>}
        </div>
        <ConnectWallet openModal={openWalletModal} closeModal={toggleWalletModal} />
        <AppCalls openModal={appCallsDemoModal} setModalState={setAppCallsDemoModal} secretGuess={secretGuess}
        getBalance = {fetchBalance} getAdress = {fetchAdress}/>
      </div>
    </div>
  );
};

export default Home;
