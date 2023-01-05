from scripts.helpful_scripts import (
    get_account,
    fund_link,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS
)
from brownie import network,exceptions,Lottery
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest


def test_entrance():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery_contract = deploy_lottery()
    expected = Web3.toWei(0.025,"ether")
    value = lottery_contract.getEntranceFee()
    assert expected==value


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account=get_account()
    lottery_contract = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery_contract.enter({"from":account, "value":lottery_contract.getEntranceFee()})

def test_can_start_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery_contract = deploy_lottery()
   
    lottery_contract.startLottery({"from":account})
   
    lottery_contract.enter({"from":account, "value":lottery_contract.getEntranceFee()})
    assert lottery_contract.players(0)==account


def test_end():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery_contract = deploy_lottery()
    lottery_contract.startLottery({"from":account})
    lottery_contract.enter({"from":account, "value":lottery_contract.getEntranceFee()})
    fund_link(lottery_contract.address)
    lottery_contract.endLottery({"from":account})
    assert lottery_contract.lottery_state() ==2

def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery_contract = deploy_lottery()
    lottery_contract.startLottery({"from":account})
    lottery_contract.enter({"from":account, "value":lottery_contract.getEntranceFee()})
    lottery_contract.enter({"from":get_account(index=1), "value":lottery_contract.getEntranceFee()})
    lottery_contract.enter({"from":get_account(index=2), "value":lottery_contract.getEntranceFee()})
    fund_link(lottery_contract.address)
    tx = lottery_contract.endLottery({"from":account})
    request_id = tx.events["RequestedRandomness"]["requestId"]
    Random_no = 444

    starting_balance = account.balance()
    starting_balance_lottery = lottery_contract.balance()
    # this is my mock random number
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id,Random_no,lottery_contract.address
    )
    # 444%3 =  0
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() ==0
    assert account.balance() == starting_balance + starting_balance_lottery


    
   
def main():
    # print(test_cant_enter_unless_started())
    # print(test_entrance())
    # print(test_can_start_enter)
    # print(test_end())
    print(test_can_pick_winner_correctly)
    
    
    