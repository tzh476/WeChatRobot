# 示例：获取某只股票的涨跌幅
# stock_code = "600036"  # 招商银行
from base.Demo1_change import get_stock_change


#    df=get_price('sh000001',frequency='1d',count=1)      #支持'1d'日, '1w'周, '1M'月
#     print('上证指数日线行情\n',df)
#
#     df=get_price('000001.XSHG',frequency='15m',count=1)  #支持'1m','5m','15m','30m','60m'
#     print('上证指数分钟线\n',df)
#
#     df = get_price('sh600036', frequency='1m', count=20)  # 分钟线实时行情，可用'1m','5m','15m','30m','60m'
#     print('招商银行1分钟线\n', df)
# 示例：获取某只股票的涨跌幅
# stock_code = "600036"  # 招商银行
stock_code = "002594"
result = get_stock_change(stock_code)

print("\n".join([f"{key}: {value.iloc[0]}" for key, value in result.items()]))

