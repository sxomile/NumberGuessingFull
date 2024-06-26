import { useWallet } from '@txnlab/use-wallet'
import { useMemo } from 'react'
import { ellipseAddress } from '../utils/ellipseAddress'
import { getAlgodConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

const Account = () => {
  const { activeAddress } = useWallet()
  const algoConfig = getAlgodConfigFromViteEnvironment()

  const dappFlowNetworkName = useMemo(() => {
    return algoConfig.network === '' ? 'sandbox' : algoConfig.network.toLocaleLowerCase()
  }, [algoConfig.network])

  return (
    <div>
      <a className="text-xl">
        Address: {ellipseAddress(activeAddress)}
      </a>
      <div className="text-xl">Network: {algoConfig.network === '' ? 'localnet' : algoConfig.network}</div>
    </div>
  )
}

export default Account
