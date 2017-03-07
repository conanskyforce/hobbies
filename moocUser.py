# -*- coding:utf-8 -*-
import requests
import re
import os
from bs4 import BeautifulSoup
import pymysql.cursors

def getUserinfos():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    # for a in range(1,20000):
    a = 1458226
    count = 212610
    while a < 4000000:
        url = "http://www.imooc.com/u/" + str(a) #初始页面
        response = requests.get(url, headers=headers)#获取页面
        if response.status_code == 404:
            a = a + 1
            continue
        soup = BeautifulSoup(response.text,'lxml')
        userId = count
        userName = soup.findAll('h3',{'class':{'user-name','clearfix'}})[0].find('span').get_text()#用户姓名
        userImg = soup.findAll('img',{'class':'img'})[0].attrs['src']#用户头像
        if soup.findAll('div',{'class':'teacher'}):#判断是学生还是老师
            teacherOrStudent = 'teacher'
        else:
            teacherOrStudent = 'student'
        userGender = soup.findAll('p',{'class':'about-info'})[0].find('span').attrs['title']#性别
        userSignature = soup.findAll('p', {'class': 'user-desc'})[0].get_text()#签名
        if len(userSignature)>100:
            a = a + 1
            continue
        if not soup.findAll('span', {'class': 'u-info-learn'}):
            a = a + 1
            continue
        userLearnTime = soup.findAll('span', {'class': 'u-info-learn'})[0].get_text().strip()#学习时长
        userLearnTime = userLearnTime[0:4] + ":" + userLearnTime[4:]
        userCredit = soup.findAll('span', {'class': 'u-info-credit'})[0].get_text().strip()#积分
        userCredit = userCredit[2:]
        userExpir = soup.findAll('span', {'class': 'u-info-mp'})[0].get_text().strip()  #经验
        userExpir = userExpir[2:]
        userfollows = soup.findAll('div', {'class': 'follows'})[0].get_text().strip()  # 关注
        userfollows = userfollows[0:-2].strip()
        userfollowers = soup.findAll('div', {'class': 'followers'})[0].get_text().strip()  # 粉丝
        userfollowers = userfollowers[0:-2].strip()
        userInfo = re.findall('p class="about-info">(.*?)class="u-info-learn"', response.text, re.S)[0]
        aboutinfo = re.findall('</span>(.*?)<span', userInfo, re.S)[0].strip().replace(" ","").replace("\n","")#职业信息
        if not aboutinfo:
            aboutinfo=""
        print(aboutinfo)
        f = open('moocUserInfos.txt', 'a+',encoding='utf-8')
        f.write("id: "+str(userId) + '\n'+"用户名: "+str(userName)+ '\n'+"用户头像: "+userImg+ '\n'+"身份: "+teacherOrStudent+ '\n'+"性别: "+userGender+ '\n'+"签名: "+str(userSignature)+ '\n'+"学习时长: "+userLearnTime+ '\n'+"积分: "+userCredit
                + '\n'+"经验: "+userExpir+ '\n'+"关注: "+userfollows+ '\n'+"粉丝: "+userfollowers+ '\n'+"关于: "+aboutinfo+ '\n'+ '---------'+'\n')
        f.close()
        try:
            connection = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='2010',
                db='moocinfos',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = connection.cursor()
            sql2 = "insert into moocuserinfos(userName,userImg,teacherOrStudent,userGender,userSignature,userLearnTime,userCredit,userExpir,userfollows,userfollowers,aboutinfo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql2, (userName, userImg,teacherOrStudent,userGender,userSignature,userLearnTime,userCredit,userExpir,userfollows,userfollowers,aboutinfo))
            connection.commit()
        finally:
            cursor.close()
            connection.close()
        count = count + 1
        print("第： ",a,"页",'\n','共计： ',count,"个信息")
        a = a + 1
if __name__ == '__main__':
    getUserinfos()