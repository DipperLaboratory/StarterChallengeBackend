import pickle

import requests
import uvicorn
from fastapi import FastAPI, Query, Body
from fastapi.responses import HTMLResponse
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

apiurl = 'https://api.jgsu.xyz'


@app.get('/login')
async def login(username: str):
    userMd5 = hashlib.md5(username.encode()).hexdigest()
    try:
        with open('data/' + userMd5, 'rb') as f:
            userData = pickle.load(f)
    except FileNotFoundError:
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
    try:
        with open('data/' + str(getHash(username)), 'rb') as f:
            userObject = pickle.load(f)
    except FileNotFoundError:
        return {'status': False, 'msg': '用户不存在'}
    if content.split('@')[1] == 'gmail.com':
        sendmail(msg='挑战一的激活链接\r\n' \
                     + '请访问链接以完成挑战\r\n' \
                     + apiurl + '/auth?username=' + username \
                     + '&step=1' \
                     + '&code=' + getHash2(userObject['salt'], saltDict[1]) \
                     + '\r\n本邮件自动生成，请勿回复',
                 title='挑战一',
                 receiver_name=username,
                 receiver_address=content)
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
    try:
        with open('data/' + str(getHash(username)), 'rb') as f:
            userObject = pickle.load(f)
    except FileNotFoundError:
        return {'status': False, 'msg': '用户不存在'}
    req = requests.get(githubAPI + str(content), headers={'Authorization': f'token {github_token}'})
    if (req.ok):
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
    try:
        with open('data/' + str(getHash(username)), 'rb') as f:
            userObject = pickle.load(f)
    except FileNotFoundError:
        return {'status': False, 'msg': '用户不存在'}
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
    try:
        with open('data/' + str(getHash(username)), 'rb') as f:
            userObject = pickle.load(f)
    except FileNotFoundError:
        return {'status': False, 'msg': '用户不存在'}
    if content.split('@')[1] == 'jgsu.edu.cn':
        print(userObject['salt'])
        sendmail(msg='挑战四的激活链接\r\n' \
                     + '请访问链接以完成挑战\r\n' \
                     + apiurl + '/auth?username=' + username \
                     + '&step=4' \
                     + '&code=' + getHash2(userObject['salt'], saltDict[4]) \
                     + '\r\n本邮件自动生成，请勿回复',
                 title='挑战四',
                 receiver_name=username,
                 receiver_address=content)
        return {'status': True}
    else:
        return {'status': False, 'msg': '请提交有效本校教育邮箱地址'}


@app.post('/challenge/5/domain')
async def challenge5(
        *,
        username: str = Query(..., description='用户名'),
        content: str = Body(..., embed=True, description='发送的内容')
):
    if content == 'potplayer.daum.net':
        try:
            with open('data/' + str(getHash(username)), 'rb') as f:
                userObject = pickle.load(f)
        except FileNotFoundError:
            return {'status': False, 'msg': '用户不存在'}
        if userObject['step'] == 5:
            userObject['salt'] = getHash2(userObject['salt'], saltDict[5])
            # userObject['salt'] = 'expired'
            userObject['step'] += 1
            with open('data/' + getHash(username), 'wb') as f:
                pickle.dump(userObject, f)
            # try:
            #     with open('data/gift', 'rb') as f:
            #         giftObject = pickle.load(f)
            # except:
            #     giftObject = {}
            # # print(userObject['user'])
            # # giftObject.append([userObject['user'],userObject['salt']])
            # giftObject[userObject['user']] = userObject['salt']
            # with open('data/gift', 'wb') as f:
            #     pickle.dump(giftObject, f)
            return {'status': True}
        else:
            return {'status': False, 'msg': '未知错误'}
    else:
        return {'status': False}


@app.get('/auth', response_class=HTMLResponse)
async def auth(
        username: str,
        code: str,
        step: int,
):
    try:
        with open('data/' + str(getHash(username)), 'rb') as f:
            userObject = pickle.load(f)
    except FileNotFoundError:
        return {'status': False, 'msg': '用户不存在'}
    print(userObject['salt'])
    if code == getHash2(userObject['salt'], saltDict[userObject['step']]) and step == userObject['step']:
        userObject['salt'] = code
        userObject['step'] += 1
        with open('data/' + getHash(username), 'wb') as f:
            pickle.dump(userObject, f)
        return '<h1>验证成功</h1>'
    else:
        return '<h1>验证失败</h1>'


@app.get('/gift')
async def gift():
    try:
        with open('data/gift', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return '没人完成'


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=4001, debug=False)
