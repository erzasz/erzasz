from etherscan.accounts import Account
from etherscan.transactions import Transactions
from etherscan.proxies import Proxies
import json
import datetime
import schedule
import time
import os

import colorama
from colorama import Fore, Back, Style
colorama.init()


def clear(): os.system('cls') #on Windows System

with open('api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

addressList = ['0x6c9fca89ff18e7b5a0172406d228ab1e056b51f7']#,'0x20360c2e04afe0dcc526b1f6936246fce5a246ac']
addressListLength = len(addressList)
prevTransactions = 0
prevText = ""
lastApproved = ""

def refreshTransactions():
    for k in range(addressListLength):
        lastContract = '000'
        api = Account(address=addressList[k], api_key=key)
        transactions = api.get_transaction_page(page=1, offset=5, sort='desc', erc20=True)
        transactions2 = api.get_transaction_page(page=1, offset=5, sort='desc')
        for element in transactions:
            element.pop('confirmations', None)
        #transactions = transactionsTest.remove('confirmations')
        dashString = ("--------------------------------")
        global prevTransactions
        #print(prevTransactions)
        global prevText
        global text
        global lastApproved
        if transactions != prevTransactions:
            prevTransactions = transactions
            print(Back.BLUE)
            print("TRANSACTIONS FOR: " + addressList[k])
            print(Style.RESET_ALL)
            #print("\n")
            prevText = ""
            for i in reversed(transactions):
                if i['to'] == addressList[0]:
                    print(Back.GREEN)
                    TX_HASH = i['hash']
                    dateToConv = datetime.datetime.fromtimestamp(int(i['timeStamp']))
                    print("IN >>>>>>>>>>>>>>>>>>>>>>>>>>", dateToConv.strftime('%Y-%m-%d %H:%M:%S'),i['tokenSymbol'] + ' ' + i['contractAddress'], sep='\n')
                    print(Style.RESET_ALL)
                    print(dashString)
                    for u in reversed(transactions2):
                          global lastApproved
                          #lastApproved = ""
                          if u['to'] == i['contractAddress'] and lastApproved != u['to']:
                              print(Back.WHITE)
                              print(Fore.BLACK)
                              print(datetime.datetime.fromtimestamp(int(u['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S') + " " + "APPROVAL FOR: " + i['tokenSymbol'] + " " + u['to'])
                              lastApproved = u['to']
                              print(Style.RESET_ALL)
                              print(dashString)
                elif i['to'] == "0x0000000000000000000000000000000000000000":
                    print(datetime.datetime.fromtimestamp(int(i['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S') + " " + "0x000000000000000000000000000000000000000")
                elif i['to'] != addressList[0]:
                    print(Back.RED)
                    TX_HASH = i['hash']
                    dateToConv = datetime.datetime.fromtimestamp(int(i['timeStamp']))
                    print("OUT <<<<<<<<<<<<<<<<<<<<<<<<<<", dateToConv.strftime('%Y-%m-%d %H:%M:%S'),i['tokenSymbol'] + ' ' + i['contractAddress'], sep='\n')
                    lastContract = i['contractAddress']
                    print(Style.RESET_ALL)
                    print(dashString)
        else:

            text = "No new transactions..."
            if prevText == text:
               return 0
            else:
                print("No new transactions...")
                prevText = "No new transactions..."

#refreshTransactions()
def fetchTransactions():
    #clear()
    refreshTransactions()
#time
schedule.every(10).seconds.do(fetchTransactions)
while True:
   schedule.run_pending()
   time.sleep(1)
