# Python量化交易实战：从零开始构建交易策略

## 🎯 学习目标

通过本次分享，您将学会：
- ✅ 搭建量化交易研究环境
- ✅ 获取和处理金融市场数据
- ✅ 使用NumPy和Pandas进行数据分析
- ✅ 实现双均线策略的完整案例


## 1. 量化交易概述

### 什么是量化交易？
- **定义**：利用数学模型和计算机程序进行投资决策的交易方式
- **核心优势**：
  - 消除情绪干扰
  - 提高执行效率
  - 风险控制精确
  - 可回测验证

---

## 2. 环境搭建实战

### 2.1 VeighNa框架介绍

**VeighNa (vnpy)** - 基于Python的开源量化交易平台开发框架

#### 核心特性
- 📈 完整的交易系统架构
- 🔌 多交易所接口支持
- 📊 内置回测引擎
- 🎯 策略开发框架

### 2.2 Mac环境安装步骤

```bash
# 1. 下载最新版本
从 https://github.com/vnpy/vnpy/releases 下载

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装核心扩展包
pip install vnpy_ctabacktester vnpy_datamanager vnpy_ctastrategy vnpy_sqlite

# 4. 安装CTP网关（可选）
git clone git@github.com:vnpy/vnpy_ctp.git
cd vnpy_ctp && pip install .

# 5. 启动程序
python examples/veighna_trader/run.py
```

### 2.3 Jupyter环境配置

#### 什么是Jupyter？
**Jupyter** 是交互式计算环境，特别适合数据科学和量化研究。

**核心优势：**
- 🔄 **交互式编程**：代码分块执行，即时查看结果
- 📝 **文档混合**：代码、图表、说明文档一体化
- 📊 **可视化友好**：图表直接在页面显示

```bash
# 安装 JupyterLab 和 Matplotlib
pip install jupyterlab matplotlib

# JupyterLab：现代化的Jupyter界面，功能更强大
# Matplotlib：Python最基础的绘图库，用于数据可视化

# 启动 JupyterLab
jupyter lab
# 会在浏览器打开 http://localhost:8888

# 测试Python环境
print("hello world")

# 测试matplotlib绘图功能
import matplotlib.pyplot as plt
plt.plot(range(10))
# 绘制一个简单的折线图，x轴为0-9，y轴为对应的值
```

#### 常用魔法命令
```python
# 运行外部脚本
%run script.py

# 查看变量
%who

# 显示所有魔法命令的详细文档和用法说明
%magic

# 显示命令历史
%hist
```

---

## 3. 数据获取与处理

### 3.1 币安API数据获取
https://developers.binance.com/docs/zh-CN/binance-spot-api-docs/rest-api/general-api-information


#### API基础使用
```python
import requests
from datetime import datetime
from pytz import timezone

# 基础配置
base = "https://api.binance.com"
CHINA_TZ = timezone("Asia/Shanghai")

# 获取服务器时间
def get_server_time():
    url = base + "/api/v3/time"
    response = requests.get(url)
    return response.json()

# 获取最优挂单
def get_best_price(symbol="BTCUSDT"):
    url = base + "/api/v3/ticker/bookTicker"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    return response.json()

# symbol：交易对标识，这里是 BTCUSDT，表示比特币与泰达币的交易对。
# bidPrice：买一价，即当前市场上愿意买入比特币的最高价格，为 109359.99 泰达币。
# bidQty：买一价对应的挂单数量，即有 4.51191 个比特币在买一价（109359.99 泰达币）处挂单等待成交。
# askPrice：卖一价，即当前市场上愿意卖出比特币的最低价格，为 109360.00 泰达币。
# askQty：卖一价对应的挂单数量，即有 8.80970 个比特币在卖一价（109360.00 泰达币）处挂单等待成交。
```

#### 实时行情监控
```python
from time import sleep

def monitor_price(symbol="BTCUSDT"):
    """实时监控价格变化"""
    url = base + "/api/v3/ticker/bookTicker"
    params = {"symbol": symbol}
    
    while True:
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            print(f"{symbol}: 买价{data['bidPrice']}, 卖价{data['askPrice']}")
            sleep(1)
        except Exception as e:
            print(f"获取数据出错: {e}")
            sleep(1)
```

