from brownie import Lottery,config,network
from scripts.helpful_scripts import get_account, get_contract,fund_link
import time
def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(get_contract("eth_usd_price_feed").address,
    get_contract("vrf_coordinator").address,
    get_contract("link_token").address,
    config["networks"][network.show_active()]["fee"],
    config["networks"][network.show_active()]["keyhash"] , {"from":account})
    # publish_source =config["networks"][network.show_active()].get("verify", False))
    print("Deployed !")
    return lottery
    
def start_lottery():
    print("Entered")
    account = get_account()
    lottery = Lottery[-1]
    tx_hash = lottery.startLottery({"from":account})
    print("Transaction done !")
    tx_hash.wait(1)
    # it is neccesary to do if you use function of deployed contract
    # required only when there is a transaction ie changing the state of blockchain
    print("Lottery started !")
    
def enter_lottery():
    print("entered the enter function")
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee({"from":account})+10000000
    tx = lottery.enter({"from":account, "value":value})
    print("transaction done !")
    tx.wait(1)
    print("You entered the lottery successfully!")

def end_lottery():
    print("enters the endLottery")
    account = get_account()
    lottery = Lottery[-1]
    tx_ = fund_link(lottery.address)
    tx_.wait(1)
    print("Funded")
    tx = lottery.endLottery({"from":account})

    print("transaction done")
    # this will return the transaction hash not the return value of end lottery
    tx.wait(1)
    time.sleep(60)
    print("Lottery completed !")
    print(f"{lottery.recentWinner} is the Winner !")






def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
    
    # print(len(Lottery))