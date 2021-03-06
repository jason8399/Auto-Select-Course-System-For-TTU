# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.response
import urllib.error
import http.cookiejar
import http.client
import platform
import os
import time
import getpass


def showMenu():
    print('Welcome To Use ASCS for TTU')
    print('Please Selected The function')
    print('1.Select Course Process')
    print('2.Read Selected Course <dev>')
    print('5.Exit')


def clrscr():
    system = platform.system()
    if system.lower() == 'windows':
        os.system('cls')
    elif system.lower() == 'darwin':
        os.system('clear')


def webDecodeBig5(web_string):  # web資料Decode BIG5
    web_string = web_string.read()
    return web_string.decode('big5')


def Login():
    x = True
    while x:
        clrscr()
        ID = input('Please input student ID: ')
        PWD = getpass.getpass('Please input Password: ')
        data = {'ID': ID, 'PWD': PWD, 'Submit': '登入系統'}
        data = urllib.parse.urlencode(data)
        data = data.encode('big5')
        req = urllib.request.Request(url_login, data, header, None, None, 'POST')
        # print(urllib.request.urlopen(req).getheaders())
        # print(time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime()) + ' GMT')
        if '登入錯誤' in webDecodeBig5(urllib.request.urlopen(req)):
            print('failed')
            x = True
        else:
            print('success!!!!')
            x = False
        input('Please press any key to continue......')


def readSelectedList():  # Select Course List
    req = urllib.request.Request(url_listed, None, header, None, None, 'GET')
    u = urllib.request.urlopen(req)
    web_string = webDecodeBig5(urllib.request.urlopen(req))
    if 'Not login or session expire!' in web_string:
        print('You need to Login again........\n')
        Login()
        readSelectedList()
    else:
        print(web_string)


def selectCourse():
    flag = True
    while (flag):
        clrscr()
        print('Please Check "list.txt" is under same folder')
        input('Please press any key to continue......')
        try:
            selectList = open('list.txt')
            flag = False
        except Exception:
            print('Open "list.txt" fail.\nPlease Check Your file')
            input('Please press any key to continue......')
            flag = True
    courseID = selectList.readlines()
    for x in range(0, len(courseID)):
        courseID[x] = courseID[x].strip('\n')
    YN = input('Do you want use CountDown function?(y/n)\n')
    if YN == 'Y' or YN == 'y':
        settime()
    req = urllib.request.Request(url_listed, None, header, None, None, 'GET')
    u = urllib.request.urlopen(req)
    for x in range(0, len(courseID)):
        selectID_url = url_select + 'AddSbjNo=' + courseID[x]
        # print(selectID_url)
        while True:
            try:
                req = urllib.request.Request(selectID_url, None, header, None, None, 'GET')
                u = urllib.request.urlopen(req)
                # web_string = webDecodeBig5(u)
                print(u.status)
                # print(u.getheaders())
                # print(web_string)
                print('Select suecced')
                break
            except urllib.error.HTTPError as err:
                print(err.reason)
                print('retry select ' + courseID[x])


def settime():
    flag = True
    while flag:
        user_Time_Str = input('Please input YYYY/MM/DD HH:MM:SS\n')
        user_Time_Str += ' GMT +0800'
        try:
            time_set = time.strptime(user_Time_Str, '%Y/%m/%d %H:%M:%S %Z %z')
            temp = list(time_set)
            time_set = time.struct_time(tuple(temp))
            if time_set < time.localtime():
                raise Exception
            flag = False
        except Exception:
            print('Set time ERROR\ntry again.\n')
    time_set_str = time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(user_Time_Str, '%Y/%m/%d %H:%M:%S %Z %z'))
    while True:
        time_Temp = time.localtime()
        while True:
            if time_Temp < time.localtime():
                break
        clrscr()
        print('Now Time Is  ' + time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
        print('The Time Set ' + time_set_str)
        if time.localtime() > time_set:
            break
    print('time up!!!!!!')

if __name__ == "__main__":
    url_login = 'http://stucis.ttu.edu.tw/login.php'
    url_listed = 'http://stucis.ttu.edu.tw/selcourse/ListSelected.php'
    url_select = 'http://stucis.ttu.edu.tw/selcourse/DoAddDelSbj.php?'
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1897.3 Safari/537.36'}
    cookie = http.cookiejar.CookieJar()
    flag = True

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))  #cookie處理
    urllib.request.install_opener(opener)

    Login()
    while True:
        clrscr()
        showMenu()
        select = input('select = ')
        if select == '1':
            selectCourse()
        elif select == '2':
            readSelectedList()
        elif select == '5':
            print('\n\nGood Bye!!!!')
            exit(0)
