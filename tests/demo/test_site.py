import unittest
from gmobin.demo.site import DemoOrderPage
import time
import json
import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger("gmobin")

class TestDemoOrderPage(unittest.TestCase):
    logger.parent.setLevel(logging.INFO)
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    logger.parent.addHandler(stream_handler)
    logger.debug("logger conf complete!")

    with open("conf/app.json") as f:
        df = json.load(f)
        print(df)
        chrome_path = df["chrome_path"]
        chromedriver_path = df["chromedriver_path"]
        if df["is_headless"]  == "True":
            is_headless = True
        else:
            is_headless = False

    def test_browser_start_close(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.test_browser_start_close]
        """
        page = DemoOrderPage(chrome_path=self.chrome_path, chromedriver_path=self.chromedriver_path, is_headless=self.is_headless)
        time.sleep(10)
        page.reload()
        time.sleep(5)
        page.close()

    def trading_name(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.trading_name]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.trading_name)
        page.close()
        
    def move_to_prev_round(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.move_to_prev_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        for i in range(5):
            page.move_to_prev_round
            time.sleep(5)
        page.close()

    def move_to_next_round(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.move_to_next_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        for i in range(5):
            page.move_to_next_round
            time.sleep(5)
        page.close()

    def move_to_initial_round(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.move_to_initial_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.move_to_initial_round
        time.sleep(5)
        page.close()
        
    def move_to_last_round(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.move_to_last_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.move_to_last_round
        time.sleep(5)
        page.close()

    def change_trading(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.change_trading]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        # jp -> jp
        page.transition_trading(trading_name="jp")
        self.assertEqual(page.trading_name, "jp")

        # jp -> us
        page.transition_trading(trading_name="us")
        self.assertEqual(page.trading_name, "us")

        # us -> us
        page.transition_trading(trading_name="us")
        self.assertEqual(page.trading_name, "us")

        # us -> jp
        page.transition_trading(trading_name="jp")
        self.assertEqual(page.trading_name, "jp")

        page.close

    def round_list(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.round_list
        time.sleep(5)
        page.close()

    def round_list(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.round_list
        time.sleep(5)
        page.close()
        
    def all_round_list(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.all_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.all_round_list
        time.sleep(5)
        page.close()
        
    def accept_round_list(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.accept_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        for i in range(5):
            page.accept_round_list
            time.sleep(5)
        page.close()

    def accept_and_endaccept_round_list(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.accept_and_endaccept_round_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        for i in range(5):
            page.accept_and_endaccept_round_list
            time.sleep(5)
        page.close()
        
    def move_round(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.move_round]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.move_round(round_open_time='21:00')
        time.sleep(5)
        page.move_round(round_open_time='01:00')
        time.sleep(5)
        page.move_round(round_open_time='11:00')
        time.sleep(5)
        page.close()

    def round(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.round]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.round
        page.close()
        
    def stock_price(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.stock_price]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.stock_price)
        page.close()
        
    def order_info(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.order_info]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.order_info)
        page.close()
        
    def condition_list(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.condition_list]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.condition_list)
        page.close()
        
    def condition(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.condition]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.condition)
        page.close()
        
    def transion_condition(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.transion_condition]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.transion_condition(value="2"))
        time.sleep(10)
        page.close()
        
    def condition_info(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.condition_info]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        print(page.condition_info)
        page.close()

    def websocket_log(self):
        """[python -m unittest tests.demo.test_site.TestDemoOrderPage.websocket_log]
        """
        page = DemoOrderPage(binary_location=self.binary_location, executable_path=self.executable_path, is_headless=self.is_headless)
        page.websocket_log
        page.close()

if __name__ == "__main__":
    unittest.main()