import calendar
import datetime
import pandas as pd

from chinese_calendar import is_workday

from base.Ashare import get_price_and_change_min_tx
from robot import Robot


class ReportReminder:

    @staticmethod
    def remind(robot: Robot) -> None:

        receivers = robot.config.REPORT_REMINDERS
        if not receivers:
            receivers = ["filehelper"]
        # 日报周报月报提醒
        for receiver in receivers:
            today = datetime.datetime.now().date()
            # 如果是非工作日
            # if not is_workday(today):
            #     robot.sendTextMsg("休息日快乐", receiver)
            # 如果是工作日
            if is_workday(today):
                robot.chat.get_answer()
                report = ReportReminder.get_report_stock()
                robot.sendTextMsg(report, receiver)
            # 如果是本周最后一个工作日
            # if ReportReminder.last_work_day_of_week(today) == today:
            #     robot.sendTextMsg("该发周报啦", receiver)
            # # 如果本日是本月最后一整周的最后一个工作日:
            # if ReportReminder.last_work_friday_of_month(today) == today:
            #     robot.sendTextMsg("该发月报啦", receiver)

    # 计算本月最后一个周的最后一个工作日
    @staticmethod
    def last_work_friday_of_month(d: datetime.date) -> datetime.date:
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        weekday = calendar.weekday(d.year, d.month, days_in_month)
        if weekday == 4:
            last_friday_of_month = datetime.date(
                d.year, d.month, days_in_month)
        else:
            if weekday >= 5:
                last_friday_of_month = datetime.date(d.year, d.month, days_in_month) - \
                                       datetime.timedelta(days=(weekday - 4))
            else:
                last_friday_of_month = datetime.date(d.year, d.month, days_in_month) - \
                                       datetime.timedelta(days=(weekday + 3))
        while not is_workday(last_friday_of_month):
            last_friday_of_month = last_friday_of_month - datetime.timedelta(days=1)
        return last_friday_of_month

    # 计算本周最后一个工作日
    @staticmethod
    def last_work_day_of_week(d: datetime.date) -> datetime.date:
        weekday = calendar.weekday(d.year, d.month, d.day)
        last_work_day_of_week = datetime.date(
            d.year, d.month, d.day) + datetime.timedelta(days=(6 - weekday))

        while not is_workday(last_work_day_of_week):
            last_work_day_of_week = last_work_day_of_week - \
                                    datetime.timedelta(days=1)
        return last_work_day_of_week

    @staticmethod
    def df_to_multiline_string(df: pd.DataFrame) -> str:
        """
        将 DataFrame 转换为分行字符串格式，支持字段映射（去掉成交量）。
        """
        keymap = {
            "name": "股票名称",
            "code": "股票代码",
            "change": "涨跌幅",
            "close": "收盘价",
            "open": "开盘价",
            "high": "最高价",
            "low": "最低价",
        }

        result = []
        if df.empty:
            return "无数据"

        latest_data = df.iloc[-1]

        # **🚀 倒序遍历 keymap**
        for key in keymap.keys():
            label = keymap[key]
            value = latest_data[key]
            if key == "change":  # ✅ 涨跌幅加上百分号
                value = f"{value:.2f}%"
            elif isinstance(value, float):  # ✅ 保留两位小数
                value = f"{value:.2f}"
            result.append(f"{label}: {value}")

        return "\n".join(result)

    @staticmethod
    def get_report_stock() -> str:
        # 获取第一个股票数据并转换
        df1 = get_price_and_change_min_tx("sh000001", frequency='1d', count=1)
        result_str1 = ReportReminder.df_to_multiline_string(df1)

        # 获取第二个股票数据并转换
        df2 = get_price_and_change_min_tx("sz399001", frequency='1d', count=1)
        result_str2 = ReportReminder.df_to_multiline_string(df2)

        # 拼接两个结果字符串
        combined_result = result_str1 + "\n\n" + result_str2
        return combined_result


if __name__ == "__main__":
    combined_result = ReportReminder.get_report_stock()
    print(combined_result)
