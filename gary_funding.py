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

    # funding api
    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)

    # 资金划转  Funds Transfer
    assetArr = ['BICO', 'XCH', 'CQT', 'BZZ', 'ETH', 'GRT', 'DOT', 'FIL', 'DYDX', 'LINK', 'AR', 'SOL', 'UNI','MATIC','FLOW','STORJ']
    for asset in assetArr:
        result = fundingAPI.get_balances(asset) # 获取资金账户余额信息  Get Balance # 6次/s
        availBal = result['data'][0]['availBal']
        if availBal != '0':
            result = fundingAPI.funds_transfer(ccy=asset, amt=availBal, type='0', froms="6", to="18",subAcct='') # 1 次/s
            print(json.dumps(result))
        time.sleep(1) # 睡眠1s