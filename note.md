
# 01-搭建量化研究环境

## [vnpy](https://www.vnpy.com/):基于Python的开源量化交易平台开发框架

## mac安装

```bash
# 下载最新的[release版本](https://github.com/vnpy/vnpy/releases)
# 从GitHub releases页面下载最新的vnpy发布版本，确保获取最新的功能和bug修复

#  创建虚拟环境
python -m venv venv
# 使用Python的venv模块创建一个名为venv的虚拟环境
# 虚拟环境可以隔离项目依赖，避免与系统Python包冲突

#  激活虚拟环境
source venv/bin/activate
# 激活虚拟环境，命令行前面会出现(venv)标识
# 激活后，pip安装的包都会安装到虚拟环境中

#  安装 VeighNa 扩展包
pip install vnpy_ctabacktester vnpy_datamanager vnpy_ctastrategy vnpy_sqlite
# 安装vnpy的核心扩展包：
# - vnpy_ctabacktester: CTA策略回测引擎
# - vnpy_datamanager: 数据管理模块
# - vnpy_ctastrategy: CTA策略模块
# - vnpy_sqlite: SQLite数据库支持

# 克隆 vnpy_ctp
git clone git@github.com:vnpy/vnpy_ctp.git
# 从GitHub克隆CTP网关模块，用于连接中国期货市场

#  安装 CTP 网关
cd vnpy_ctp && pip install .
# 进入vnpy_ctp目录并安装CTP网关模块
# 这会编译并安装CTP相关的C++扩展

# 运行程序
cd .. && python examples/veighna_trader/run.py
# 返回上级目录并运行vnpy交易程序示例
# 这会启动vnpy的图形化交易界面
```


# Jupyter是什么？

**Jupyter** 是一个开源的交互式计算环境，特别适合数据科学、机器学习和量化交易研究。

## 主要特点

### 1. 交互式编程
- 代码可以分块执行，每块代码称为一个"单元格"(cell)
- 可以单独运行某个代码块，看到即时结果
- 支持实时调试和实验

### 2. 富文本支持
- 支持Markdown格式的文档说明
- 可以插入图片、公式、表格
- 代码和文档混合展示

### 3. 数据可视化
- 直接在notebook中显示图表
- 支持matplotlib、plotly、seaborn等绘图库
- 交互式图表展示

```bash
# 安装JupyterLab（现代化的Jupyter界面）
pip install jupyterlab
# 启动JupyterLab服务器
jupyter lab

# 安装经典版Jupyter Notebook（可选）

pip install notebook
# 启动经典版Jupyter Notebook
jupyter notebook

# 安装matplotlib绘图库（用于数据可视化）
pip install matplotlib

# 测试Python环境
print("hello world")

# 测试matplotlib绘图功能
import matplotlib.pyplot as plt
plt.plot(range(10))
# 绘制一个简单的折线图，x轴为0-9，y轴为对应的值

```

## jupyter的魔法命令

Jupyter的魔法命令是以`%`开头的特殊命令，用于增强notebook的功能。

