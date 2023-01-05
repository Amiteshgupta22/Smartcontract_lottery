from brownie import (accounts, network, config , MockV3Aggregator, Contract,VRFCoordinatorMock,LinkToken,interface)
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]
FORK_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork"]
import dotenv
# dotenv.load()


def get_account(index = None , id=None):
    if index:
        # its obvious that index is passed when Im on a development or local network or forked
        return accounts[index]
    if id:
        return accounts.load(id)

    # print(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS)
    # print(network.show_active() in FORK_BLOCKCHAIN_ENVIRONMENTS)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORK_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
     
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator ,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken    
}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active()  in  LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type)<=0:
            deploy_mock()
        contract = contract_type[-1]
        contract_address = contract.address
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # now we will get the contract from abi
        contract = Contract.from_abi(contract_type._name , contract_address , contract_type.abi)
                                    # movkv3aggregator                         # Mockv3aggregatorabi
    return contract    



decimal = 8
Starting_value = 200000000000
# this gives ether/usd = 2000
def deploy_mock(decimals = decimal , initial_value = Starting_value):
    account= get_account()
    print(f"Deploying to mock{network.show_active()}")
    MockV3Aggregator.deploy(decimal , Starting_value,{"from":account})
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address , {"from":account})
    price_feed = MockV3Aggregator[-1].address



def fund_link(contact_address,link_token=None,account=None,value = 250000000000000000):
    account = account  if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # tx = link_token.transfer(contact_address,value,{"from":account})
    link_token_contract =  interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(contact_address,value,{"from":account})
    
    tx.wait(1)
    print("Contract funded !")
    return tx