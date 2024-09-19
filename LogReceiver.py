from flask import Flask, request
from flask_cors import CORS

from LogProcesser import * 
from LogWriter import *

app = Flask(__name__)
CORS(app)  # CORS 설정 추가

""" 자바스크립트에서 fetch로 쿼리 던지는 형태 참고할 것
    fetch(`/getLog?currentDateTime=${encodeURIComponent(currentDateTime)}&timeSpent=${encodeURIComponent(timeSpent)}
    &currentUrl=${encodeURIComponent(currentUrl)}&userVisitCookie=${encodeURIComponent(userVisitCookie)}
    &newVisiter=${encodeURIComponent(newVisiter)}&scrollingPercentage=${encodeURIComponent(scrollingPercentage)}`
"""
@app.route('/PageLog', methods=['POST'])
def receivePageLog():
    # 쿼리 파라미터 추출
    try:
        currentDateTime = request.args.get('currentDateTime')
        timeSpent = request.args.get('timeSpent')
        currentUrl = request.args.get('currentUrl')
        userVisitCookie = request.args.get('userVisitCookie')
        newVisiter = request.args.get('newVisiter')
        scrollingPercentage = request.args.get('scrollingPercentage')
    except Exception:
        print("Failed to receive log")
        
    print(currentDateTime)
    print(timeSpent)
    print(currentUrl)
    print(userVisitCookie)
    print(newVisiter)
    print(scrollingPercentage)
    
    ret = pageLogProcess(currentDateTime, timeSpent, currentUrl, userVisitCookie, newVisiter, scrollingPercentage)
    
    if ret == False:
        print("Failed to pageLogProcess")
    
    # 로그가 잘 수신되었다는 응답 반환
    return 'OK', 200



""" 자바스크립트에서 fetch로 쿼리 던지는 형태 참고할 것
    fetch(`http://localhost:5000/EventLog?dateTime=${encodeURIComponent(pushReReservDateTime)}
    &cookie=${encodeURIComponent(mypageCookie)}&uri=${encodeURIComponent(uri)}&clickItem=${encodeURIComponent(clickItem)`
"""
@app.route('/EventLog', methods=['POST'])
def receiveEvnetLog():
    # 쿼리 파라미터 추출
    try:
        currentDateTime = request.args.get('dateTime')
        userVisitCookie = request.args.get('cookie')
        uri = request.args.get('uri')
        clickItem = request.args.get('clickItem')
    except Exception:
        print("Failed to receive log")
        
    print(currentDateTime)
    print(userVisitCookie)
    print(uri)
    print(clickItem)
    
    ret = eventLogProcess(currentDateTime, userVisitCookie, uri, clickItem)
    
    if ret == False:
        print("Failed to pageLogProcess")
    
    # 로그가 잘 수신되었다는 응답 반환
    return 'OK', 200






if __name__ == '__main__':
    # Flask 애플리케이션 실행
    app.run(debug=True, port=5000)


