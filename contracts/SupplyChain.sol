// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChain {
    struct Product {
        string name;
        string origin;
        string destination;
        uint scheduledDays;
        uint orderTotal;
        uint delayProbability;
        uint currentProfit;
        uint maximumPotentialProfit;
        uint[] monthlyProfits;
        address owner;
    }

    mapping(uint => Product) public products;
    uint public productCount;

    event ProductAdded(uint productId, string name, string origin, string destination, uint scheduledDays, uint orderTotal);
    event ProductUpdated(uint productId, uint delayProbability, uint currentProfit, uint maximumPotentialProfit, uint[] monthlyProfits);

    function addProduct(
        string memory name,
        string memory origin,
        string memory destination,
        uint scheduledDays,
        uint orderTotal
    ) public {
        products[productCount] = Product(
            name,
            origin,
            destination,
            scheduledDays,
            orderTotal,
            0,
            0,
            0,
            new uint[](0),
            msg.sender
        );
        emit ProductAdded(productCount, name, origin, destination, scheduledDays, orderTotal);
        productCount++;
    }

    function updateProductStatus(
        uint productId,
        uint delayProbability,
        uint currentProfit,
        uint maximumPotentialProfit,
        uint[] memory monthlyProfits
    ) public {
        Product storage product = products[productId];
        product.delayProbability = delayProbability;
        product.currentProfit = currentProfit;
        product.maximumPotentialProfit = maximumPotentialProfit;
        product.monthlyProfits = monthlyProfits;

        emit ProductUpdated(productId, delayProbability, currentProfit, maximumPotentialProfit, monthlyProfits);
    }

    function getProduct(uint productId) public view returns (
        string memory name,
        string memory origin,
        string memory destination,
        uint scheduledDays,
        uint orderTotal,
        uint delayProbability,
        uint currentProfit,
        uint maximumPotentialProfit,
        uint[] memory monthlyProfits,
        address owner
    ) {
        Product memory product = products[productId];
        return (
            product.name,
            product.origin,
            product.destination,
            product.scheduledDays,
            product.orderTotal,
            product.delayProbability,
            product.currentProfit,
            product.maximumPotentialProfit,
            product.monthlyProfits,
            product.owner
        );
    }
}