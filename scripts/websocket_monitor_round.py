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

parser = argparse.ArgumentParser(description="cats gmo")

# args params
parser.add_argument('-cf', '--config', help="configuration file", required=True)
parser.add_argument('-t', '--target', help="target", required=True)
parser.add_argument('-r', '--round_open_time', help="round_open_time", required=True)
parser.add_argument('-out', '--out', help="out", required=True)
parser.add_argument('-log', '--log', help="log", required=True)
args = parser.parse_args()
round_open_time = args.round_open_time
output_path = f"{args.out}/{get_today_date()}"
target = args.target
print(args)

logger.init_from_json(args.log)
logger.info("catsgmo webscoket monitor start")

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

# init
page = DemoOrderPage(binary_location=binary_location, executable_path=executable_path, is_headless=is_headless)

# move change_trading
page.change_trading(trading_name=target)

# move round
page.move_round(round_open_time=round_open_time)

# data
price_csv = ','.join(list(map(lambda x: x.target_price.split(" ")[1].replace(",",""), page.condition_list.conditions)))
print(price_csv)

round = page.round
date = get_today_date()
round_file_path = f"{output_path}/{gethostname()}_{target}_{round.round_open_time.replace(':','')}_{get_current_time()}_websocket_monitor_round.csv"
logger.info(f"round_file_path is {round_file_path}.")

with open(round_file_path, mode="w") as f:
    header = "date,round_open_time,round_end_time,a,b,c,d,e,f,g,data\n"
    f.write(header)
    try:
        while True:
            round_status = page.round.status
            for wl in page.websocket_log:
                f.write(f"{date},{round.round_open_time},{round.round_end_time},{price_csv},{str(wl)}\n")
                f.flush()
            if round_status == "END_TRADE":
                logger.info("close")
                break
            time.sleep(10)
    except:
        logger.error(f"websocket_monitor_round {round_file_path}. {sys.exc_info()}")

page.close()

