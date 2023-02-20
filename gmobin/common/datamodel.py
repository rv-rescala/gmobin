from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
import datetime

@dataclass_json
@dataclass(frozen=True, eq=True)
class StockPrice:
    time: str
    openPrice: str
    highPrice: str
    lowPrice: str
    closePrice: str

@dataclass_json
@dataclass(frozen=True, eq=True)
class Order:
    buy: str
    sell: str
    payout_price: str

@dataclass_json
@dataclass(frozen=True, eq=True)
class OrderInfo:
    put: Order
    call: Order
    
@dataclass_json
@dataclass(frozen=True, eq=True)
class Condition:
	target_price: str
	selector_value: str
 
@dataclass_json
@dataclass(frozen=True, eq=True)
class ConditionList:
	conditions: List[Condition]
 
@dataclass_json
@dataclass(frozen=True, eq=True)
class RoundListElem:
    status: str
    sub_status: str
    round_open_time: str
    round_end_time: str
 
@dataclass_json
@dataclass(frozen=True, eq=True)
class ConditionInfo:
    trading_name: str
    timestamp: str
    round_date: str
    round: RoundListElem
    condition: Condition
    order_info: OrderInfo
    
    
@dataclass_json
@dataclass(frozen=True, eq=True)
class RoundInfo:
    trading_name: str
    timestamp: str
    round_date: str
    round: RoundListElem
    condition_infos: List[ConditionInfo]
    stock_price: StockPrice

@dataclass_json
@dataclass(frozen=True, eq=True)
class AllRoundInfo:
    round_infos: List[RoundInfo]