# 加载模块
import requests
from pytz import timezone
from datetime import datetime

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData
import pandas as pd

# 开始K线查询函数
CHINA_TZ = timezone("Asia/Shanghai")


def download_binance_minute_data(symbol: str, start: str, end: str):
    """基于代码和交易所下载数据"""
    base = "https://api.binance.com"
    endpoint = "/api/v3/klines"
    url = base + endpoint

    # 开始和结束时间
    start_dt = datetime.strptime(start, "%Y%m%d")
    start_dt = CHINA_TZ.localize(start_dt)

    end_dt = datetime.strptime(end, "%Y%m%d")
    end_dt = CHINA_TZ.localize(end_dt)

    # 查询缓存变量
    bar_data = {}  # 使用字典对时间戳去重
    finished = False  # 查询结束

    # 持续循环
    while True:
        # 执行REST数据查询
        params = {
            "symbol": symbol,
            "interval": "1m",
            "startTime": int(start_dt.timestamp() * 1000),
            "limit": 1000,
        }
        r = requests.get(url, params=params)
        data = r.json()

        # 如果有返回的数据，则进行处理
        if data:
            for l in data:
                # 生成时间戳
                dt = datetime.fromtimestamp(l[0] / 1000)
                dt = CHINA_TZ.localize(dt)

                # 检查是否已经超出结束时间，若超出则说明已经完成
                if dt > end_dt:
                    finished = True  # 标识完成状态
                    break  # 退出for循环

                # 解析K线数据
                bar = BarData(
                    symbol=symbol,
                    exchange=Exchange.BINANCE,
                    datetime=dt,
                    interval=Interval.MINUTE,
                    open_price=float(l[1]),
                    high_price=float(l[2]),
                    low_price=float(l[3]),
                    close_price=float(l[4]),
                    volume=float(l[5]),
                    gateway_name="BINANCE",
                )
                bar_data[bar.datetime] = bar

                # 打印本轮查询范围
            # print(start_dt, bar.datetime)

            # 将本轮的结束时间戳，作为新一轮的开始时间
            start_dt = bar.datetime
        # 否则说明已经结束
        else:
            finished = True

        # 结束则退出while循环
        if finished:
            break

    # 对时间戳排序
    dts = list(bar_data.keys())
    dts.sort()

    # 然后以列表形式返回
    return [bar_data[dt] for dt in dts]


def download_data(symbol: str, exchange: str) -> pd.DataFrame:
    """下载数据"""
    exchange = exchange.upper()
    if exchange == Exchange.BINANCE.value:
        bars = download_binance_minute_data(symbol, "20250801", "20250810")
        df = pd.DataFrame.from_records([bar.__dict__ for bar in bars])
        df.index = df["datetime"]
        return df
    else:
        raise ValueError(f"不支持的交易所: {exchange}")
    
def moving_average(data: list, window: int):
    """计算移动平均值"""
    # 最前面的window窗口数据无法计算
    ma = [0 for i in range(window - 1)]
    
    # 滚动求和，然后除以窗口得到均值
    for start_ix in range(len(data) - (window - 1)):
        end_ix = start_ix + window
        value = sum(data[start_ix:end_ix]) / window
        ma.append(value)
    
    return ma