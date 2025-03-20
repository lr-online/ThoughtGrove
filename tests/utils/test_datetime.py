from datetime import datetime, timedelta, UTC
import pytest
from thoughtgrove.utils.datetime import (
    to_utc, to_beijing, format_datetime, now_beijing, now_utc, BEIJING_TZ
)

def test_to_utc_with_tzinfo():
    # 创建一个带北京时区的时间
    beijing_dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=BEIJING_TZ)
    # 转换为UTC
    utc_dt = to_utc(beijing_dt)
    # 北京时间比UTC早8小时
    assert utc_dt.hour == 4
    assert utc_dt.tzinfo == UTC

def test_to_utc_without_tzinfo():
    # 创建一个不带时区的时间
    naive_dt = datetime(2023, 1, 1, 12, 0, 0)
    # 转换为UTC (假定输入是UTC)
    utc_dt = to_utc(naive_dt)
    assert utc_dt.hour == 12
    assert utc_dt.tzinfo == UTC

def test_to_beijing_with_tzinfo():
    # 创建一个带UTC时区的时间
    utc_dt = datetime(2023, 1, 1, 4, 0, 0, tzinfo=UTC)
    # 转换为北京时间
    beijing_dt = to_beijing(utc_dt)
    # 北京时间比UTC晚8小时
    assert beijing_dt.hour == 12
    assert beijing_dt.tzinfo == BEIJING_TZ

def test_to_beijing_without_tzinfo():
    # 创建一个不带时区的时间
    naive_dt = datetime(2023, 1, 1, 4, 0, 0)
    # 转换为北京时间 (假定输入是UTC)
    beijing_dt = to_beijing(naive_dt)
    # 北京时间比UTC晚8小时
    assert beijing_dt.hour == 12
    assert beijing_dt.tzinfo == BEIJING_TZ

def test_format_datetime_default():
    # 创建一个UTC时间
    utc_dt = datetime(2023, 1, 1, 4, 0, 0, tzinfo=UTC)
    # 格式化为默认格式 (转换为北京时间)
    formatted = format_datetime(utc_dt)
    assert formatted == "2023-01-01 12:00:00"

def test_format_datetime_custom():
    # 创建一个UTC时间
    utc_dt = datetime(2023, 1, 1, 4, 0, 0, tzinfo=UTC)
    # 格式化为自定义格式 (保持UTC)
    formatted = format_datetime(utc_dt, to_timezone=UTC, fmt="%Y/%m/%d %H:%M")
    assert formatted == "2023/01/01 04:00"

def test_now_functions():
    # 简单测试确保now_utc和now_beijing不会抛出异常
    # 并且它们的时区是正确的
    utc_now = now_utc()
    beijing_now = now_beijing()
    
    assert utc_now.tzinfo == UTC
    assert beijing_now.tzinfo == BEIJING_TZ
    
    # 检查北京时间和UTC时间在同一时刻，只是表示的时区不同
    # 因此它们的时间戳应该相同或非常接近
    utc_timestamp = utc_now.timestamp()
    beijing_timestamp = beijing_now.timestamp()
    
    assert abs(utc_timestamp - beijing_timestamp) < 1  # 允许1秒内的误差 