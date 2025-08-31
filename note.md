
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

# A股日线数据获取 

```python
# 封装函数
from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData
from vnpy.trader.database import DB_TZ, database_manager

def download_stock_daily_data(symbol: str, exchange: Exchange):
    """基于代码和交易所下载数据"""
    exchange_map = {
        Exchange.SSE: "sh",
        Exchange.SZSE: "sz",
    }
    exchange_str = exchange_map[exchange]

    url = f"http://api.finance.ifeng.com/akdaily/?code={exchange_str}{symbol}&type=last"
    r = requests.get(url)
    record = r.json()["record"]

    bar_data = []
    for rd in record:
        dt = datetime.strptime(rd[0], "%Y-%m-%d")
        bar = BarData(
            symbol=symbol,
            exchange=exchange,
            datetime=DB_TZ.localize(dt),
            interval=Interval.DAILY,
            open_price=rd[1],
            high_price=rd[2],
            close_price=rd[3],
            low_price=rd[4],
            volume=rd[5],
            gateway_name="IFENG"
        )
        bar_data.append(bar)
    return bar_data

# 尝试下载
bar_data = download_stock_daily_data("600036", Exchange.SSE)

# 转换DataFrame
import pandas as pd
df = pd.DataFrame.from_records([bar.__dict__ for bar in bar_data])

# 保存到csv文件
df.to_csv("demo.csv")

# 写入数据库
database_manager.save_bar_data(bar_data)
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
