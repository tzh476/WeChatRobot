# A股票行情数据获取演示   https://github.com/mpquant/Ashare
from base.Ashare import get_price_and_change_min_tx

# 证券代码兼容多种格式 通达信，同花顺，聚宽
# sh000001 (000001.XSHG)    sz399006 (399006.XSHE)   sh600519 ( 600519.XSHG ) 


import re


def convert_stock_code(code: str) -> str:
    """
    将用户输入的 A 股股票代码（可能含有非数字字符）转换为带交易所前缀的标准代码。
    适用于：
    - 沪深 A 股（主板、中小板、创业板、科创板）
    - 沪深 ETF（交易型开放式指数基金）
    - 其他股票代码，如科创 50 ETF（588xxx）

    例如：
    - "600036" → "sh600036"（沪市主板）
    - "000001" → "sz000001"（深市主板）
    - "510300" → "sh510300"（沪市 ETF）
    - "159915" → "sz159915"（深市 ETF）
    - "588000" → "sh588000"（科创 50 ETF）
    """

    # 只保留 `code` 中的数字部分（去掉前后可能的字母）
    digits = re.sub(r'\D', '', code)  # 提取纯数字

    if len(digits) != 6:
        raise ValueError(f"无法识别的股票代码: {code}，提取到的数字部分: {digits}")

    # **沪市（sh）**
    if digits.startswith(('600', '601', '603', '605')):  # 沪市主板
        return 'sh' + digits
    elif digits.startswith('688'):  # 科创板
        return 'sh' + digits
    elif digits.startswith('588'):  # 科创 50 ETF
        return 'sh' + digits
    elif digits.startswith('51'):  # 沪市 ETF（如 510300）
        return 'sh' + digits

    # **深市（sz）**
    elif digits.startswith(('000', '001')):  # 深市主板
        return 'sz' + digits
    elif digits.startswith('002'):  # 深市中小板
        return 'sz' + digits
    elif digits.startswith('300'):  # 深市创业板
        return 'sz' + digits
    elif digits.startswith(('15', '16')):  # 深市 ETF（如 159915）
        return 'sz' + digits

    else:
        raise ValueError(f"无法识别的股票代码前缀: {code}，提取到的数字部分: {digits}")


# **📌 测试示例**
if __name__ == "__main__":
    print("\n")
    test_codes = [
        "600036", "000001", "510300", "159915", "688981", "588000",
        "sh600519", "sz000002", "002475abc", "300750xyz"
    ]
    for code in test_codes:
        try:
            print(f"{code} → {convert_stock_code(code)}")
        except ValueError as e:
            print(f"❌ {e}")


# 示例
# try:
#     print(convert_stock_code("sh600036"))  # 输出: sh600036
#     print(convert_stock_code("600036xyz"))  # 输出: sh600036
#     print(convert_stock_code("abc000001"))  # 输出: sz000001
#     print(convert_stock_code("xyz12345"))  # 会抛出错误
# except ValueError as e:
#     print(f"错误: {e}")


def get_stock_change(stock_code: str):
    stock_code = convert_stock_code(stock_code)
    # 获取最近1条数据，确保包含昨天的收盘价
    df = get_price_and_change_min_tx(stock_code, frequency='1m', count=1)
    # pd.set_option('display.max_columns', None)  # 显示所有列
    # pd.set_option('display.width', 200)  # 设置输出宽度，防止换行

    return df