```bash
# %run - 运行Python脚本文件
%run script.py
# 在notebook中执行外部的Python脚本文件
# 脚本中定义的变量和函数会导入到当前notebook环境中

# %load - 加载外部文件内容到当前单元格
%load script.py
# 将指定文件的内容加载到当前单元格中，但不执行
# 常用于查看或编辑外部代码文件

# %quickref - 显示魔法命令的快速参考
%quickref
# 显示所有可用的魔法命令的简要说明和用法

# %magic - 显示魔法命令的详细帮助
%magic
# 显示所有魔法命令的详细文档和用法说明

# %time - 测量单行代码的执行时间
%time result = some_function()
# 显示单行代码的执行时间

# %timeit - 多次执行并测量平均执行时间
%timeit result = some_function()

# 第一个单元格：定义函数
def add(a, b):
    return a + b

# 第二个单元格：使用%timeit测试函数
%timeit add(1, 2)
26.8 ns ± 0.0598 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)

# %timeit输出结果解释：
# 26.8 ns - 平均执行时间（纳秒）
# ± 0.0598 ns - 标准差，表示执行时间的波动范围
# per loop - 每次循环的执行时间
# mean ± std. dev. of 7 runs - 基于7次运行的均值和标准差
# 10,000,000 loops each - 每次运行执行了1000万次循环

# 性能分析：
# - 26.8纳秒 = 0.0000000268秒，非常快的执行速度
# - 标准差0.0598纳秒，说明执行时间很稳定
# - 1000万次循环确保统计结果的可靠性
# - 7次运行取平均值，减少偶然误差

# %timeit执行逻辑详解：
# 1. 首先进行7次独立的测试运行
# 2. 每次运行内部执行1000万次函数调用
# 3. 记录每次运行的总时间
# 4. 计算每次运行的平均时间（总时间 ÷ 1000万）
# 5. 最后计算7次运行的平均值和标准差

# 具体计算过程：
# 运行1: 1000万次调用总时间 ÷ 1000万 = 平均时间1
# 运行2: 1000万次调用总时间 ÷ 1000万 = 平均时间2
# ...
# 运行7: 1000万次调用总时间 ÷ 1000万 = 平均时间7
# 最终结果 = (平均时间1 + 平均时间2 + ... + 平均时间7) ÷ 7

# 为什么要这样设计：
# - 1000万次循环：确保单次运行有足够的样本量
# - 7次运行：减少系统波动和偶然因素的影响
# - 双重平均：既保证了单次运行的准确性，又保证了多次运行的稳定性

# 在量化交易中的应用：
# - 用于测试策略函数的执行效率
# - 比较不同算法的性能差异
# - 优化高频交易代码的执行速度

# %hist - 显示命令历史
%hist
# 显示当前会话中执行过的命令历史记录

# %reset - 全局重置
%reset
# 删除当前命名空间中的所有变量，重置环境

# %who - 变量查看
%who
# 显示当前命名空间中定义的所有变量

# %matplotlib inline - 在notebook中内联显示matplotlib图表
%matplotlib inline
# 让matplotlib图表直接显示在notebook单元格中，而不是弹出窗口

# %pwd - 显示当前工作目录
%pwd
# 显示当前notebook的工作目录路径

# %ls - 列出当前目录的文件
%ls
# 列出当前目录下的文件和文件夹

# %cd - 切换目录
%cd /path/to/directory
# 切换到指定目录
```



