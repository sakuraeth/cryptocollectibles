import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";

type NFT = {
  id: string;
  name: string;
  image: string;
  description: string;
  isFavorite?: boolean; 
};

const NFTGallery: React.FC = () => {
  const [nftCollection, setNftCollection] = useState<NFT[]>([]);
  const [activeNFT, setActiveNFT] = useState<NFT | null>(null);
  const [nftCache, setNftCache] = useState<{ [url: string]: NFT[] }>({}); 

  const apiUrl = process.env.REACT_APP_API_URL || "https://example.com/api/nfts"; 

  const fetchNFTCollection = useCallback(async () => {
    if (nftCache[apiUrl]) {
      console.log("Loading from cache");
      setNftCollection(nftCache[apiUrl]);
      return;
    }

    try {
      const response = await axios.get(apiUrl, {
        headers: {
          Authorization: `Bearer ${process.env.REACT_APP_API_KEY}`,
        },
      });
      const nfts = response.data.map((nft: NFT) => ({ ...nft, isFavorite: false })); 
      const updatedCache = { ...nftCache, [apiUrl]: nfts };
      setNftCache(updatedCache);
      setNftCollection(nfts);
    } catch (error) {
      console.error("Failed to fetch NFTs:", error);
    }
  }, [apiUrl, nftCache]);

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

  
  const toggleFavorite = (id: string) => {
    const updatedCollection = nftCollection.map((nft) =>
      nft.id === id ? { ...nft, isFavorite: !nft.isFavorite } : nft
    );
    setNftCollection(updatedCollection);

    
    const updatedCache = { ...nftCache, [apiUrl]: updatedCollection };
    setNftCache(updatedCache);
  };

  return (
    <div>
      <h2>NFT Gallery</h2>
      <div className="nft-gallery">
        {nftCollection.map((nft) => (
          <div key={nft.id} className="nft-item" onClick={() => onNFTClick(nft)}>
            <img src={nft.image} alt={nft.name} />
            <h4>{nft.name}</h4>
            <button onClick={(e) => {
                  e.stopPropagation(); 
                  toggleFavorite(nft.id);
                }}>
              {nft.isFavorite ? "Unfavorite" : "Favorite"}
            </button>
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