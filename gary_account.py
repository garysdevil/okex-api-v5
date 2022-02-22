import okex.Account_api as Account
import okex.Funding_api as Funding
import okex.Market_api as Market
import okex.Public_api as Public
import okex.Trade_api as Trade
import okex.subAccount_api as SubAccount
import okex.status_api as Status
import json

import configparser
import time


if __name__ == '__main__':
    file = '.config.ini'
    # 创建配置文件对象
    con = configparser.ConfigParser()
    # 读取文件
    con.read(file, encoding='utf-8')
    loginInfo = dict(con.items('login_info'))
    api_key = loginInfo['api_key']
    secret_key = loginInfo['secret_key']
    passphrase = loginInfo['passphrase']

    # flag是实盘与模拟盘的切换参数 flag is the key parameter which can help you to change between demo and real trading.
    # flag = '1'  # 模拟盘 demo trading
    flag = '0'  # 实盘 real trading

    # account api
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    # 查看账户持仓风险 GET Position_risk
    # result = accountAPI.get_position_risk('SWAP')
    # 查看账户余额  Get Balance
    result = accountAPI.get_account()
    assetArr=result['data'][0]['details']
    for asset in assetArr:
        print(asset['ccy'])
        print('可操作余额', asset['availEq'])
        print('价值', asset['disEq'])
    
#     {
#   "code": "0",
#   "data": [
#     {
#       "adjEq": "",
#       "details": [
#         {
#           "availBal": "",

    # print(json.dumps(result))