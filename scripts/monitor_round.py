import unittest
from gmobin.demo.site import DemoOrderPage
import time
import json
from gmobin.lib.logger import CatsLogging as logger
import argparse
import threading
from socket import gethostname
from gmobin.common.tool import *
import os
import sys
from gmobin.common.tool import *

"""
cron sample
0 9 * * * command
0 11 * * * command
0 13 * * * command
0 15 * * * command
0 17 * * * command
0 21 * * * command
0 23 * * * command
0 1 * * * command
"""


parser = argparse.ArgumentParser(description="cats gmo")

# args params
parser.add_argument('-cf', '--config', help="configuration file", required=True)
parser.add_argument('-r', '--round_open_time', help="round_open_time", required=True)
parser.add_argument('-t', '--target', help="target", required=True)
parser.add_argument('-out', '--out', help="out", required=True)
parser.add_argument('-log', '--log', help="log", required=True)
args = parser.parse_args()
round_open_time = args.round_open_time
output_path = f"{args.out}/{get_today_date()}"
target = args.target
print(args)

logger.init_from_json(args.log)
logger.info("catsgmo monitor?round start")

with open(args.config) as f:
    df = json.load(f)
    print(df)
    binary_location = df["binary_location"]
    executable_path = df["executable_path"]
    if df["is_headless"]  == "True":
        is_headless = True
    else:
        is_headless = False

# mkdir
try:
    os.mkdir(output_path)
except:
    print(f"{output_path} is exsited.")
    
is_stock_output = True
def option_worker(value):
    logger.info(f"option_worker start, condition value is {value}")
    full_file_path = f"{output_path}/{gethostname()}_{target}_{round_open_time.replace(':','')}_{value}_{get_current_time()}_option.csv"
    logger.info(full_file_path)
    try:
        # init
        page = DemoOrderPage(binary_location=binary_location, executable_path=executable_path, is_headless=is_headless)

        # move change_trading
        page.change_trading(trading_name=target)

        # move round
        page.move_round(round_open_time=round_open_time)
        
        # change condition
        page.transion_condition(value=str(value))
        
        #header = "trading_name,timestamp,round_date,round_open_time,round_end_time,condition_target_price,put_buy,put_sell,put_payout_price,call_buy,call_sell,call_payout_price,stock_open,stock_high,stock_low,stock_close\n"
        header = "trading_name,timestamp,round_date,round_open_time,round_end_time,condition_target_price,put_buy,put_sell,put_payout_price,call_buy,call_sell,call_payout_price\n"
        
        with open(full_file_path, mode="w") as f:
            f.write(header)
            while True:
                round_status = page.round.status
                if round_status == "END_TRADE":
                    logger.info("close")
                    is_stock_output = False
                    break
                else:
                    c = page.condition_info
                    #s = page.stock_price()
                    #f.write(f"{c.trading_name},{c.timestamp},{c.round_date},{c.round.round_open_time},{c.round.round_end_time},{c.condition.target_price.replace(',','')},{c.order_info.put.buy.replace(',','')},{c.order_info.put.sell.replace(',','')},{c.order_info.put.payout_price.replace(',','')},{c.order_info.call.buy.replace(',','')},{c.order_info.call.sell.replace(',','')},{c.order_info.call.payout_price.replace(',','')},{s.openPrice},{s.highPrice},{s.lowPrice},{s.closePrice}\n")
                    f.write(f"{c.trading_name},{c.timestamp},{c.round_date},{c.round.round_open_time},{c.round.round_end_time},{c.condition.target_price.replace(',','')},{c.order_info.put.buy.replace(',','')},{c.order_info.put.sell.replace(',','')},{c.order_info.put.payout_price.replace(',','')},{c.order_info.call.buy.replace(',','')},{c.order_info.call.sell.replace(',','')},{c.order_info.call.payout_price.replace(',','')}\n")
                    f.flush()
    except:
        logger.error(f"option_worker is stopped: {full_file_path}: {sys.exc_info()}")
    finally:
        print("option_worker stop")
        page.close()
  
def stock_worker():
    logger.info(f"stock_worker start")
    full_file_path = f"{output_path}/{gethostname()}_{target}_{round_open_time.replace(':','')}_{get_current_time()}_stock.csv"
    logger.info(full_file_path)    
    try:
        header = "timestamp,stock_open,stock_high,stock_low,stock_close\n"
        with open(full_file_path, mode="w") as f:
            f.write(header)
            while is_stock_output:
                s = DemoOrderPage.stock_price(trading_name=target)
                f.write(f"{get_current_time()},{s.openPrice},{s.highPrice},{s.lowPrice},{s.closePrice}\n")
                f.flush()
                time.sleep(0.5)
    except:
        logger.error(f"stock_worker is stopped: {full_file_path}: {sys.exc_info()}")
    finally:
        logger.info("stock_worker stop")

for i in range(1,8):
    t = threading.Thread(target=option_worker, args=([i]))
    t.start()
t = threading.Thread(target=stock_worker)
t.start()

print('started')
