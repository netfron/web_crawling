#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import json
import sys  
#reload(sys)  
#sys.setdefaultencoding('utf8')
import urllib2
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import requests, re

def getURL(date, page):
    url_part1 = 'http://dart.fss.or.kr/dsac001/mainAll.do?selectDate='
    url_part2 = '&sort=&series=&mdayCnt=0&currentPage='
    url = url_part1 + date + url_part2 + str(page)

    res = requests.get(url)
    body = res.text.encode('utf-8')
    soup = bs(body, 'html.parser')

    return soup

def getTotalRow(soup):
    totNum = soup.find_all('p')[8].text.encode('utf-8')
    totNum = re.sub("\\[.*\\] \\[","",totNum)
    totNum = re.sub(u"\ucd1d","",totNum)
    totNum = re.sub("\\]","",totNum)
    totNum = totNum.replace('총 ','')
    totNum = totNum.replace('건','')
    totNum = int(totNum)
    return totNum

date = '2016.07.13'
soup = getURL(date, 1)

#전체 개수 및 페이지 번호 생성
totNum = getTotalRow(soup)
totPage = int(totNum / 100)+1

resultData = pd.DataFrame()
resultData = resultData.append(
    {'pubTime':'','ComName':'','Cat':'','colID':'','Content':'','reqDate':'','pubDate':'','rcpNo':'','reportComName':''}, 
    ignore_index=True
)

for page in range(1, totPage+1):
    soup = getURL(date, page)
    totNum = getTotalRow(soup)
    tempNumCont = len(soup.find_all("tr"))

    for j in range(1, tempNumCont):
            
        #공시일자
        pubDate = date
        #공시시간
        pubTime = soup.find_all("tr")[j].find_all("td",class_="cen_txt")[0].text.strip()
        #회사명
        ComName = soup.find_all("tr")[j].find("a").text.encode('utf-8').strip()
        #유권시장
        Cat = soup.find_all("tr")[j].find("img").get('title').encode('utf-8').strip()
        #시장번호
        testStr = soup.find_all("tr")[j].find("a").get('href').encode('utf-8').strip()
        colID = re.findall(r"[0-9]{8}",testStr)[0]
        #rcpNo
        list1 = soup.find_all("tr")[j].find_all("a")
        str1 = ''.join(str(e) for e in list1)
        #print str1
        #testStr = soup.find_all("tr")[j].find_all("a")
        rcpNo = re.findall(r"[0-9]{14}",str1)[0]
        #접수일자
        reqDate = soup.find_all("tr")[j].find_all("td")[4].text
        #제출인
        reportComName = soup.find_all("tr")[j].find_all("td")[3].text.encode('utf-8')
        #보고서명
        Content = soup.find_all("tr")[j].find_all('a')[1].text.encode('utf-8').strip()
        #print Content
        resultData = resultData.append(
            {
            'pubTime':pubTime,'ComName':ComName,'Cat':Cat,'colID':colID,'Content':Content,
            'reqDate':reqDate,'pubDate':pubDate,'rcpNo':rcpNo,'reportComName':reportComName
            }, 
            ignore_index=True
        )

#print resultData.head()

excelOutPath = 'C:/test_dart.xlsx'
writer = pd.ExcelWriter(excelOutPath, engine='xlsxwriter')
resultData.to_excel(writer, "Sheet1", index=False)
writer.save()