### 3.2 K线数据下载

#### 单次数据获取
```python
from vnpy.trader.object import BarData
from vnpy.trader.constant import Exchange, Interval

def download_binance_minute_data(symbol: str):
    """下载币安分钟K线数据"""
    url = base + "/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1m"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    bar_data = []
    for item in data:
        dt = datetime.fromtimestamp(item[0]/1000)
        bar = BarData(
            symbol=symbol,
            exchange=Exchange.BINANCE,
            datetime=CHINA_TZ.localize(dt),
            interval=Interval.MINUTE,
            open_price=float(item[1]),
            high_price=float(item[2]),
            low_price=float(item[3]),
            close_price=float(item[4]),
            volume=float(item[5]),
            gateway_name="BINANCE"
        )
        bar_data.append(bar)
    
    return bar_data


# 测试一下结果
bar_data = download_binance_minute_data("BTCUSDT")
bar_data[0]

# 转换DataFrame
import pandas as pd
df1 = pd.DataFrame.from_records([bar.__dict__ for bar in bar_data])

# 保存到csv文件
df1.to_csv("demo.csv")
df2 = pd.DataFrame.from_records([{"close": bar.close_price} for bar in bar_data])
df2.to_csv("BTC_close.csv")

```

#### 分段下载历史数据
```python
def download_historical_data(symbol: str, start: str, end: str):
    """分段下载历史数据，避免API限制"""
    start_dt = datetime.strptime(start, "%Y%m%d")
    start_dt = CHINA_TZ.localize(start_dt)
    
    end_dt = datetime.strptime(end, "%Y%m%d")
    end_dt = CHINA_TZ.localize(end_dt)
    
    all_bars = {}  # 使用字典去重
    
    while start_dt < end_dt:
        params = {
            "symbol": symbol,
            "interval": "1m",
            "startTime": int(start_dt.timestamp() * 1000),
            "limit": 1000
        }
        
        response = requests.get(base + "/api/v3/klines", params=params)
        data = response.json()
        
        if not data:
            break
            
        for item in data:
            dt = datetime.fromtimestamp(item[0]/1000)
            dt = CHINA_TZ.localize(dt)
            
            if dt > end_dt:
                break
                
            bar = BarData(
                symbol=symbol,
                exchange=Exchange.BINANCE,
                datetime=dt,
                interval=Interval.MINUTE,
                open_price=float(item[1]),
                high_price=float(item[2]),
                low_price=float(item[3]),
                close_price=float(item[4]),
                volume=float(item[5]),
                gateway_name="BINANCE"
            )
            all_bars[dt] = bar
        
        start_dt = dt
    
    # 按时间排序返回
    sorted_times = sorted(all_bars.keys())
    return [all_bars[dt] for dt in sorted_times]


bar_data = download_historical_data("BTCUSDT", "20250801", "20250810")
bar_data[0]
bar_data[-1]
```

---

## 4. 数据分析工具

### 4.1 NumPy基础

#### 为什么使用NumPy？
- ⚡ **高性能**：C语言实现的底层运算
- 🔢 **向量化操作**：批量处理数据
- 📊 **多维数组支持**

