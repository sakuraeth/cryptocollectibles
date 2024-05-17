import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";

type NFT = {
  id: string;
  name: string;
  image: string;
  description: string;
};

const NFTGallery: React.FC = () => {
  const [nftCollection, setNftCollection] = useState<NFT[]>([]);
  const [activeNFT, setActiveNFT] = useState<NFT | null>(null);
  
  const nftCache: { [url: string]: NFT[] } = {};

  const fetchNFTCollection = useCallback(async () => {
    const apiUrl = "https://example.com/api/nfts";
    if (nftCache[apiUrl]) {
      console.log("Loading from cache");
      setNftCollection(nftCache[apiUrl]);
      return;
    }

    const response = await axios.get(apiUrl, {
      headers: {
        Authorization: `Bearer ${process.env.REACT_APP_API_KEY}`,
      },
    });
    nftCache[apiUrl] = response.data;
    setNftCollection(response.data);
  }, []);

  useEffect(() => {
    fetchNFTCollection();
  }, [fetchNFTCollection]);

  const onNFTClick = (nft: NFT) => {
    setActiveNFT(nft);
  };

  const buySelectedNFT = () => {
    console.log("Buying", activeNFT?.name);
  };

  const sellSelectedNFT = () => {
    console.log("Selling", activeNFT?.name);
  };

  return (
    <div>
      <h2>NFT Gallery</h2>
      <div className="nft-gallery">
        {nftCollection.map((nft) => (
          <div key={nft.id} className="nft-item" onClick={() => onNFTClick(nft)}>
            <img src={nft.image} alt={nft.name} />
            <h4>{nft.name}</h4>
          </div>
        ))}
      </div>
      {activeNFT && (
        <div className="nft-details">
          <h3>{activeNFT.name}</h3>
          <p>{activeNFT.description}</p>
          <img src={activeNFT.image} alt={activeNFT.name} />
          <button onClick={buySelectedNFT}>Buy</button>
          <button onClick={sellSelectedNFT}>Sell</button>
        </div>
      )}
    </div>
  );
};

export default NFTGallery;