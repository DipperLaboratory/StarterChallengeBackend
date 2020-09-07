import datetime
import pickle
import threading

import requests
import uvicorn
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware

from func import *
from secret import github_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

apiurl = 'https://api.startcoder.top'


@app.get('/login')
async def login(username: str):
    userMd5 = hashlib.md5(username.encode()).hexdigest()
    try:
        with open('data/' + userMd5, 'rb') as f:
            userData = pickle.load(f)
    except:
        userData = {
            'step': 1,
            'user': username,
            'salt': userMd5,
        }
        with open('data/' + userMd5, 'wb') as f:
            pickle.dump(userData, f)
    returnBody = {
        "status": True,
        "data": {
            **userData
        },
    }
    return returnBody


@app.post('/challenge/1/email')
async def challenge1(
        *,
        username: str = Query(..., description='用户名'),
        content: str = Body(..., embed=True, description='发送的内容')
):
    # print('data/'+str(getHash(username)))
    with open('data/' + str(getHash(username)), 'rb') as f:
        userObject = pickle.load(f)
    try:
        lastSendEmailTime = userObject['emailTime']
        if datetime.now() - lastSendEmailTime < thirtySecondTime:
            return {'status': False, 'msg': '发送邮件频率过高，请30秒后重试'}
        else:
            userObject['emailTime'] = datetime.now()
            with open('data/' + str(getHash(username)), 'wb') as f:
                pickle.dump(userObject, f)
    except:
        userObject['emailTime'] = datetime.now()
        with open('data/' + str(getHash(username)), 'wb') as f:
            pickle.dump(userObject, f)
    if content.split('@')[1].lower() == 'gmail.com':
        threading.Thread(target=sendmail, kwargs={
            'msg': '挑战一的激活链接\r\n' \
                   + '请访问链接以完成挑战\r\n' \
                   + apiurl + '/auth?username=' + username \
                   + '&step=1' \
                   + '&code=' + getHash2(userObject['salt'], saltDict[1]) \
                   + '\r\n本邮件自动生成，请勿回复',
            'title': '挑战一',
            'receiver_address': content}).start()
        return {'status': True}
    else:
        return {'status': False, 'msg': '请提交有效 Gmail 地址'}


@app.post('/challenge/2/github')
async def challenge2(
        *,
        username: str = Query(..., description='用户名'),
        content: int = Body(..., embed=True, description='发送的内容')
):
    githubAPI = 'https://api.github.com/repos/DipperLaboratory/clockin/issues/'
    with open('data/' + str(getHash(username)), 'rb') as f:
        userObject = pickle.load(f)
    req = requests.get(githubAPI + str(content), params={'access_token': github_token})
    if req.ok:
        c2salt = req.json()['title']
        # print(userObject['salt'])
        if c2salt == getHash2(userObject['salt'], saltDict[2]):
            userObject['salt'] = c2salt
            userObject['step'] += 1
            with open('data/' + getHash(username), 'wb') as f:
                pickle.dump(userObject, f)
            return {'status': True}
        else:
            return {'status': False, 'msg': '无法验证'}
    else:
        return {'status': False, 'msg': '无法验证'}


@app.put('/challenge/3/http')
async def challenge3(
        *,
        username: str = Query(..., description='用户名'),
):
    with open('data/' + str(getHash(username)), 'rb') as f:
        userObject = pickle.load(f)
    if userObject['step'] == 3:
        userObject['salt'] = getHash2(userObject['salt'], saltDict[3])
        userObject['step'] += 1
        with open('data/' + getHash(username), 'wb') as f:
            pickle.dump(userObject, f)
        return ['挑战成功']
    else:
        return ['挑战失败或已完成']


@app.post('/challenge/4/email')
async def challenge4(
        *,
        username: str = Query(..., description='用户名'),
        content: str = Body(..., embed=True, description='发送的内容')
):
    # print('data/'+str(getHash(username)))
    with open('data/' + str(getHash(username)), 'rb') as f:
        userObject = pickle.load(f)
    lastSendEmailTime = userObject['emailTime']
    if datetime.now() - lastSendEmailTime < thirtySecondTime:
        return {'status': False, 'msg': '发送邮件频率过高，请30秒后重试'}
    else:
        userObject['emailTime'] = datetime.now()
        with open('data/' + str(getHash(username)), 'wb') as f:
            pickle.dump(userObject, f)
    if content.split('@')[1].lower() == 'jgsu.edu.cn':
        print(userObject['salt'])
        threading.Thread(target=sendmail, kwargs={
            'msg': '挑战四的激活链接\r\n' \
                   + '请访问链接以完成挑战\r\n' \
                   + apiurl + '/auth?username=' + username \
                   + '&step=4' \
                   + '&code=' + getHash2(userObject['salt'], saltDict[4]) \
                   + '\r\n本邮件自动生成，请勿回复',
            'title': '挑战四',
            'receiver_address': content}).start()
        return {'status': True}
    else:
        return {'status': False, 'msg': '请提交有效本校教育邮箱地址'}


@app.post('/challenge/5/domain')
async def challenge5(
        *,
        username: str = Query(..., description='用户名'),
        content: str = Body(..., embed=True, description='发送的内容')
):
    if (content == 'potplayer.daum.net'):
        with open('data/' + str(getHash(username)), 'rb') as f:
            userObject = pickle.load(f)
        if userObject['step'] == 5:
            userObject['salt'] = getHash2(userObject['salt'], saltDict[5])
            userObject['step'] += 1
            with open('data/' + getHash(username), 'wb') as f:
                pickle.dump(userObject, f)
            try:
                with open('data/gift', 'rb') as f:
                    giftObject = pickle.load(f)
            except:
                giftObject = {}
            # print(userObject['user'])
            # giftObject.append([userObject['user'],userObject['salt']])
            giftObject[userObject['user']] = userObject['salt']
            with open('data/gift', 'wb') as f:
                pickle.dump(giftObject, f)
            return {'status': True}
        else:
            return {'status': False, 'msg': '未知错误'}
    else:
        return {'status': False}


@app.get('/auth')
async def auth(
        username: str,
        code: str,
        step: int
):
    with open('data/' + str(getHash(username)), 'rb') as f:
        userObject = pickle.load(f)
    print(userObject['salt'])
    try:
        if code == getHash2(userObject['salt'], saltDict[userObject['step']]) and step == userObject['step']:
            userObject['salt'] = code
            userObject['step'] += 1
            with open('data/' + getHash(username), 'wb') as f:
                pickle.dump(userObject, f)
            return ['验证成功']
        else:
            return ['验证失败']
    except:
        return ['验证过期']



@app.get('/gift')
async def gift():
    with open('data/gift', 'rb') as f:
        return pickle.load(f)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    uvicorn.run('main:app', port=4001, debug=False)
