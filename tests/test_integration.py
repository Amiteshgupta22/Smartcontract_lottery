from brownie import network,Lottery,config
from scripts.helpful_scripts import (get_account,fund_link, get_contract,LOCAL_BLOCKCHAIN_ENVIRONMENTS)
from scripts.deploy_lottery import deploy_lottery
import pytest
import time
def test_can_pick_winner():
    # if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #     pytest.skip()
    account = get_account()
    lottery_contract = deploy_lottery()
    lottery_contract.startLottery({"from":account})
    lottery_contract.enter({"from":account, "value":lottery_contract.getEntranceFee()})
    lottery_contract.enter({"from":get_account(), "value":lottery_contract.getEntranceFee()})
    # lottery_contract.enter({"from":get_account(index=2), "value":lottery_contract.getEntranceFee()})
    fund_link(lottery_contract.address)
    lottery_contract.endLottery({"from":account})

    # in unity we pretended to be the chain link node but here we wait for chain link node to respond
    time.sleep(60)
    assert lottery_contract.recentWinner()==account
    assert lottery_contract.balance()==0

def main():
    test_can_pick_winner()