# 币圈行情数据获取
```python
# 币安的API文档地址
# https://developers.binance.com/docs/zh-CN/binance-spot-api-docs/rest-api/general-api-information

# 加载模块
import requests

from datetime import datetime
from pytz import timezone
from time import sleep

from vnpy.trader.object import BarData
from vnpy.trader.constant import Exchange, Interval

# 构建访问链接
base = "https://api.binance.com"
endpoint = "/api/v3/time"
url = base + endpoint

# 获取服务器时间
r = requests.get(url)
r.json()


# 最优挂单接口 https://developers.binance.com/docs/zh-CN/binance-spot-api-docs/rest-api/market-data-endpoints#%E6%9C%80%E4%BC%98%E6%8C%82%E5%8D%95%E6%8E%A5%E5%8F%A3
endpoint = "/api/v3/ticker/bookTicker"
url = base + endpoint

# 查询参数字典
params = {"symbol": "BTCUSDT"}

# 在加密货币交易领域，像 BTCUSDT、BNBUSDT 这样的组合是交易对的表示方式，具体含义如下：

# 基础货币（Base Currency）：前面的币种 ，比如 BTCUSDT 里的 BTC（比特币）、BNBUSDT 里的 BNB（币安币）。它是交易中被衡量价值的对象。
# 报价货币（Quote Currency）：后面的币种，即 USDT（泰达币，一种稳定币，通常与美元保持 1:1 的锚定汇率 ）。
# 报价货币用于衡量基础货币的价值，表明购买一个单位的基础货币需要支付多少报价货币。

# 以 BTCUSDT 为例，如果当前市场价格是 25000，意味着购买 1 个比特币需要支付 25000 个泰达币；
# BNBUSDT 交易对的价格则反映了购买 1 个币安币所需花费的泰达币数量。通过交易对，投资者可以在加密货币交易平台上进行买卖操作 ，实现资产的配置和盈利。

# 查询最优挂单接口信息
r = requests.get(url, params=params)
r.json()

{'symbol': 'BTCUSDT',
 'bidPrice': '109359.99000000',
 'bidQty': '4.51191000',
 'askPrice': '109360.00000000',
 'askQty': '8.80970000'}

# symbol：交易对标识，这里是 BTCUSDT，表示比特币与泰达币的交易对。
# bidPrice：买一价，即当前市场上愿意买入比特币的最高价格，为 109359.99 泰达币。
# bidQty：买一价对应的挂单数量，即有 4.51191 个比特币在买一价（109359.99 泰达币）处挂单等待成交。
# askPrice：卖一价，即当前市场上愿意卖出比特币的最低价格，为 109360.00 泰达币。
# askQty：卖一价对应的挂单数量，即有 8.80970 个比特币在卖一价（109360.00 泰达币）处挂单等待成交。

# 持续轮询输出
while True:
    r = requests.get(url, params=params)
    d = r.json()

    symbol = d["symbol"]
    bp = d["bidPrice"]
    bq = d["bidQty"]
    ap = d["askPrice"]
    aq = d["askQty"]

    msg = f"{symbol}. 买价{bp}[{bq}], 卖价{ap}[{aq}]"
    print(msg)
    sleep(1)


# k线数据 https://developers.binance.com/docs/zh-CN/binance-spot-api-docs/rest-api/market-data-endpoints#k%E7%BA%BF%E6%95%B0%E6%8D%AE

# 这次来查询K线
endpoint = "/api/v3/klines"
url = base + endpoint

# 构建查询参数
params = {
    "symbol": "BTCUSDT",
    "interval": "1m"
}

# 发起K线查询请求
r = requests.get(url, params=params)
data = r.json()

# 查看数据类型
type(data)

# 查看具体数据
data[0]

[
    1499040000000,      // 开盘时间
    "0.01634790",       // 开盘价
    "0.80000000",       // 最高价
    "0.01575800",       // 最低价
    "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
    "148976.11427815",  // 成交量
    1499644799999,      // 收盘时间
    "2434.19055334",    // 成交额
    308,                // 成交笔数
    "1756.87402397",    // 主动买入成交量
    "28.46694368",      // 主动买入成交额
    "17928899.62484339" // 请忽略该参数
]

# 开放K线查询函数
CHINA_TZ = timezone("Asia/Shanghai")

def download_binance_minute_data(symbol: str):
    """基于代码和交易所下载数据"""
    base = "https://api.binance.com"
    endpoint = "/api/v3/klines"
    url = base + endpoint

    params = {
        "symbol": symbol,
        "interval": "1m"
    }

    r = requests.get(url, params=params)
    data = r.json()

    bar_data = []
    for l in data:
        dt = datetime.fromtimestamp(l[0]/1000)
        bar = BarData(
            symbol=symbol,
            exchange=Exchange.BINANCE,
            datetime=CHINA_TZ.localize(dt),
            interval=Interval.MINUTE,
            open_price=float(l[1]),
            high_price=float(l[2]),
            low_price=float(l[3]),
            close_price=float(l[4]),
            volume=float(l[5]),
            gateway_name="BINANCE"
        )
        bar_data.append(bar)
    return bar_data

# 测试一下结果
bar_data = download_binance_minute_data("BTCUSDT")
bar_data[0]

# 转换DataFrame
import pandas as pd
df = pd.DataFrame.from_records([bar.__dict__ for bar in bar_data])

# 保存到csv文件
df.to_csv("demo.csv")


# 写入数据库
from vnpy.trader.database import get_database
db = get_database()
db.save_bar_data(bar_data)
```


