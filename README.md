# Time Bank Application with Algorand and PyTeal

## Introduction

This project is an innovative application leveraging the Algorand blockchain
and PyTeal, the Python SDK for Algorand smart contracts. Algorand provides a
decentralized, scalable, and secure blockchain network, ideal for modern
financial applications.

## Architecture

### Algorand and PyTeal

Our application uses Algorand for its blockchain backend, with smart contracts
written in PyTeal. PyTeal offers a Pythonic way to write secure and efficient
smart contracts for the Algorand network.

### Docker Compose for Algorand Node

We utilize Docker Compose to manage and run an Algorand node service, ensuring
a consistent and isolated environment for blockchain interactions.

### Flask Application

The frontend interaction with our Algorand/PyTeal backend is handled by a Flask
web application. Flask, a lightweight and flexible Python web framework, allows
for easy management of web requests and integrates seamlessly with PyTeal for
blockchain operations.

## Functionality

Our Time Bank application allows users to manage time credits. It includes
features for adding, viewing, and editing member information and transactions,
all tied to smart contract logic on the Algorand blockchain.

This README provides a high-level overview. For detailed setup and usage
instructions, please refer to the specific sections in this document.
