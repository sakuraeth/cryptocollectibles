import { useEffect, useState } from 'react';
import Web3 from 'web3';
import { AbiItem } from 'web3-utils';
import ERC721ABI from './ERC721ABI.json';

const CONTRACT_ADDRESS = process.env.REACT_APP_CONTRACT_ADDRESS!;
const INFURA_KEY = process.env.REACT_APP_INFURA_KEY;

const useNFTBlockchain = () => {
  const [web3, setWeb3] = useState<Web3>();
  const [contract, setContract] = useState<any>();
  const [account, setAccount] = useState<string>('');

  useEffect(() => {
    const initWeb3 = async () => {
      if (window.ethereum) {
        const web3Instance = new Web3(window.ethereum);
        try {
          await window.ethereum.enable();
          const accounts = await web3Instance.eth.getAccounts();
          setAccount(accounts[0]);
        } catch (error) {
          console.error('User denied account access');
        }
        setWeb3(web3Instance);
        const contractInstance = new web3Instance.eth.Contract(ERC721ABI as AbiItem[], CONTRACT_ADDRESS);
        setContract(contractInstance);
      } else if (window.web3) {
        setWeb3(new Web3(window.web3.currentProvider));
      } else {
        const provider = new Web3.providers.HttpProvider(
          `https://mainnet.infura.io/v3/${INFURA_KEY}`
        );
        setWeb3(new Web3(provider));
      }
    };

    initWeb3();
  }, []);

  const mintNFT = async (tokenURI: string) => {
    if (!contract || !account) return;
    try {
      const response = await contract.methods.mint(account, tokenURI).send({ from: account });
      return response;
    } catch (error) {
      console.error('Error minting NFT:', error);
    }
  };

  const fetchNFTData = async (tokenId: number) => {
    if (!contract) return;
    try {
      const tokenURI = await contract.methods.tokenURI(tokenId).call();
      return tokenURI;
    } catch (error) {
      console.error('Error fetching NFT data:', error);
    }
  };

  const transferNFT = async (to: string, tokenId: number) => {
    if (!contract || !account) return;
    try {
      const response = await contract.methods.safeTransferFrom(account, to, tokenId).send({ from: account });
      return response;
    } catch (error) {
      console.error('Error transferring NFT:', error);
    }
  };

  return { mintNFT, fetchNFTData, transferNFT };
};

export default useNFTBlockchain;