# 分段下载连续数据

每次只能查询一定数量的数据（比如 1000 根）
完成一次查询后，用结束时间作为下一次查询的起始时间
直到全部查询完（时间戳超过目标或者其他标准）
基于时间戳对缓存的 K 线数据排序
最终返回可以直接使用的 BarData 列表

```python
# 加载模块
import requests
from pytz import timezone
from datetime import datetime

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData

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
            "limit": 1000
        }
        r = requests.get(url, params=params)
        data = r.json()

        # 如果有返回的数据，则进行处理
        if data:
            for l in data:
                # 生成时间戳
                dt = datetime.fromtimestamp(l[0]/1000)
                dt = CHINA_TZ.localize(dt)

                # 检查是否已经超出结束时间，若超出则说明已经完成
                if dt > end_dt:
                    finished = True  # 标识完成状态
                    break             # 退出for循环

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
                    gateway_name="BINANCE"
                )
                bar_data[bar.datetime] = bar

                            # 打印本轮查询范围
            print(start_dt, bar.datetime)

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


# 测试一下结果
bar_data = download_binance_minute_data("BTCUSDT", "20250801", "20250810")
print(bar_data[0])
print(bar_data[-1])

import pandas as pd
df = pd.DataFrame.from_records([{"close": bar.close_price} for bar in bar_data])
df.to_csv("BTC_close.csv")
```

# 初识NumPy

```python
import numpy as np
import plotly.express as px

a = np.arange(50)
print(a)

fig = px.line(a)
fig.show()
```

# ndarray数组对象

```python
import numpy as np

# 生成随机数组
data = np.random.randn(10)

# 查看数据
data

# 数组运算
data + data

data * 10


# 创建数组对象
data1 = [3, 4, 5, 6, 7, 8]
arr1 = np.array(data1)

# 查看数组类型
type(arr1)

# 查看数组内容
arr1

# 二维数组
data2 = [
    [1, 3, 5, 7, 9],
    [2, 4, 6, 8, 10]
]
arr2 = np.array(data2)

# 查看数组
arr2

# 查看数组维度
arr2.ndim

# 查看数组形状
arr2.shape

# 查看数据类型
arr2.dtype

# 转换为浮点数数组
arr3 = arr2.astype("float")

arr3

arr3.dtype


# numpy版的range
np.arange(10)

# 全0数组
np.zeros(10)

# 全1数组
np.ones(10)
```

# 向量化运算函数

```python
# 用CSV模块加载数据
from csv import DictReader

with open("BTC_close.csv") as f:
    reader = DictReader(f)
    close_data = [row["close"] for row in reader]

# 查看前10个数据
close_data[:10]

# 转换为数组
import numpy as np

close_array = np.array(close_data).astype("float")

# 取最后20个元素
sample_array = close_array[-20:].copy()

# 查看sample_array
sample_array

# 四则运算（这里以加法为例）
sample_array + sample_array

# 数组每个元素乘以10
sample_array * 10

# 数组每个元素除以1000
sample_array / 1000

# 计算均值
sample_array.mean()

# 计算中位数
np.median(sample_array)

# 计算最大值
sample_array.max()

# 计算最小值
sample_array.min()

# 计算标准差
sample_array.std()

# 累积求和
np.cumsum(sample_array)
```

# 数组进阶编程
```python
import numpy as np

# 创建数组对象
data1 = [3, 4, 5, 6, 7, 8]
arr1 = np.array(data1)

# 基于索引访问数据
arr1[0]
arr1[-1]

# 基于索引切片
buf = arr1[1:3]

# 查看切片结果
buf

# 切片结果只是视图（而非新的数组对象），修改视图会影响原数组
buf[0] = 10

arr1

# 用List作对比
buf2 = data1[1:3]
buf2
buf2[0] = 10
data1

# 用copy来复制创建新的ndarray
buf3 = arr1[1:3].copy()
print(buf3)

# 二维数组
data2 = [
    [1, 3, 5, 7, 9],
    [2, 4, 6, 8, 10]
]
arr2 = np.array(data2)

# 查看 arr2
arr2

# 两种索引方式获取元素
arr2[1][2]
arr2[1, 2]

# 布尔索引
index = arr2 > 3
index

# 基于布尔值筛选出数据（会丢失数组形状）
arr2[arr2 > 3]
```

