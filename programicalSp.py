import datetime
from pytz import timezone
from collections import OrderedDict

def getProgramicalSp(programs_dict):
    def customsort(dict1 , key_order):
        items = [dict1[k] if k in dict1.keys() else None for k in key_order] 
        sorted_dict = OrderedDict()
        for i in range(len(key_order)):
            if( items[i] != None ):
                sorted_dict[key_order[i]] = items[i]
        return sorted_dict
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    now = datetime.datetime.now().astimezone(timezone('Europe/Budapest'))
    
    if(programs_dict == None):
        return None
    programs_dict_sorted = customsort(programs_dict,days)
    
    dayNow = days.index(now.strftime("%A"))
    hourNow = now.strftime("%H")
    setpoint = None
    defaultSetpoint = 24
    
    for dayName in programs_dict_sorted:
        day = days.index(dayName.capitalize())
        if( day <= dayNow and isinstance(programs_dict_sorted[dayName], dict) ):
            selectedDay = sorted(programs_dict_sorted[dayName])
            for hour in selectedDay:
                if( ( day < dayNow ) or ( day == dayNow and hour <= hourNow ) ):
                    setpoint = programs_dict_sorted[dayName][hour]
                    
    if( setpoint == None and isinstance(programs_dict_sorted, dict) ):
        daysLastKey = list(programs_dict_sorted.keys())[-1]
        if( isinstance(programs_dict_sorted[daysLastKey], dict) ):
            sortedLastDay = sorted(programs_dict_sorted[daysLastKey])
            if( sortedLastDay ):
                hoursLastKey = sortedLastDay[-1]
                setpoint = programs_dict_sorted[daysLastKey][hoursLastKey]
    
    return setpoint