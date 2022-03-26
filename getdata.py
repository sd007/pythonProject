
# 获取烂番茄全部评论

# coding：utf-8
import requests
import json
import xlwt
import time



dates = []
reviews = []
allReviews = []
reviewerOrigins =[]
reviewers = []
websites = []


#获取网络响应请求的数据URL，改一下

#topic
#urlpre = 'https://www.rottentomatoes.com/napi/movie/7e63963f-6cf7-4077-8577-3c2d92ee5e0b/criticsReviews/top_critics/:sort?&direction=next&'

#全部
urlpre = 'https://www.rottentomatoes.com/napi/movie/2eb14a80-6921-3cd5-b2a0-960cec34aeee/criticsReviews/all?direction=next&'
cursorparam = 'endCursor=undefined&startCursor=undefined'


isFirstPage = True
hasNextPage = True
while hasNextPage:

    url = urlpre + cursorparam
    data = requests.get(url).text
    if len(data) <= 0:
        break
    
    jsondata = json.loads(data)   

    pageinfo = jsondata['pageInfo']

    if isFirstPage :
        endcursor = 'MQ=='
        startcursor = ''
        isFirstPage = False
    else:
        for i in pageinfo:
            if i == 'endCursor' :
                endcursor = jsondata['pageInfo']['endCursor']
            if i == 'startCursor' :
                startcursor = jsondata['pageInfo']['startCursor']

    reviewsList = jsondata['reviews']

    for reviewone in reviewsList:    
        reviewer = reviewone['critic']['name']    
        reviewers.append(reviewer)  

        review = reviewone['quote']    
        reviews.append(review)
        
        if 'reviewUrl' in reviewone:
            review_url = reviewone['reviewUrl']    
            websites.append(review_url)
    
        reviewerOrigin = reviewone['publication'] ['name']   
        reviewerOrigins.append(reviewerOrigin)

        reviewdate = reviewone['creationDate']
        dates.append(reviewdate)    

    cursorparam = 'endCursor='+ endcursor + '&startCursor='+startcursor
    hasNextPage = jsondata['pageInfo']['hasNextPage']

#写文件
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = book.add_sheet('mulan',cell_overwrite_ok=True)
sheet.write(0,0,'Reviewer')
for i in range(0, len(reviewers)):
    sheet.write(i+1,0,reviewers[i]) 

sheet.write(0,1,'ReviewerOrigin')
for i in range(0, len(reviewerOrigins)):
    sheet.write(i+1,1,reviewerOrigins[i]) 

sheet.write(0,2,'reviews')
for i in range(0, len(reviews)):
    sheet.write(i+1,2,reviews[i]) 

sheet.write(0,3,'Website')
for i in range(0, len(websites)):
    sheet.write(i+1,3,websites[i]) 

sheet.write(0,4,'Date')
for i in range(0, len(dates)):
    sheet.write(i+1,4,dates[i]) 

book.save('/Users/xxx/Desktop/python/test.xls')