# 计算大盘的双均线

```python
import numpy as np
import plotly.express as px
import pandas as pd
import pandas as pa
from data_tool import download_binance_minute_data

bar_data = download_binance_minute_data("BTCUSDT", "20250901", "20250902")

# 提取收盘价
close_prices = [bar.close_price for bar in bar_data]

# 绘制曲线
fig = px.line(close_prices)
fig.show()

# 计算移动平均值: 是一种常用的时间序列数据平滑方法，用于消除短期波动，突出长期趋势。
def moving_average(data: list, window: int):
    # 最前面的window窗口数据无法计算
    ma = [0 for i in range(window - 1)]

    # 滚动求和，然后除以窗口得到均值
    for start_ix in range(len(data) - (window - 1)):
        end_ix = start_ix + window
        value = sum(data[start_ix:end_ix]) / window
        ma.append(value)

    # 返回结果
    return ma

# 计算不同窗口的移动平均
ma10 = moving_average(close_prices, 10)
ma20 = moving_average(close_prices, 20)

# 创建 DataFrame
d = {
    "close": close_prices,
    "ma10": ma10,
    "ma20": ma20
}
df = pd.DataFrame(d)

# 绘制折线图
fig = px.line(df)
fig.show()
```

# Series和DataFrame

```python
import pandas as pd
from data_tool import download_binance_minute_data

# 创建对象
s = pd.Series(range(10, 20))

s.index

s.values

s > 15

s[s > 15]


# 自定义标签
s2 = pd.Series([29, 20, 35], index=["shanghai", "beijing", "shenzhen"])

# 查看 s2
s2

# 获取 "shanghai" 对应的值
s2["shanghai"]


bar_data = download_binance_minute_data("BTCUSDT", "20250901", "20250902")

df = pd.DataFrame.from_records([bar.__dict__ for bar in bar_data])


# 基于多个列表的创建
dts = []
open_prices = []
high_prices = []
low_prices = []
close_prices = []

for bar in bar_data:
    dts.append(bar.datetime)
    open_prices.append(bar.open_price)
    high_prices.append(bar.high_price)
    low_prices.append(bar.low_price)
    close_prices.append(bar.close_price)

df2 = pd.DataFrame(dict(open=open_prices, high=high_prices, low=low_prices, close=close_prices), index=dts)

# 查看头部数据
df2.head()

# 提取某列
open_s = df2["open"]

open_s

# 绘制折线图
import plotly.express as px
fig = px.line(df2)
fig.show()

```

# 索引和切片
```python
import pandas as pd
from data_tool import download_binance_minute_data

# 下载币安分钟线的DataFrame
def download_df(symbol: str, start: str, end: str):
    bars = download_binance_minute_data(symbol, start, end)
    df = pd.DataFrame.from_records([bar.__dict__ for bar in bars])
    df.index = df["datetime"]
    return df

df1 = download_df("BTCUSDT", "20250801", "20250810")
df2 = download_df("BTCUSDT", "20250806", "20210815")

df1.index

df1.index.name

df1.index[:10]

# 删掉某一列
df3 = df1.drop("open_price", axis=1)
df3

# iloc访问
df3.iloc[0, 1]

# 切片访问
df3.iloc[1:5, 3:6]

# loc访问
df3.loc["2021-08-05", "close_price"]
```

# 常用统计指标计算

## 统计数量（count）
count 用于统计数据集中有效数据的数量，即非缺失值的个数。通过它可以了解数据的完整程度，若 count 数值与数据总量差距较大，说明存在较多缺失值，可能需要对数据进行缺失值处理，如填充或删除等操作，以保证后续分析的准确性

