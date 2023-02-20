from datetime import datetime as dt
import sys
import re
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from gmobin.common.datamodel import *
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from logging import getLogger
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import requests
from gmobin.common.tool import *
from selenium.webdriver.chrome.options import Options
import json

logger = getLogger(__name__)

class DemoOrderPageInitPageError(RuntimeError):
    pass

class DemoOrderPageTransitionFailedError(RuntimeError):
    pass

class DemoOrderPageDataConsistencyError(RuntimeError):
    pass

class DemoOrderPage:
    url = "https://demo.click-sec.com/ixop/order.do"

    def __init__(self, chrome_path: str, chromedriver_path: str, is_headless: bool):
            """_summary_

            Args:
                chrome_path (str): _description_
                chromedriver_path (str): _description_
                is_headless (bool): _description_
            """
            logger.info(f"init by chrome_path: {chrome_path}, chromedriver_path: {chromedriver_path}, is_headless: {is_headless}")
            options = Options()
            options.binary_location = chrome_path
            if is_headless:
                options.add_argument('--headless')
            # https://www.ytyng.com/blog/ubuntu-chromedriver/
            options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
            options.add_argument("start-maximized") # open Browser in maximized mode
            options.add_argument("disable-infobars") # disabling infobars
            options.add_argument("--disable-extensions") # disabling extensions
            options.add_argument("--disable-gpu") # applicable to windows os only
            options.add_argument("--no-sandbox") # Bypass OS security model
            caps = DesiredCapabilities.CHROME
            caps['loggingPrefs'] = {'performance': 'INFO'}
            options.add_experimental_option('w3c', False)
            self.driver = webdriver.Chrome(options=options, executable_path=chromedriver_path, desired_capabilities=caps)
            self.driver.implicitly_wait(5)
            self.__init_page(click_skip=True)

    def __init_page(self, click_skip: bool):
        """[ページの初期化]

        Args:
            click_skip (bool): [description]

        Returns:
            [type]: [description]
        """
        self.driver.get(self.url)
        if click_skip:
            skip_count = 0
            # Wait rendering
            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located)
            while True:
                try:
                    button = self.driver.find_elements_by_css_selector(".joyride-tooltip__button.joyride-tooltip__button--primary")[0]
                    button.click()
                    time.sleep(1)
                    skip_count = skip_count + 1
                    logger.info(f"__init_page skip_count {skip_count}")
                except:
                    logger.info(f"__init_page finish")
                    return True

    def close(self):
        """[close]
        """
        self.driver.close()
        self.driver.quit()

    def reload(self):
        logger.info("reload")
        self.driver.refresh()

    def is_open(self):
        """[ToDo: check market is open or close]
        """
        pass

    @property
    def html(self) -> BeautifulSoup:
        """[現在表示されているhtmlを取得]

        Returns:
            BeautifulSoup: [description]
        """
        html = self.driver.page_source.encode('utf-8')
        return BeautifulSoup(html, "lxml")

    @property
    def trading_name(self):
        """[現在の銘柄を取得]
        
        Returns:
            [str] -- [jp or us]
        """
        
        _name = self.html.find('button', {'class': 'currency-list-button on'}).text
        if _name == "日本225":
            name = "jp"
        elif _name == "米国30":
            name = "us"
        logger.debug(f"trading_name is {name}")
        return name

    def change_trading(self, trading_name) -> bool:
        """[銘柄を変更]
        
        Arguments:
            id {[trading_name]} -- [jp or us]
        """
        current_trading_name = self.trading_name
        if current_trading_name != trading_name: # 遷移が必要ない場合は遷移しない
            logger.info(f"Transition {current_trading_name} to {trading_name}")
            if trading_name == "us":
                id = 1
            else:
                id = 0
            button = self.driver.find_elements_by_css_selector(".currency-list-button")[id]
            button.click()
            # check
            error_count = 0
            while True:
                current_trading_name = self.trading_name
                logger.info(f"Current trading name is {current_trading_name}.")
                if trading_name == current_trading_name:
                    logger.info(f"Transition success.")
                    return True
                elif error_count == 4:
                    raise DemoOrderPageTransitionFailedError("Transition trading is failed")
                else:
                    error_count = error_count + 1
                    logger.info(f"transition_trading error count is : {error_count}")
        else:
            logger.info(f"There's no need to transition.")
            return True

    @property
    def __wait_trade_order_loading(self):
        """[trade_orderの読み込みが終わるまでwaitする]

        Returns:
            [type]: [description]
        """
        while True:
            trade_order = self.html.find('div', {'class': 'trade-order'}).get('class')
            logger.debug(trade_order)
            if len(trade_order) == 1:
                return True
            else:
                if trade_order[1] == "before":
                    return True

    @property
    def move_to_next_round(self):
        """[一つ次のラウンドリストに移動]
        """
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located)
            self.__wait_trade_order_loading
            clickable_button = self.driver.find_elements_by_css_selector(".round-list-last")[0]
            clickable_button.click()
            result = True
        except:
            logging.info(sys.exc_info())
            result = False
        return result

    @property
    def move_to_prev_round(self):
        """[一つ前のラウンドリストに移動]
        """
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located)
            self.__wait_trade_order_loading
            clickable_button = self.driver.find_elements_by_css_selector(".round-list-first")[0]
            clickable_button.click()
            result = True
        except:
            result = False
        return result

    @property
    def move_to_initial_round(self):
        """[初回のラウンドリストに移動]
        """
        move_count = 0
        while True:
            r = self.move_to_prev_round
            if not r:
                break
            move_count = move_count + 1
            logger.info(f"move_to_initial_round_list move count is {move_count}")
        return move_count

    @property
    def move_to_last_round(self):
        """[最終のラウンドリストに移動]
        """
        move_count = 0
        while True:
            r = self.move_to_next_round
            if not r:
                break
            move_count = move_count + 1
            logger.info(f"move_to_last_round_list move count is {move_count}")
        return move_count

    def __parse_round_list(self, round_list) -> RoundListElem:
        status = round_list[0][1]
        if len(round_list[0]) == 3:
            sub_status = round_list[0][2]
        else:
            sub_status = None
        open_end_time = round_list[1].find('span').text.split("-")
        round_open_time = open_end_time[0]
        round_end_time = open_end_time[1]
        r = RoundListElem(status=status, sub_status=sub_status, round_open_time=round_open_time, round_end_time=round_end_time)
        return r

    @property
    def all_round_list(self) -> List[RoundListElem]:
        """[全てのラウンド一覧を取得]

        Returns:
            [type] -- [description]
        """
        # move to initail round list
        self.move_to_initial_round_list
        _round_list = []
        while True:
            buttons = self.html.find('div', {'class': 'round-list'}).findAll('button')
            _round_list.extend(list(filter(lambda x: x[0][0] == 'round-list-button', map(lambda x: (x.get("class"), x), buttons))))
            if not self.move_to_next_round_list:
                break
        round_list = set(list(map(lambda x: self.__parse_round_list(x), _round_list)))
        logger.info(f"round_list: {round_list}")
        return round_list

    @property
    def round_list(self) -> List[RoundListElem]:
        """[現在表示されているラウンド一覧を取得]

        Returns:
            [type] -- [description]
        """
        # move to initail round list
        buttons = self.html.find('div', {'class': 'round-list'}).findAll('button')
        _round_list = list(filter(lambda x: x[0][0] == 'round-list-button', map(lambda x: (x.get("class"), x), buttons)))
        round_list = set(list(map(lambda x: self.__parse_round_list(x), _round_list)))
        logger.debug(f"round_list: {round_list}")
        return round_list

    @property
    def accept_round_list(self):
        """[Acceptステータスのラウンド一覧を取得]

        Returns:
            [type] -- [description]
        """
        accept_round_list = list(filter(lambda x: (x.status == 'ACCEPT'), self.round_list))
        # or END_ACCEPT
        logger.debug(f"accept_round_list is {accept_round_list}")
        return accept_round_list
    
    @property
    def accept_and_endaccept_round_list(self):
        """[Accept/END_ACCEPTステータスのラウンド一覧を取得]
        
        Returns:
            [type] -- [description]
        """
        accept_round_list = list(filter(lambda x: (x.status== 'ACCEPT') or (x.status == 'END_ACCEPT'), self.round_list))
        logger.debug(f"accept_and_endaccept_round_list is {accept_round_list}")
        return accept_round_list
    
    @property
    def round(self):
        """[現在のラウンドを取得]
        """
        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located)
        self.__wait_trade_order_loading
        round = list(filter(lambda x: (x.sub_status == 'on'), self.round_list))
        if len(round) != 1:
            raise RuntimeError(f"round: current round len are {round}")
        else:
            logging.debug(f"round: {round[0]}")
            return round[0]

    def move_round(self, round_open_time):
        """[特定のラウンドに移動]
        
        Arguments:
            round_open_time {[type]} -- [hh:00]
        """
        if self.round.round_open_time == round_open_time:
            logger.info("Need not to move round.")
            return True
        elif round_open_time == "01:00":
            self.move_to_last_round
            logger.info("Move to last round.")
            return True
        while True:
            if self.round.round_open_time == round_open_time:
                return True
            if self.round.round_open_time == "01:00":
                move_result = self.move_to_prev_round
            elif self.round.round_open_time < round_open_time:
                move_result = self.move_to_next_round
            else:
                move_result = self.move_to_prev_round
            if not move_result:
                raise DemoOrderPageTransitionFailedError("Transiition faild")

    @classmethod
    def stock_price(cls, trading_name) -> StockPrice:
        """[現在の株価情報を取得]

        Returns:
            [type] -- [description]
        """
        if trading_name == "jp":
            stock_price_url = "https://demo.click-sec.com/boquote/api/v3/chart?underlierCd=000001&count=1&type=MIN_1"
        elif trading_name == "us":
            stock_price_url = "https://demo.click-sec.com/boquote/api/v3/chart?underlierCd=000002&count=1&type=MIN_1"
        ret = requests.get(stock_price_url)
        soup = BeautifulSoup(ret.content, features="html.parser")
        c = json.loads(str(soup))[0]
        result = StockPrice(
            time=c["time"],
            openPrice=c["open"],
            highPrice=c["high"],
            lowPrice=c["low"],
            closePrice=c["close"])
        logger.debug(f"stock_price: {result}")
        return result

    @property
    def order_info(self) -> OrderInfo:
        """[オーダ情報を取得]
        
        Returns:
            [type] -- [description]
        """
        def __parse_oder_panel(order_panel) -> Order:
            buy = order_panel.find('span', {'class': 'order-buy-price'}).text
            sell = order_panel.find('span', {'class': 'order-sell-price'}).text
            payout_price = order_panel.find('span', {'class': 'order-payout-price'}).text
            return Order(buy=buy, sell=sell, payout_price=payout_price)

        trade_panel = self.html.find('div', {'class': 'trade-panel'})
        panel_put = __parse_oder_panel(trade_panel.find('div', {'class': 'panel-put'}))
        panel_call = __parse_oder_panel(trade_panel.find('div', {'class': 'panel-call'}))
        r = OrderInfo(put=panel_put, call=panel_call)
        logging.debug(f"order_info: {r}")
        return r

    @property
    def condition_list(self) -> ConditionList:
        """[権利行使価格一覧を取得]
        """
        target_selector = self.html.find('select', {'class': 'select-strike-price'})
        result = ConditionList(conditions=list(map(lambda selector: Condition(target_price=selector.text, selector_value=selector["value"]), target_selector)))
        logger.debug(f"condition_list: {result}")
        return result

    @property
    def condition(self) -> Condition:
        selectable_selector = Select(self.driver.find_element_by_class_name('select-strike-price'))
        result = Condition(target_price=selectable_selector.first_selected_option.text, selector_value=selectable_selector.first_selected_option.get_property("value"))
        logger.debug(f"condition: {result}")
        return result

    def transion_condition(self, value: str):
        """[summary]
        
        Arguments:
            value {[str]} -- [From 1 to 7]
        """
        before_value = self.condition.selector_value
        if before_value != value:
            logger.debug("transion_condition")
            selectable_selector = Select(self.driver.find_element_by_class_name('select-strike-price'))
            selectable_selector.select_by_value(value) # select pulldown
        # check
        for i in range(4):
            current_value = self.condition.selector_value
            if value == current_value:
                logger.debug(f"transion_condition: {before_value} to {current_value}")
                return True
            else:
                logger.info(f"transion_condition: error count is {i}")
        raise DemoOrderPageTransitionFailedError("transion_condition is failed")

    @property
    def condition_info(self) -> ConditionInfo:
        r =  ConditionInfo(trading_name=self.trading_name, timestamp=get_current_time(), round_date=get_today_date(), round=self.round, condition=self.condition, order_info=self.order_info)
        logger.debug(f"condition_info result: {r}")
        return r

    @property
    def websocket_log(self):
        result = []
        for entry in self.driver.get_log('performance'):
            j = json.loads(entry['message'])["message"]
            if j["method"] == "Network.webSocketFrameReceived":
                result.append(j["params"]["response"]["payloadData"])
        return result