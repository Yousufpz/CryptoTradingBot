import talib
import websocket
import json
import numpy as np
from talib import abstract

# Buy function
def buy(allocated_money,price):
  print("in buy")
  global portfolio, money_end
  #print('on line 11')
  print(portfolio)
  print(money_end)
  quantity = allocated_money / price
  print(quantity)
  #print(money_end+"\n"+allocated_money+"\n"+transaction_cost+"\n"+allocated_money)
  
  money_end = money_end - allocated_money - transaction_cost*allocated_money
  
  print(money_end)

  portfolio += quantity
  print(portfolio)
  
  if investment == []:
    investment.append(allocated_money)
  else:
    investment.append(allocated_money)
    investment[-1] += investment[-2]

# Sell function
def sell(allocated_money,price):
  print("in sell")
  global portfolio, money_end
  quantity = allocated_money / price
  money_end = money_end + allocated_money -transaction_cost*allocated_money
  portfolio -= quantity
  investment.append(-allocated_money)
  investment[-1] += investment[-2]

# Bitcoin Bot

def on_close(ws):
  port_value = portfolio*closes[-1]
  if port_value > 0:
    sell(port_value,price = closes[-1])
  else:
    buy(-port_value, price = closes[-1])
  money_end += investment[-1]
  print('All trades settled')

def on_message(ws,message):
  #print("on_message")
  global portfolio, investment, closes, highs, lows, money_end, core_to_trade, core_quantity, real_time_portfolio_value
  json_message = json.loads(message)
  cs = json_message['k']
  candle_closed, close, high, low, open, volume = cs['x'], cs['c'], cs['h'], cs['l'], cs['o'], cs['v']
  candle = [open,high,low,close,volume]
  #print(candle_closed)

  if candle_closed:
    for i in candles:
      i.append(float(candle[candles.index(i)]))
    #print(f'Closes: {closes}')
    inputs = {'open': np.array(opens), 'high': np.array(highs), 'low': np.array(lows), 'close': np.array(closes), 'volume': np.array(volumes)}
    #print(inputs)

    if core_to_trade:
      print('in core_to_trade')
      #print(core_trade_amount)
      buy(core_trade_amount, price=closes[-1])
      print(f'Core Investment: We bought ${core_trade_amount} worth of bitcoin', '\n')
      core_quantity += core_trade_amount/closes[-1]
      print(core_quantity)
      core_to_trade = False
      print(core_to_trade)
    
    # aroon = talib.AROONOSC(np.array(highs), np.array(lows), aroon_time_period)
    indicators = []
    for method in public_method_names:
      indicator = getattr(f, method)(inputs)
      indicators.append(indicator[-1])
    av_indicator = np.mean(indicators)
    print(av_indicator)
    
    if av_indicator >= 10:
      amt = trade_amount
    elif av_indicator <= -10:
      amt = -trade_amount
    else:
      amt = av_indicator*10
    port_value = portfolio*closes[-1] - core_quantity*closes[-1]
    trade_amt = amt - port_value
    RT_portfolio_value = money_end + portfolio*closes[-1]
    real_time_portfolio_value.append(float(RT_portfolio_value))
    print(f'Average of all indicators is "{av_indicator}" and recommended exposure is "${amt}"')
    print(f'Real-Time Portfolio Value: ${RT_portfolio_value}', '\n')
    print('__________________________')
    print('__________________________')
    print(f'Invested amount: ${portfolio*closes[-1]}')
    print('\n______END OF BOT CYCLE____')
    print('__________________________')
    
    if trade_amt > min_trade_amt:
      buy(trade_amt, price=closes[-1])
      print(f'We bought ${trade_amt} worth of bitcoin', '\n', '\n')
    elif trade_amt < -min_trade_amt:
      sell(-trade_amt, price=closes[-1])
      print(f'We sold ${-trade_amt} worth of bitcoin', '\n', '\n')

cc = 'btcusd'
interval = '1m'

socket = f'wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}'

# Trading Strategy Parameters
amount = 1000
core_trade_amount = amount*0.90
core_quantity = 0
trade_amount = amount*0.10
core_to_trade = True
transaction_cost = 0.0005
min_trade_amt = 30

portfolio = 0
investment, real_time_portfolio_value, closes, highs, lows, opens, volumes = [], [], [], [], [], [], []
money_end = amount
candles = [opens,highs,lows,closes,volumes]


  
  
import inspect

f = abstract
dir1 = dir(f)
public_method_names = [method for method in dir1 if method.startswith('CDL')]



ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
ws.run_forever()

print(investment)

port_value = portfolio*closes[-1]
if port_value > 0:
  sell(port_value,price = closes[-1])
else:
  buy(-port_value, price = closes[-1])
money_end += investment[-1]
print('All trades settled')
