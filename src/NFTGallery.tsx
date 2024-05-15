import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";

type NFTItem = {
  id: string;
  name: string;
  image: string;
  description: string;
};

const NFTGallery: React.FC = () => {
  const [nfts, setNfts] = useState<NFTItem[]>([]);
  const [selectedNft, setSelectedNft] = useState<NFTItem | null>(null);
  
  const cache: any = {};

  const fetchNFTs = useCallback(async () => {
    const url = "https://example.com/api/nfts";
    if (cache[url]) {
      console.log("Fetching from cache");
      setNfts(cache[url]);
      return;
    }

    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${process.env.REACT_APP_API_KEY}`,
      },
    });
    cache[url] = response.data;
    setNfts(response.data);
  }, []);

  useEffect(() => {
    fetchNFTs();
  }, [fetchNFTs]);

  const handleNftClick = (nft: NFTItem) => {
    setSelectedNft(nft);
  };

  const handleBuy = () => {
    console.log("Buying", selectedNft?.name);
  };

  const handleSell = () => {
    console.log("Selling", selectedNft?.name);
  };

  return (
    <div>
      <h2>NFT Gallery</h2>
      <div className="nft-gallery">
        {nfts.map((nft) => (
          <div key={nft.id} className="nft-item" onClick={() => handleNftClick(nft)}>
            <img src={nft.image} alt={nft.name} />
            <h4>{nft.name}</h4>
          </div>
        ))}
      </div>
      {selectedNft && (
        <div className="nft-details">
          <h3>{selectedNft.name}</h3>
          <p>{selectedNft.description}</p>
          <img src={selectedNft.image} alt={selectedNft.name} />
          <button onClick={handleBuy}>Buy</button>
          <button onClick={handleSell}>Sell</button>
        </div>
      )}
    </div>
  );
};

export default NFTGallery;