## 求和（sum、cumsum）
sum 用于计算数据集中所有数值的总和。在金融领域，可用于计算某一时间段内的总交易量；在销售场景中，能统计一段时间的总销售额等，帮助快速获取数据的总量信息

cumsum（累积求和）它会依次计算从数据起始位置到当前位置的数值总和。例如，在分析股票价格的累计涨幅时，cumsum 可以展示出随着时间推移，价格的累积变化情况，便于观察数据的累积趋势。

# 均值（mean）
mean 计算的是数据的算术平均值，反映了数据的集中趋势。比如，计算一组学生的考试平均分，能大致了解整体的学习水平。但均值容易受到极端值（极大或极小值）的影响，当数据中存在极端值时，均值可能无法很好地代表数据的一般水平，此时可结合其他指标（如中位数）一起分析。

## 极值（max、min）
max 用于找出数据集中的最大值。在分析产品价格时，max 可以确定价格的最高值，帮助了解价格的上限情况；在监测系统性能指标时，能找到性能的峰值。

min 则是找出数据集中的最小值，可用于确定价格下限、性能最低值等，与 max 配合使用，能快速掌握数据的波动范围。

## 中位数（median）
median 是将数据按大小顺序排列后，位于中间位置的数值（若数据个数为偶数，则为中间两个数的平均值）。它不受极端值的影响，在数据存在极端值时，比均值更能代表数据的集中趋势。例如，在统计居民收入水平时，若存在少数极高收入者，中位数能更合理地反映大部分居民的收入状况。

```python
import pandas as pd

# 读取 CSV 文件，将 "datetime" 列设为索引
df = pd.read_csv("demo.csv", index_col="datetime")

# 查看 DataFrame 的前几行数据
df.head()

# 统计数量
df.count()

# 对 "volume" 列求和
df["volume"].sum()

# 对 "volume" 列进行累计求和
df["volume"].cumsum()

# 计算 "volume" 的均值
df["volume"].mean()

# 求 "high_price" 列的最大值
df["high_price"].max()

# 求 "low_price" 列的最小值
df["low_price"].min()

# 求中位数
df["close_price"].median()

# 求百分比变动
df["return"] = df["close_price"].pct_change()

# 查看 return 列
df["return"]

# 标准差
df["return"].std()

# 极值索引（最大值索引）
df["return"].idxmax()

# 极值索引（最小值索引）
df["return"].idxmin()

# 汇总描述
df["return"].describe()
```

## 百分比变动（pct_change）
pct_change 用于计算数据的百分比变化。它会将当前数据与上一个数据进行比较，得出相对变化的百分比。在金融领域，可用于计算股票价格、收益率等的环比变化情况，帮助分析数据的波动幅度和趋势变化。例如，对于时间序列的收盘价数据，使用 pct_change 能直观地看到每天收盘价相对于前一天的涨跌幅度。

## 标准差（std）
标准差是用来衡量数据离散程度的指标。它反映了数据相对于均值的分散情况，标准差越大，说明数据的波动越剧烈，离散程度越高；标准差越小，数据越集中在均值附近。在风险分析中，标准差常被用于衡量投资组合的风险水平，标准差大意味着投资风险高，因为收益的波动大，不确定性强。

## 极值索引（idxmax、idxmin）

idxmax 用于获取数据集中最大值所在的索引位置。通过它可以快速定位到数据中最大数值对应的时间或其他标识信息，有助于分析数据出现峰值的时间点或条件。比如，在分析某商品的日销量数据时，idxmax 能找到销量最高的那一天。

idxmin 则是获取数据集中最小值所在的索引位置，可用于定位数据的最低值出现的位置，与 idxmax 配合使用，能全面了解数据极值的分布情况。

## 汇总描述（describe）

describe 可以生成数据的汇总统计信息，包括计数（count）、均值（mean）、标准差（std）、最小值（min）、四分位数（25%、50%、75%）和最大值（max）等。它能一次性提供数据的多个关键统计指标，帮助快速把握数据的整体分布特征，是数据探索性分析中非常实用的工具。