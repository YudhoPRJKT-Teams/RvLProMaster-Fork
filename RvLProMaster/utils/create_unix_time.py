from .create_log import CreateLog
from datetime import datetime, timedelta, timezone
import time

class UnixTime:
  # Calculate Time
  @classmethod
  def CalculateTime(cls, input_time: int):
    future_time = datetime.now(timezone.utc) + timedelta(seconds=input_time)
    return int(future_time.timestamp())
  
  # Convert From Timestamp to date
  @classmethod
  def ReadFromTimestamp(cls, timestamp: int) -> str:
    return str(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S UTC'))
  class ConvertFrom:
    # Minutes
    @classmethod
    def Minutes(cls, time: int) -> str:
      if time is not None:
        return str(UnixTime.CalculateTime(time * 60))
      
    # Hours
    @classmethod
    def Hour(cls, time: int) -> str:
      if time is not None:
        return str(UnixTime.CalculateTime(time * 3600))
      
    # Day
    @classmethod
    def Day(cls, time: int) -> str:
      if time is not None:
        return str(UnixTime.CalculateTime(time * 86400))
      
    # Month
    @classmethod
    def Month(cls, time: int) -> str:
      if time is not None:
        return str(UnixTime.CalculateTime(time * 30 * 86400))
      
      
    # Month
    @classmethod
    def Year(cls, time: int) -> str:
      if time is not None:
        return str(UnixTime.CalculateTime(time * 365 * 86400))
    
    # Custom
    @classmethod
    def Custom(cls, time: int) -> str:
      if time is not None:
        return str(UnixTime.CalculateTime(time))