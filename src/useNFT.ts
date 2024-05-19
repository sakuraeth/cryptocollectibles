import { useEffect, useState, useMemo } from 'react';
import Web3 from 'web3';
import { AbiItem } from 'web3-utils';
import ERC721ABI from './ERC721ABI.json';

const CONTRACT_ADDRESS = process.env.REACT_APP_CONTRACT_ADDRESS!;
const INFURA_KEY = process.env.REACT_APP_INFURA_KEY;

const useNFTBlockchain = () => {
  const [web3, setWeb3] = useState<Web3>();
  const [contract, setContract] = useState<any>();
  const [account, setAccount] = useState<string>('');
  const [tokenURICache, setTokenURICache] = useState<{ [key: number]: any }>({});

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

  const fetchMultipleTokenURIs = async (tokenIds: number[]) => {
    if (!web3 || !contract) return;

    const uncachedTokenIds = tokenIds.filter(id => !tokenURICache[id]);

    if (uncachedTokenIds.length === 0) {
      return tokenIds.map(id => tokenURICache[id]);
    }

    const batch = new web3.BatchRequest();
    const tokenURIPromises = uncachedTokenIds.map(tokenId => {
      return new Promise((resolve, reject) => {
        const request = contract.methods.tokenURI(tokenId).call.request({}, (error, result) => {
          if (error) reject(error);
          else {
            setTokenURICache(prevCache => ({ ...prevCache, [tokenId]: result }));
            resolve(result);
          }
        });
        batch.add(request);
      });
    });

    batch.execute();

    try {
      await Promise.all(tokenURIPromises);
      // Return combined results from cache and fresh fetch
      return tokenIds.map(id => tokenURICache[id]);
    } catch (error) {
      console.error('Error fetching multiple token URIs:', error);
    }
  };

  const fetchNFTData = async () => {
    // Placeholder - Implement as needed
  };

  const transferNFT = async () => {
    // Placeholder - Implement as needed
  };

  const memoizedValues = useMemo(() => ({
    mintNFT,
    fetchNFTData,
    transferNFT,
    fetchMultipleTokenURIs
  }), [contract, account, tokenURICache]);

  return memoizedValues;
};

export default useNFTBlockchain;