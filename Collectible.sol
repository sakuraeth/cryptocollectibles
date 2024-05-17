pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _totalMintedTokens;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mintToken(address recipient, string memory metadataURI) public returns (uint256) {
        require(recipient != address(0), "MyNFT: mint to the zero address");
        
        _totalMintedTokens.increment();
        
        uint256 newTokenId = _totalMintedTokens.current();
        
        _mint(recipient, newTokenId);
        
        _setTokenURI(newTokenId, metadataURI);
        
        return newTokenId;
    }

    function transferToken(address sender, address receiver, uint256 tokenId) public {
        require(receiver != address(0), "MyNFT: transfer to the zero address");
        
        require(_isApprovedOrOwner(_msgSender(), tokenId), "MyNFT: caller is not owner nor approved");
        
        _transfer(sender, receiver, tokenId);
    }

    function fetchTokenMetadata(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "MyNFT: query for nonexistent token");
        
        return tokenURI(tokenId);
    }
}