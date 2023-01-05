For Interfaces:
1. Either you import them or you just copy and paste them.
2. I can also copy and paste the contract of this interface.
3. You need to pass the argument into the interface .
4. Interfaces are not required to be deployed.
5. Interfaces are used where live data is required ex: Pricefeed usd/eth conversion

6.  Infura is used to connect to testnet, so i want to deploy my code to goerli then I need it ,not needed in case of local,
or development.

your code is written in .sol only but to deploy it you need deploy script so justwrtie all the function in .sol

Link Token is like etherium used for paying at sometime
Link token is like fund me which fund link to contract

Note: if there is s transation happening in that function then you cant view return of it as
tx = somefunction({"from":accpount}) then it always return tx hash
you need to make a seperate method as view only to et the required value

7. Deploy a contract return the contract
Balance:
    contract.balance()
    address.balance()