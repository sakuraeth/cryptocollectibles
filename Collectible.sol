// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MyNFT is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _totalMintedTokens;

    constructor() ERC721("MyNFT", "MNFT") {}

    function mintToken(address recipient, string memory metadataURI) public returns (uint256) {
        require(recipient != address(0), "MyNFT: Cannot mint to the zero address");

        _totalMintedTokens.increment();

        uint256 newTokenId = _totalMintedTokens.current();

        _mint(recipient, newTokenId);

        _setTokenURI(newTokenId, metadataURI);

        return newTokenId;
    }

    function transferToken(address sender, address receiver, uint256 tokenId) public {
        require(receiver != address(0), "MyNFT: Cannot transfer to the zero address");

        require(_isApprovedOrOwner(_msgSender(), tokenId), "MyNFT: Caller is not owner nor approved for transfer");

        _transfer(sender, receiver, tokenId);
    }

    function fetchTokenMetadata(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "MyNFT: Query for nonexistent token");

        return tokenURI(tokenId);
    }
}