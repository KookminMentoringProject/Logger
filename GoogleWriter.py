import gspread
import time
import os
import sys
from gspread_formatting import *


def findLastPageLog():
    pageLogPath = "page_log"
    try:
        # 디렉토리 내의 모든 파일 리스트 가져오기
        fileList = [os.path.join(pageLogPath, f) for f in os.listdir(pageLogPath) if os.path.isfile(os.path.join(pageLogPath, f))]

        if not fileList:
            return None  # 파일이 없을 경우 None 반환

        # 마지막으로 수정된 파일 찾기
        latestFile = max(fileList, key=os.path.getmtime)
        latestFileRemoveFolder = latestFile.split("/")[1]
        return latestFileRemoveFolder
    except FileNotFoundError:
        print(f"Directory is not exist")
        return None
    except Exception as e:
        print(f"Unknown error in findLastPageLog")
        return None

def findLastEventLog():
    eventLogPath = "event_log"
    try:
        # 디렉토리 내의 모든 파일 리스트 가져오기
        fileList = [os.path.join(eventLogPath, f) for f in os.listdir(eventLogPath) if os.path.isfile(os.path.join(eventLogPath, f))]

        if not fileList:
            return None  # 파일이 없을 경우 None 반환

        # 마지막으로 수정된 파일 찾기
        latestFile = max(fileList, key=os.path.getmtime)
        latestFileRemoveFolder = latestFile.split("/")[1]
        return latestFileRemoveFolder
    except FileNotFoundError:
        print(f"Directory is not exist")
        return None
    except Exception as e:
        print(f"Unknown error in findLastEventLog")
        return None

def readyToAddData(p_lastLogFileName, p_sheetLastRow, e_lastLogFileName, e_sheetLastRow):
    totalAddDataList = []
    p_addDataList = []
    e_addDataList = []
    # page log부터 준비
    try:
        with open("page_log/" + p_lastLogFileName, 'r') as pageLogRead:
            pageLogLines = pageLogRead.readlines()  # 모든 줄 읽기
            pageLogDataList = pageLogLines[(p_sheetLastRow - 1):]
            if len(pageLogDataList) > 0:
                for pageLogData in pageLogDataList:
                    pageLogDataSplit = pageLogData.split(" ")
                    pageLogDataRemoveSpace = list(filter(lambda item: item != "" and item != "\n", pageLogDataSplit))
                    p_addDataList.append(pageLogDataRemoveSpace)
    except Exception:
        return None
    
    # event log 준비
    try:
        with open("event_log/" + e_lastLogFileName, 'r') as eventLogRead:
            eventLogLines = eventLogRead.readlines()  # 모든 줄 읽기
            eventLogDataList = eventLogLines[(e_sheetLastRow - 1):]
            if len(eventLogDataList) > 0:
                for eventLogData in eventLogDataList:
                    eventLogDataSplit = eventLogData.split(" ")
                    eventLogDataSplitRemoveSpace = list(filter(lambda item: item != "" and item != "\n", eventLogDataSplit))
                    e_addDataList.append(eventLogDataSplitRemoveSpace)
    except Exception:
        return None
    
    if len(p_addDataList) != 0:
        totalAddDataList.append(p_addDataList)
    if len(e_addDataList) != 0:
        totalAddDataList.append(e_addDataList)
    return totalAddDataList

def getLastSheet(worksheets):
    p_lastSheet = ""
    e_lastSheet = ""
    
    p_lastsheetYear = "24"
    p_lastsheetMonth = "09"
    p_lastsheetCount = "0"
    
    e_lastsheetYear = "24"
    e_lastsheetMonth = "09"
    e_lastsheetCount = "0"

    for worksheet in worksheets:
        # 최신시트 추리는 작업
        if "p" in worksheet:
            p_worksheetYear = worksheet[1:3]
            p_worksheetMonth = worksheet[4:6]
            p_worksheetCount = worksheet[7]
            
            if (p_worksheetYear >= p_lastsheetYear) and (p_worksheetMonth >= p_lastsheetMonth) and (p_worksheetCount >= p_lastsheetCount):
                p_lastsheetYear = p_worksheetYear
                p_lastsheetMonth = p_worksheetMonth
                p_lastsheetCount = p_worksheetCount
        
        # 최신시트 추리는 작업
        if "e" in worksheet:
            e_worksheetYear = worksheet[1:3]
            e_worksheetMonth = worksheet[4:6]
            e_worksheetCount = worksheet[7]
            
            if (e_worksheetYear >= e_lastsheetYear) and (e_worksheetMonth >= e_lastsheetMonth) and (e_worksheetCount >= e_lastsheetCount):
                e_lastsheetYear = e_worksheetYear
                e_lastsheetMonth = e_worksheetMonth
                e_lastsheetCount = e_worksheetCount
    
    p_lastSheet = "p" + p_lastsheetYear + "_" + p_lastsheetMonth + "_" + p_lastsheetCount
    e_lastSheet = "e" + e_lastsheetYear + "_" + e_lastsheetMonth + "_" + e_lastsheetCount
    if p_lastSheet != "p24_09_0" and e_lastSheet != "e24_09_0":
        return [p_lastSheet, e_lastSheet]
    else:
        return None


# main 시작

# initialize 작업
# 엑셀 기록 시작할 컬럼 지정
startWriteExcelCol = "b"

# 헤더 색상 및 서식 만들어주기
headerFormat = CellFormat(
    backgroundColor=Color(0.3, 0.3, 0.3),  # 배경 색상 (RGB로 지정, 1은 255, 0은 0)
    textFormat=TextFormat(
        foregroundColor=Color(1, 1, 1),  # 글자 색상
    )
)

