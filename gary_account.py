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




def func_token_price(marketAPI):

    instId_arr = ['BICO-USDT', 'XCH-USDT', 'CQT-USDT', 'BZZ-USDT', 'ETH-USDT', 'GRT-USDT', 'DOT-USDT', 'FIL-USDT', 'DYDX-USDT', 'LINK-USDT', 'AR-USDT', 'SOL-USDT', 'UNI-USDT','MATIC-USDT','FLOW-USDT','STORJ-USDT']
    result = marketAPI.get_tickers('SPOT')
    asset_arr = []
    seq = 0
    for token in result['data']:
        if token['instId'] in instId_arr:
            seq += 1
            asset_dict = {}
            asset_dict['序号']=seq
            asset_dict['交易对'] = token['instId']
            asset_dict['卖一价'] = token['askPx']
            asset_arr.append(asset_dict)
    print(json.dumps(asset_arr))


def func_sell_asset(tradeAPI, asset_arr):
    # 查看账户币种余额信息
    # assetArr = ['BICO', 'XCH', 'CQT', 'BZZ', 'ETH', 'GRT', 'DOT', 'FIL', 'DYDX', 'LINK', 'AR', 'SOL', 'UNI','MATIC','FLOW','STORJ']
    result = accountAPI.get_account()
    assetArr=result['data'][0]['details']
    asset_arr = []
    seq = 0
    for asset in assetArr:
        if float(asset['disEq']) > 0.1:
            seq += 1
            asset_dict = {}
            asset_dict['序号']=seq
            asset_dict['币名']=asset['ccy']
            asset_dict['可操作余额']=asset['availEq']
            asset_dict['价值']=asset['disEq']
            asset_arr.append(asset_dict)
    print(json.dumps(asset_arr))

    # 批量卖出资产
    for asset in asset_arr:
        if asset['ccy'] == 'USDT':
            continue
    
        # 批量下单卖出
        result = tradeAPI.place_multiple_orders([
            {'instId': asset_dict['币名']+'-USDT', 'tdMode': 'cash', 'clOrdId': asset_dict['币名']+'_1', 'side': 'sell', 'ordType': 'market', 'sz': str(asset_dict['可操作余额'])}
        ])
        print(json.dumps(result))


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
     # trade API
    tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

    # 查看价格
    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    func_token_price(marketAPI)