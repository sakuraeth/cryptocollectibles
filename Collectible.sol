pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mintNFT(address recipient, string memory tokenURI) public returns (uint256) {
        require(recipient != address(0), "MyNFT: mint to the zero address");
        
        _tokenIds.increment();
        
        uint256 newItemId = _tokenIds.current();
        
        _mint(recipient, newItemId);
        
        _setTokenURI(newItemId, tokenURI);
        
        return newItemId;
    }

    function transferNFT(address from, address to, uint256 tokenId) public {
        require(to != address(0), "MyNFT: transfer to the zero address");
        
        require(_isApprovedOrOwner(_msgSender(), tokenId), "MyNFT: caller is not owner nor approved");
        
        _transfer(from, to, tokenId);
    }

    function getTokenDetails(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "MyNFT: query for nonexistent token");
        
        return tokenURI(tokenId);
    }
}