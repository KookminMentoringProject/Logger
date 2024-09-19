# from enum import Enum

# class CommonLogType(Enum):
#     DATE_TIME        = 0
#     SLUG             = 1
#     COOKIE           = 2
    
# class PageLogType(Enum):
#     DWILL_TIME       = 0
#     SCROLLINGPERCENT = 1
#     RETURN_VISITOR   = 2
#     INACTIVE_USER    = 3
    
# class EventLogType(Enum):
#     CLICK_EVENT_TYPE = 0

import copy
from LogWriter import *

# 참조용으로 만들어둔거지 이거 그대로 갖다 쓰지 마세요~
# C++ 개발자에게 파이썬은 불지옥이다.. 오히려 더 어려워ㅠㅠ
PageLogStruct = {
    "n" : "",
    "date" : "",
    "time" : "",
    "cookie" : "",
    "slug" : "",
    "dwillTime" : "",
    "scrollPercent" : "",
    "newVisiter" : ""
}

EventLogStruct = {
    "n" : "",
    "date" : "",
    "time" : "",
    "cookie" : "",
    "slug" : "",
    "click_event" : ""
}

def pageLogProcess(currentDateTime, timeSpent, currentUrl, userVisitCookie, newVisiter, scrollingPercentage):
    try:
        # struct 원본 그대로 일단 복사뜨고
        PageLogDict = copy.deepcopy(PageLogStruct)
    except Exception:
        print("Failed to copy page struct")
        return False
    
    try:
        # 파싱 과정
        dateTimeList = currentDateTime.split(" ")
        date = dateTimeList[0]
        time = dateTimeList[1]

        cookie = userVisitCookie
        
        currentUrlSplit = currentUrl.split("http://localhost:8080")
        # 뒤에 오는 하위 경로만 분리
        slug = currentUrlSplit[1].rstrip()

        timeSpentMs = int(timeSpent)
        total_seconds = timeSpentMs / 1000.0
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int(timeSpentMs % 1000)
        dwillTime = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

        if scrollingPercentage == "NaN":
            scrollPercent = "100%"
        else:
            scrollFloat = float(scrollingPercentage)
            rounded_number = round(scrollFloat, 2)
            percent = rounded_number * 100
            scrollPercent = str(percent) + "%"
        
        # 값 채워주기
        PageLogDict["date"] = date
        PageLogDict["time"] = time
        PageLogDict["cookie"] = cookie
        PageLogDict["slug"] = slug
        PageLogDict["dwillTime"] = dwillTime
        PageLogDict["scrollPercent"] = scrollPercent
        PageLogDict["newVisiter"] = newVisiter
    except Exception:
        print("Failed to page log parsing")
        return False
    
    ret = pageLogWrite(PageLogDict)
    if ret == False:
        print("Failed to pageLogWrite")
    
    return True


def eventLogProcess(currentDateTime, userVisitCookie, uri, clickItem):
    try:
        # struct 원본 그대로 일단 복사뜨고
        EventLogDict = copy.deepcopy(EventLogStruct)
    except Exception:
        print("Failed to copy event struct")
        return False
    
    try:
        # 파싱 과정
        dateTimeList = currentDateTime.split(" ")
        date = dateTimeList[0]
        time = dateTimeList[1]

        cookie = userVisitCookie.strip()
        
        slash_count = uri.count('/')
        if slash_count == 2:
            if "mypage" in uri:
                slug = uri[7:]
            else:
                slug = uri
        else:
            slug = uri

        # 값 채워주기
        EventLogDict["date"] = date
        EventLogDict["time"] = time
        EventLogDict["cookie"] = cookie
        EventLogDict["slug"] = slug
        EventLogDict["click_event"] = clickItem
    except Exception:
        print("Failed to event log parsing")
        return False
    
    ret = eventLogWrite(EventLogDict)
    if ret == False:
        print("Failed to eventLogWrite")
    
    return True
