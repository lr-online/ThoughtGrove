from datetime import datetime, timezone, timedelta, UTC
from typing import Optional

# 中国北京时区 (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

def to_utc(dt: datetime) -> datetime:
    """
    将任何时间转换为UTC时间
    
    如果输入时间没有时区信息，假定为UTC时间
    """
    if dt.tzinfo is None:
        # 如果没有时区信息，假定为UTC
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)

def to_beijing(dt: datetime) -> datetime:
    """
    将任何时间转换为北京时间 (UTC+8)
    
    如果输入时间没有时区信息，假定为UTC时间
    """
    if dt.tzinfo is None:
        # 如果没有时区信息，假定为UTC
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(BEIJING_TZ)

def format_datetime(dt: datetime, to_timezone: Optional[timezone] = BEIJING_TZ, 
                   fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    将datetime对象格式化为指定格式的字符串，并转换为指定时区
    
    参数:
        dt: 待格式化的datetime对象
        to_timezone: 目标时区，默认为北京时区
        fmt: 格式化字符串，默认为 "%Y-%m-%d %H:%M:%S"
        
    返回:
        格式化后的时间字符串
    """
    if dt.tzinfo is None:
        # 如果没有时区信息，假定为UTC
        dt = dt.replace(tzinfo=UTC)
        
    if to_timezone:
        dt = dt.astimezone(to_timezone)
        
    return dt.strftime(fmt)

def now_beijing() -> datetime:
    """
    获取当前的北京时间
    """
    return datetime.now(UTC).astimezone(BEIJING_TZ)

def now_utc() -> datetime:
    """
    获取当前的UTC时间
    """
    return datetime.now(UTC) 