from datetime import datetime
import pytz
import time

def get_time_and_timezone_info():
    # Get current time in GMT
    gmt_time = datetime.now(pytz.utc)
    gmt_day_of_week = gmt_time.strftime("%A")  # Day of the week
    
    # Get the device's timezone
    local_time = datetime.now()
    timezone_offset = time.strftime('%z')
    timezone_name = time.tzname[0]
    local_day_of_week = local_time.strftime("%A")  # Day of the week
    
    # Return structured data instead of a formatted string
    info = {
        "gmt_time": gmt_time.strftime('%Y-%m-%d %H:%M:%S'),
        "gmt_day_of_week": gmt_day_of_week,
        "timezone_name": timezone_name,
        "timezone_offset": timezone_offset,
        "local_time": local_time.strftime('%Y-%m-%d %H:%M:%S'),
        "local_day_of_week": local_day_of_week
    }
    
    return info