```python
import numpy as np

# 创建数组
prices = np.array([100, 102, 98, 105, 103])

# 向量化运算 - 计算收益率
# 收益率定义: 衡量价格变化的百分比，公式为 (今日价格 - 昨日价格) / 昨日价格
# 计算步骤:
# 1. prices[1:] 获取从第2天开始的价格: [102, 98, 105, 103]
# 2. prices[:-1] 获取从第1天到倒数第2天的价格: [100, 102, 98, 105]
# 3. 计算每日收益率: (今日价格 - 昨日价格) / 昨日价格
returns = (prices[1:] - prices[:-1]) / prices[:-1]
print(f"收益率: {returns}")

# 统计指标
# 均值 (Mean): 所有收益率的算术平均值，衡量平均盈利能力
# 计算公式: (r1 + r2 + ... + rn) / n
# 计算步骤:
# 1. 将所有收益率相加: 0.02 + (-0.0392) + 0.0714 + (-0.0190) = 0.0332
# 2. 除以收益率个数: 0.0332 / 4 = 0.0083
print(f"均值: {np.mean(returns):.4f}")

# 标准差 (Standard Deviation): 收益率波动性的度量，数值越大风险越高
# 计算公式: sqrt(sum((ri - mean)^2) / n)
# 计算步骤:
# 1. 计算每个收益率与均值的差值: [0.02-0.0083, -0.0392-0.0083, 0.0714-0.0083, -0.0190-0.0083]
# 2. 将差值平方: [0.0001, 0.0023, 0.0040, 0.0007]
# 3. 求平方和并除以个数: (0.0001+0.0023+0.0040+0.0007)/4 = 0.0018
# 4. 开平方根: sqrt(0.0018) = 0.0424
print(f"标准差: {np.std(returns):.4f}")

# 最大值 (Maximum): 期间内单日最大收益率，了解最佳表现
# 计算公式: max(r1, r2, ..., rn)
# 计算步骤:
# 1. 比较所有收益率: [0.02, -0.0392, 0.0714, -0.0190]
# 2. 找出最大值: 0.0714 (7.14%)
print(f"最大值: {np.max(returns):.4f}")
```

#### 移动平均计算
```python
def moving_average(data: list, window: int):
    """
    计算移动平均线 (Moving Average, MA)
    
    定义: 移动平均线是技术分析中最常用的指标之一，通过计算一定周期内价格的平均值来平滑价格波动
    
    计算公式: MA(n) = (P1 + P2 + ... + Pn) / n
    其中: n为周期长度，P为价格数据
    
    计算步骤:
    1. 确定移动窗口大小 (如5日、10日、20日)
    2. 从第n天开始，取前n天的价格数据
    3. 计算这n天价格的平均值
    4. 移动一天，重复步骤2-3，直到数据结束
    5. 前面不足n天的位置用0填充
    """
    ma = [0] * (window - 1)  # 前面填充0，因为前n-1天无法计算n日移动平均
    
    for i in range(len(data) - window + 1):
        # 获取当前窗口的数据: 从第i天开始的连续window天数据
        window_data = data[i:i + window]
        # 计算平均值: 窗口内所有价格之和除以窗口大小
        ma.append(sum(window_data) / window)
    
    return ma

# 示例使用
prices = [100, 102, 98, 105, 103, 107, 104, 108, 106, 110]
ma5 = moving_average(prices, 5)   # 5日移动平均
ma10 = moving_average(prices, 10) # 10日移动平均

# 计算示例说明 (以5日移动平均为例):
# 第1-4天: 无法计算5日平均，填充0
# 第5天: (100+102+98+105+103)/5 = 508/5 = 101.6
# 第6天: (102+98+105+103+107)/5 = 515/5 = 103.0
# 第7天: (98+105+103+107+104)/5 = 517/5 = 103.4
# 以此类推...
```

### 4.2 Pandas数据处理

#### Series和DataFrame基础
```python
import pandas as pd

# Series创建
prices_series = pd.Series([100, 102, 98, 105], 
                         index=['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'])

# DataFrame创建
data = {
    'open': [100, 102, 98, 105],
    'high': [103, 104, 101, 108],
    'low': [99, 101, 96, 104],
    'close': [102, 98, 105, 103],
    'volume': [1000, 1200, 800, 1500]
}
df = pd.DataFrame(data)
```

