import React, { useState } from 'react';
import { useSnackbar } from 'notistack';
import { useWallet } from '@txnlab/use-wallet';
import algosdk, { Transaction } from 'algosdk';
import AlgorandService from '../utils/AlgorandService';

interface AppCallsProps {
  openModal: boolean;
  setModalState: (value: boolean) => void;
  secretGuess: (uplata: Transaction, guess: number) => Promise<string>;
  getBalance: () => Promise<number>
  getAdress: () => string
}

const AppCalls: React.FC<AppCallsProps> = ({ openModal, setModalState, secretGuess, getBalance, getAdress }) => {
  const [contractInput, setContractInput] = useState<number>(0);
  const [bid, setBid] = useState<string>('')
  const { enqueueSnackbar } = useSnackbar();
  const { activeAddress } = useWallet();

  const handlePlayerMove = async () => {
    if (!activeAddress) {
      enqueueSnackbar('Please connect wallet first', { variant: 'warning' });
      return;
    }
    const algosBefore = await getBalance()
    try {

      const suggestedParams = await AlgorandService.getAlogdClient().getTransactionParams().do();
      const bidding = bid

      if(!parseInt(bidding)){
        enqueueSnackbar("Bid must be an integer!", {variant: 'warning'})
        return
      }

      const transaction = algosdk.makePaymentTxnWithSuggestedParams
      (activeAddress, getAdress(), parseInt(bidding) * 1000000, undefined, undefined, suggestedParams);

      await secretGuess(transaction, contractInput);

    } catch (error) {

      if((error as Error).message.includes('overspend')){
        enqueueSnackbar('Application doesn\'t have enough money to pay you :(\n Come back later or try lower bid :(')
        return
      }

      const algosAfter = await getBalance()
      if(algosAfter > algosBefore){
        enqueueSnackbar("Congrats! Available algos: " + algosAfter, {variant: "success"})
      } else{
        enqueueSnackbar("So close! Available algos: " + algosAfter, {variant: "error"})
      }
    }
  };

  return (
    <dialog className={`modal ${openModal ? 'modal-open' : ''}`}>
      <form className="modal-box">
        <h3 className="font-bold text-lg">Can YOU guess the hidden number?</h3>
        <input type="number" placeholder="Guess a number 1-10" className="input input-bordered w-full mt-4"
        value={contractInput.toString()} onChange={(e) => setContractInput(parseInt(e.target.value))} />
        <input type="text" placeholder="Bidding amount:" className="input input-bordered w-full mt-4"
        value={bid} onChange={(e) => setBid(e.target.value)} />
        <div className="modal-action">
          <button type="button" className="btn" onClick={() => setModalState(false)}>Close</button>
          <button type="button" className="btn btn-primary" onClick={handlePlayerMove}>Try your luck!</button>
        </div>
      </form>
    </dialog>
  );
};

export default AppCalls;
