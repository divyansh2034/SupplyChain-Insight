const SupplyChain = artifacts.require("SupplyChain");

module.exports = async function(deployer) {
  try {
    await deployer.deploy(SupplyChain);
    const instance = await SupplyChain.deployed();
    console.log("SupplyChain deployed at:", instance.address);
  } catch (error) {
    console.error("Error deploying SupplyChain:", error);
    throw error;
  }
};