#### 常用统计指标
```python
# 基础统计 - 对价格数据的统计
print(f"数据量: {df.count()}")

# 价格均值 (Mean): 所有收盘价的算术平均值
# 计算公式: (P1 + P2 + ... + Pn) / n
# 计算步骤: 将所有价格相加，然后除以价格个数
print(f"价格均值: {df['close'].mean():.2f}")  # 收盘价的平均值，单位：价格

# 价格中位数 (Median): 将所有价格排序后，位于中间位置的值
# 计算步骤: 
# 1. 将价格从小到大排序
# 2. 如果数据个数为奇数，取中间值
# 3. 如果数据个数为偶数，取中间两个值的平均值
print(f"价格中位数: {df['close'].median():.2f}")  # 收盘价的中位数

# 价格标准差 (Standard Deviation): 衡量价格波动性的指标
# 计算公式: sqrt(sum((Pi - mean)^2) / n)
# 计算步骤:
# 1. 计算每个价格与均值的差值
# 2. 将差值平方
# 3. 求平方和的平均值
# 4. 开平方根
print(f"价格标准差: {df['close'].std():.2f}")  # 收盘价的标准差

# 收益率计算
df['returns'] = df['close'].pct_change()  # 计算日收益率

# 收益率统计 - 对收益率数据的统计
# 收益率均值: 所有收益率的算术平均值，衡量平均盈利能力
# 计算公式: (r1 + r2 + ... + rn) / n
# 计算步骤: 将所有收益率相加，然后除以收益率个数
print(f"收益率均值: {df['returns'].mean():.4f}")  # 平均收益率，单位：百分比

# 收益率标准差: 衡量收益率波动性的指标，数值越大风险越高
# 计算公式: sqrt(sum((ri - mean)^2) / n)
# 计算步骤:
# 1. 计算每个收益率与均值的差值
# 2. 将差值平方
# 3. 求平方和的平均值
# 4. 开平方根
print(f"收益率标准差: {df['returns'].std():.4f}")  # 收益率波动性

# 收益率最大值: 期间内单日最大收益率
# 计算步骤: 比较所有收益率，找出最大值
print(f"收益率最大值: {df['returns'].max():.4f}")  # 最大单日收益率

# 汇总描述
print(df['returns'].describe())

# 极值索引
max_idx = df['returns'].idxmax()
min_idx = df['returns'].idxmin()
print(f"最大收益日: {max_idx}, 最小收益日: {min_idx}")
```

---

## 5. 策略开发与回测

### 5.1 双均线策略

#### 策略定义与逻辑
**双均线策略**：通过比较两条不同周期的移动平均线来生成交易信号

- **短期均线**：周期较短的移动平均线（如ma10，10日移动平均）
- **长期均线**：周期较长的移动平均线（如ma20，20日移动平均）

**交易信号**：
- 📈 **买入信号（金叉）**：短期均线上穿长期均线（ma10 > ma20，且前一日ma10 ≤ ma20）
- 📉 **卖出信号（死叉）**：短期均线下穿长期均线（ma10 < ma20，且前一日ma10 ≥ ma20）

**技术分析术语**：
- **金叉**：短期均线从下方穿越长期均线，通常表示上涨趋势开始
- **死叉**：短期均线从上方穿越长期均线，通常表示下跌趋势开始

**策略原理**：
- 当短期均线在长期均线之上时，表示短期趋势向上，适合买入
- 当短期均线在长期均线之下时，表示短期趋势向下，适合卖出

