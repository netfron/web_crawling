from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import json
import os, sys
from scrapy import Spider

def getURL(categoryNo, p):

    udemy = "https://www.udemy.com/api-2.0/channels/"+str(categoryNo)+"/courses?is_angular_app=true&is_topic_filters_enabled=false&p="+str(p)
    html = urlopen(udemy)
    soup = BeautifulSoup(html, 'html.parser')
    newDict=json.loads(str(soup))
    return newDict

#print(soup.prettify())
#print(newDict['results'])

def main():
        
    categoryNo = 1640 #Development Category, 7468 lectures
    newDict = getURL(categoryNo,1)
    totalPage = int(newDict['pagination']['total_page'])
    resultData = pd.DataFrame()

    for page in range(1, totalPage):

        for Data in newDict['results']:
            title = Data['title']
            headline = Data['headline']    
            url = Data['url']
            isPaid = Data['is_paid']
            subscribers = Data['num_subscribers']
            instructorName = Data['visible_instructors'][0]['name']
            instructorJobTitle = Data['visible_instructors'][0]['job_title']
            instructorsData = Data['visible_instructors']

            price = ''
            originalPrice = ''
            discountPrice = ''
            discountRate = ''

            if Data.get('discount'):
                price = Data['discount']['price']['price_string']
                originalPrice = Data['discount']['list_price']['price_string']
                discountPrice = Data['discount']['saving_price']['price_string']
                discountRate = Data['discount']['discount_percent_for_display']
            
            if(price==''):
                price = Data['price']

            reviews = Data['num_reviews']
            totalLessonCnt = Data['num_published_lectures']
            level = Data['instructional_level']
            contentLengths = Data['content_info']
            publishedTime = Data['published_time']
            relevancyScore = Data['relevancy_score']
            avgRatingRecent = Data['avg_rating_recent']
            bestseller = Data['bestseller_badge_content']
            contentLocale = Data['locale']
            captionLanguages = Data['caption_languages']

            resultData = resultData.append(
                {'title':title,'headline':headline,'url':url,'is_paid':isPaid,'subscribers':subscribers,'instructor_name':instructorName,'instructor_job_title':instructorJobTitle,'instructors_data':instructorsData,'price':price,'original_price':originalPrice,'discount_price':discountPrice,'discount_rate':discountRate,'reviews':reviews,'total_lesson_cnt':totalLessonCnt,'level':level,'content_lengths':contentLengths,'published_time':publishedTime,'relevancy_score':relevancyScore,'avg_rating_recent':avgRatingRecent,'bestseller':bestseller,'content_locale':contentLocale,'caption_languages':captionLanguages}, 
                ignore_index=True
            )

        newDict = getURL(categoryNo, page+1)

    excelOutPath = os.path.dirname(os.path.realpath(sys.argv[0])) + '\\result.xlsx'
    print(excelOutPath)
    writer = pd.ExcelWriter(excelOutPath, engine='xlsxwriter')
    resultData.to_excel(writer, "Sheet1", index=False)
    writer.save()

if __name__ == '__main__':
    main()