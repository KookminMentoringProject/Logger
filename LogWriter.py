from datetime import datetime
import os


# 로그 파일 작명법
# 24_01_1 -> 24년도 1월 1일부터 10일 집계
# 24_11_2 -> 24년도 11월 11일부터 20일 집계
# 24_12_3 -> 24년도 12월 21일부터 말일까지의 집계

# 로그 파일 나누는 기준
# 1일부터 10일까지는  _1
# 11일부터 20일까지는 _2
# 21일부터 그 이후는  _3

def getFileName():
    # 현재 날짜와 시간 구하기
    now = datetime.now()
    
    # 날짜를 yyyy-mm-dd 형식으로 포맷
    currentDate = now.strftime("%Y-%m-%d")
    #print("현재 날짜:", current_date)
    
    # 년도, 월, 일 추출
    currentDateList = currentDate.split("-")
    year = currentDateList[0][2:]
    month = currentDateList[1]
    day = int(currentDateList[2])
    
    # 파일 이름 제작 하기
    fileName = str(year) + "_" + str(month) + "_"
    if day > 20:
        fileName += "1.log"
    elif day > 10:
        fileName += "2.log"
    elif day > 0:
        fileName += "3.log"
    else:
        print("day process error!")
        return None
    return fileName


def pageLogWrite(PageLogDict):
    defaultFilePath = "/Users/kimdonghyun/Desktop/kookmin_logger/page_log/"
    try:
        # 로그 데이터를 파일에 기록 (누적 기록)
        fileName = getFileName()
        if fileName != None :
            defaultFilePath += fileName
        else:
            print("Failed to getFileName")
            return False
    except Exception:
        print("Failed to getFileName")
        return False
    
    try:
        if not os.path.exists(defaultFilePath):
            PageLogDict["n"] = "p1"
            with open(defaultFilePath, 'w') as file:
                for key in PageLogDict.keys():
                    file.write(key)
                    file.write("         ")
                file.write("\n")
        else:
            with open(defaultFilePath, 'r') as readMode:
                lines = readMode.readlines()  # 모든 줄 읽기
                lastN = lines[-1].split(" ")[0]
                onlyNumberStr = lastN[1:]
                onlyNumber = int(onlyNumberStr)
                onlyNumber = onlyNumber + 1
                PageLogDict["n"] = "p" + str(onlyNumber)
    except Exception:
        print("Failed to \"os.path.exists(defaultFilePath)\" ")
        return False
    
    try:
        with open(defaultFilePath, 'a') as log_file:
            for value in PageLogDict.values():
                log_file.write(value)
                log_file.write("    ")
            log_file.write("\n")
    except Exception:
        print("Failed to open log file and write")
        return False


def eventLogWrite(EventLogDict):
    defaultFilePath = "/Users/kimdonghyun/Desktop/kookmin_logger/event_log/"
    try:
        # 로그 데이터를 파일에 기록 (누적 기록)
        fileName = getFileName()
        if fileName != None :
            defaultFilePath += fileName
        else:
            print("Failed to getFileName")
            return False
    except Exception:
        print("Failed to getFileName")
        return False
    
    try:
        if not os.path.exists(defaultFilePath):
            EventLogDict["n"] = "e1"
            with open(defaultFilePath, 'w') as file:
                for key in EventLogDict.keys():
                    file.write(key)
                    file.write("         ")
                file.write("\n")
        else:
            with open(defaultFilePath, 'r') as readMode:
                lines = readMode.readlines()  # 모든 줄 읽기
                lastN = lines[-1].split(" ")[0]
                onlyNumberStr = lastN[1:]
                onlyNumber = int(onlyNumberStr)
                onlyNumber = onlyNumber + 1
                EventLogDict["n"] = "e" + str(onlyNumber)
    except Exception:
        print("Failed to \"os.path.exists(defaultFilePath)\" ")
        return False
    
    try:
        with open(defaultFilePath, 'a') as log_file:
            for value in EventLogDict.values():
                log_file.write(value)
                log_file.write("    ")
            log_file.write("\n")
    except Exception:
        print("Failed to open log file and write")
        return False