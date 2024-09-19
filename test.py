# 파일 열기
with open('24_09_2.log', 'r') as file:
    lines = file.readlines()  # 모든 줄 읽기
    print(lines[-1].split(" ")[0])
    # for line in lines:
    #     print(line.strip())  # 줄바꿈 문자를 제거하고 출력


def toAddData(lastIndexGoogleSheet, logFileName):
    try:
        with open(logFileName, 'r') as readMode:
            lines = readMode.readlines()  # 모든 줄 읽기
            splitIndex = -1
            for i in range(len(lines)):
                indexLogfile = lines[i].split(" ")[0]
                if indexLogfile == lastIndexGoogleSheet:
                    splitIndex = i
                    break
            if splitIndex != -1:
                addRawDataList = lines[splitIndex + 1:]
                addData = []
                for addRawData in addRawDataList:
                    addRawDataSplit = addRawData.split(" ")
                    addDataToAppend = list(filter(lambda item: item != "", addRawDataSplit))
                    addData.append(addDataToAppend)
                return addData
            else:
                return None
    except Exception:
        return None

import gspread
json_file_path = "/Users/kimdonghyun/Downloads/user-log-435911-75a9257d1641.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1DthwcZHaMMeV5qX-5i96K712SI9UKG5Puj-GOfAWvZ0/"
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("페이지 로그 양식")
worksheet.update('c8', [["1", "2", "3", "4"], ["1", "2", "3", "4"]])



import gspread
from gspread_formatting import *

# JSON 파일을 통해 인증
jsonFilePath = "user-log-435911-75a9257d1641.json"
gc = gspread.service_account(jsonFilePath)

# 스프레드시트 URL
spreadSheetUrl = "https://docs.google.com/spreadsheets/d/1DthwcZHaMMeV5qX-5i96K712SI9UKG5Puj-GOfAWvZ0/"
doc = gc.open_by_url(spreadSheetUrl)

PageWorkSheet = doc.worksheet("p24_09_1")
EventWorkSheet = doc.worksheet("e24_09_1")

# 셀에 값 업데이트
PageWorkSheet.update('B2', [['n', '일자', '시-분-초', 'cookie', 'slug', '체류시간', '페이지 스크롤', '재방문 여부', '비활성 사용자']])
EventWorkSheet.update('B2', [['n', '일자', '시-분-초', 'cookie', 'slug', 'click event']])

# 색상 및 서식 지정
headerFormat = CellFormat(
    backgroundColor=Color(0.3, 0.3, 0.3),  # 배경 색상 (RGB로 지정, 1은 255, 0은 0)
    textFormat=TextFormat(
        foregroundColor=Color(1, 1, 1),  # 글자 색상
    )
)

# 셀에 서식 적용
format_cell_range(PageWorkSheet, 'B2:J2', headerFormat)
format_cell_range(EventWorkSheet, 'B2:G2', headerFormat)

set_column_width(PageWorkSheet, 'A', 20)
set_column_width(EventWorkSheet, 'A', 20)
