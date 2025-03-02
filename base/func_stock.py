#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import pandas as pd


from base.Demo1_change import get_stock_change


class Stock:
    def __init__(self) -> None:
        self.LOG = logging.getLogger(__name__)

    def get_answer(self, question: str) -> str:
        # wxid或者roomid,个人时为微信id，群消息时为群id
        try:
            res = get_stock_change(question)
            res_message = self.format_stock_info(res)
            return res_message
        except Exception as e0:
            print(e0)
            self.LOG.error(f"发生未知错误：{str(e0)}")

        return ""

    def format_stock_info(self, stock_data):
        # 映射字典，将英文的字段转换为中文
        keymap = {
            "name": "名称",
            "code": "代码",
            "close": "股价",
            "change": "涨跌幅",
            # "volume": "成交量",
        }
        result = []
        for key, label in keymap.items():
            if key in stock_data:
                value = stock_data[key]
                if isinstance(value, pd.Series):  # 取出 Series 的第一个值
                    value = value.iloc[0]

                if key == "change":  # 涨跌幅加上百分号
                    value = f"{value:.2f}%"

                result.append(f"{label}: {value}")

        return "\n".join(result)  # 拼接成单行字符串


if __name__ == "__main__":
    stock = Stock()
    code = '600036'
    print(stock.get_answer(code))