```python
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_tool import download_binance_minute_data, moving_average

def dual_moving_average_strategy(symbol: str, start_date: str, end_date: str, 
                                short_window: int = 10, long_window: int = 20, 
                                capital: float = 1000000):
    """双均线策略实现"""
    
    # 1. 下载数据
    print(f"正在下载 {symbol} 从 {start_date} 到 {end_date} 的数据...")
    bar_data = download_binance_minute_data(symbol, start_date, end_date)
    
    # 2. 转换为DataFrame
    df = pd.DataFrame.from_records([bar.__dict__ for bar in bar_data])
    df.index = df["datetime"]
    
    # 3. 提取收盘价
    close_prices = df["close_price"].tolist()
    
    # 4. 计算移动平均线
    df["ma_short"] = moving_average(close_prices, short_window)
    df["ma_long"] = moving_average(close_prices, long_window)
    
    # 5. 生成交易信号
    df["signal"] = 0  # 0: 无信号, 1: 买入, -1: 卖出
    
    for i in range(1, len(df)):
        # 金叉：短期均线上穿长期均线，买入信号
        if (df.iloc[i]["ma_short"] > df.iloc[i]["ma_long"] and 
            df.iloc[i-1]["ma_short"] <= df.iloc[i-1]["ma_long"]):
            df.iloc[i, df.columns.get_loc("signal")] = 1
            
        # 死叉：短期均线下穿长期均线，卖出信号
        elif (df.iloc[i]["ma_short"] < df.iloc[i]["ma_long"] and 
              df.iloc[i-1]["ma_short"] >= df.iloc[i-1]["ma_long"]):
            df.iloc[i, df.columns.get_loc("signal")] = -1
    
    # 6. 计算持仓和收益
    position = 0  # 当前持仓
    positions = []  # 持仓记录
    balance = capital  # 账户余额
    balances = []  # 余额记录
    
    for i, row in df.iterrows():
        if row["signal"] == 1 and position == 0:  # 买入信号且当前无持仓
            position = balance / row["close_price"]  # 全仓买入
            balance = 0
        elif row["signal"] == -1 and position > 0:  # 卖出信号且当前有持仓
            balance = position * row["close_price"]  # 全部卖出
            position = 0
        
        positions.append(position)
        if position > 0:
            balances.append(position * row["close_price"])
        else:
            balances.append(balance)
    
    df["position"] = positions
    df["balance"] = balances
    
    # 7. 计算策略收益
    df["returns"] = df["close_price"].pct_change()
    df["strategy_returns"] = df["balance"].pct_change()
    
    # 8. 计算绩效指标
    total_return = (df["balance"].iloc[-1] - capital) / capital * 100
    buy_hold_return = (df["close_price"].iloc[-1] - df["close_price"].iloc[0]) / df["close_price"].iloc[0] * 100
    
    print(f"\n=== 双均线策略回测结果 ===")
    print(f"交易对: {symbol}")
    print(f"回测期间: {start_date} 到 {end_date}")
    print(f"短期均线: {short_window}期")
    print(f"长期均线: {long_window}期")
    print(f"初始资金: {capital:,.0f}")
    print(f"最终资金: {df['balance'].iloc[-1]:,.0f}")
    print(f"策略总收益: {total_return:.2f}%")
    print(f"买入持有收益: {buy_hold_return:.2f}%")
    print(f"超额收益: {total_return - buy_hold_return:.2f}%")
    
    return df

def plot_dual_ma_strategy(df: pd.DataFrame, symbol: str):
    """绘制双均线策略图表"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'{symbol} 双均线策略', '账户余额'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # 第一个子图：价格和均线
    fig.add_trace(
        go.Scatter(x=df.index, y=df["close_price"], name="收盘价", line=dict(color="black")),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df["ma_short"], name="短期均线", line=dict(color="red")),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df["ma_long"], name="长期均线", line=dict(color="blue")),
        row=1, col=1
    )
    
    # 标记买卖信号
    buy_signals = df[df["signal"] == 1]
    sell_signals = df[df["signal"] == -1]
    
    fig.add_trace(
        go.Scatter(x=buy_signals.index, y=buy_signals["close_price"], 
                  mode='markers', marker=dict(symbol='triangle-up', size=10, color='green'),
                  name='买入信号'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=sell_signals.index, y=sell_signals["close_price"], 
                  mode='markers', marker=dict(symbol='triangle-down', size=10, color='red'),
                  name='卖出信号'),
        row=1, col=1
    )
    
    # 第二个子图：账户余额
    fig.add_trace(
        go.Scatter(x=df.index, y=df["balance"], name="账户余额", line=dict(color="purple")),
        row=2, col=1
    )
    
    fig.update_layout(
        title=f"{symbol} 双均线策略回测结果",
        xaxis_title="时间",
        height=800,
        showlegend=True
    )
    
    fig.show()



# 参数设置
symbol = "BTCUSDT"
start_date = "20250801"
end_date = "20250810"
short_window = 10  # 短期均线周期
long_window = 20   # 长期均线周期
initial_capital = 1000000  # 初始资金

# 执行策略
df_result = dual_moving_average_strategy(
    symbol=symbol,
    start_date=start_date,
    end_date=end_date,
    short_window=short_window,
    long_window=long_window,
    capital=initial_capital
)

# 绘制图表
plot_dual_ma_strategy(df_result, symbol)

# 显示交易信号统计
signal_counts = df_result["signal"].value_counts()
print(f"\n=== 交易信号统计 ===")
print(f"买入信号次数: {signal_counts.get(1, 0)}")
print(f"卖出信号次数: {signal_counts.get(-1, 0)}")
print(f"无信号次数: {signal_counts.get(0, 0)}")
   
```


**感谢大家的聆听！**  
**祝愿大家在量化交易的道路上收获满满！** 🚀📈