# 1. 구글 스프레드 시트의 리스트를 파이썬에 저장
jsonFilePath = "user-log-435911-75a9257d1641.json"
gc = gspread.service_account(jsonFilePath)
spreadSheetUrl = "https://docs.google.com/spreadsheets/d/1DthwcZHaMMeV5qX-5i96K712SI9UKG5Puj-GOfAWvZ0/"
doc = gc.open_by_url(spreadSheetUrl)
########################################################################################################

# 2. 시트 리스트는 2개이다. 페이지, 이벤트
worksheetObjList = doc.worksheets()
worksheets = [sheet.title for sheet in worksheetObjList]
########################################################################################################

# 3. 여기서 가장 마지막꺼 추출해서 p_lastSheet, e_lastSheet 변수명으로 저장하기
p_lastSheet = ""
e_lastSheet = ""

lastSheetList = getLastSheet(worksheets)
if lastSheetList != None:
    p_lastSheet = lastSheetList[0]
    e_lastSheet = lastSheetList[1]
else:
    print("getLastSheet function error")
    sys.exit()

PageWorkSheet = doc.worksheet(p_lastSheet)
EventWorkSheet = doc.worksheet(e_lastSheet)
########################################################################################################

# 4. p_lastSheet, e_lastSheet의 전체 컬럼 불러와서 마지막으로 기록된 p_sheetLastRow, e_sheetLastRow 기록하기 페이지, 이벤트 둘다
allPageSheetLines = PageWorkSheet.get_all_values()
p_sheetLastRow = len(allPageSheetLines)

allEventSheetLines = EventWorkSheet.get_all_values()
e_sheetLastRow = len(allEventSheetLines)
########################################################################################################


# while True 돌면서 지속적으로 수행할 것
while True:
# 1. 기존의 파일 시스템의 로그 파일중에서 최근에 수정된애꺼의 이름 불러오기 페이지, 이벤트 둘다. 변수명은 p_lastLogFileName, e_lastLogFileName
    p_lastLogFileName = findLastPageLog()
    if p_lastLogFileName == None:
        print("failed to find p_lastLogFileName")
        sys.exit()
    
    e_lastLogFileName = findLastEventLog()
    if e_lastLogFileName == None:
        print("failed to find e_lastLogFileName")
        sys.exit()
########################################################################################################

# 2. p_lastLogFileName, e_lastLogFileName과 p_lastSheet, e_lastSheet와 비교
# 3. 일치하면 그 이름 가지고 문서 수정작업 들어갈거임
# 4. 없으면 새로 생성함. 내 파일시스템에서 불러와진애의 이름을 가지고. 그리고 p_sheetLastRow, e_sheetLastRow 는 둘다 2이된다. 그리고 헤더 셋업해주고
    p_lastLogFileNameRemoveExt = p_lastLogFileName.split(".")[0]
    if ("p" + p_lastLogFileNameRemoveExt) != p_lastSheet:
        p_lastSheet = "p" + p_lastLogFileNameRemoveExt
        doc.add_worksheet(title=p_lastSheet, rows="50000", cols="12")
        PageWorkSheet = doc.worksheet(p_lastSheet)
        format_cell_range(PageWorkSheet, 'B2:J2', headerFormat)
        PageWorkSheet.update('B2', [['n', '일자', '시-분-초', 'cookie', 'slug', '체류시간', '페이지 스크롤', '재방문 여부', '비활성 사용자']])
        set_column_width(PageWorkSheet, 'A', 20)
        p_sheetLastRow = 2
    
    e_lastLogFileNameRemoveExt = e_lastLogFileName.split(".")[0]
    if ("e" + e_lastLogFileNameRemoveExt) != e_lastSheet:
        e_lastSheet = "e" + e_lastLogFileNameRemoveExt
        doc.add_worksheet(title=e_lastSheet, rows="50000", cols="12")
        EventWorkSheet = doc.worksheet(e_lastSheet)
        format_cell_range(EventWorkSheet, 'B2:G2', headerFormat)
        EventWorkSheet.update('B2', [['n', '일자', '시-분-초', 'cookie', 'slug', 'click event']])
        set_column_width(EventWorkSheet, 'A', 20)
        e_sheetLastRow = 2
########################################################################################################

# 5. p_lastLogFileName, e_lastLogFileName 로그파일 읽어들여서 (p_sheetLastRow - 2), (e_sheetLastRow의 - 2) 부터 시작되는 dataSet준비
#    변수 이름은 p_addDataList ,e_addDataList

    addDataList = readyToAddData(p_lastLogFileName, p_sheetLastRow, e_lastLogFileName, e_sheetLastRow)
    if addDataList == None:
        print("Failed to parse log")
        sys.exit()

    if len(addDataList) != 2:
        print("no exist update log")
        time.sleep(10)
        continue
    
    p_addDataList = addDataList[0]
    e_addDataList = addDataList[1]
########################################################################################################

# 6. p_lastSheet, e_lastSheet에다가 p_addDataList ,e_addDataList 기록해주기
    p_startWriteExcelRow = str(p_sheetLastRow+1)
    e_startWriteExcelRow = str(e_sheetLastRow+1)
    
    p_startWritePoint = startWriteExcelCol + p_startWriteExcelRow
    e_startWritePoint = startWriteExcelCol + e_startWriteExcelRow
    
    PageWorkSheet.update(p_startWritePoint,p_addDataList)
    EventWorkSheet.update(e_startWritePoint,e_addDataList)

    time.sleep(30)

# while True 끝지점
########################################################################################################




