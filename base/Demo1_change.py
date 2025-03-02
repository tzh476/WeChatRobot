#A股票行情数据获取演示   https://github.com/mpquant/Ashare
from  Ashare import *

# 证券代码兼容多种格式 通达信，同花顺，聚宽
# sh000001 (000001.XSHG)    sz399006 (399006.XSHE)   sh600519 ( 600519.XSHG ) 


def convert_stock_code(code: str) -> str:
    """
    将用户输入的A股股票代码（如 600036）转换为带交易所前缀的标准代码（如 sh600036）。
    """
    if not code.isdigit() or len(code) != 6:
        raise ValueError("股票代码必须是6位数字")

    # 判断交易所
    if code.startswith(('600', '601', '603', '605')):  # 沪市主板
        return 'sh' + code
    elif code.startswith(('000', '001')):  # 深市主板
        return 'sz' + code
    elif code.startswith('002'):  # 深市中小板
        return 'sz' + code
    elif code.startswith('300'):  # 深市创业板
        return 'sz' + code
    elif code.startswith('688'):  # 沪市科创板
        return 'sh' + code
    else:
        raise ValueError("无法识别的股票代码前缀")

# # 测试代码
# test_codes = ["600036", "000001", "002001", "300001", "688001", "601398"]
# for code in test_codes:
#     print(f"用户输入: {code} -> 转换后: {convert_stock_code(code)}")


def get_stock_change(stock_code: str):
    stock_code = convert_stock_code(stock_code)
    # 获取最近2条数据，确保包含昨天的收盘价
    df = get_price_and_change_min_tx(stock_code, frequency='1m', count=1)
    # pd.set_option('display.max_columns', None)  # 显示所有列
    # pd.set_option('display.width', 200)  # 设置输出宽度，防止换行

    return df
