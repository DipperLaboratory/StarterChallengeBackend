import pickle
import hashlib
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/login')
async def login(username:str):
    userMd5 = hashlib.md5(username.encode()).hexdigest()
    try:
        with open('data/'+userMd5,'rb') as f:
            userData = pickle.load(f)
    except:
        userData = {
            'step':1,
        }
        with open('data/' + userMd5,'wb') as f:
            pickle.dump(userData,f)
    returnBody = {
        "status": True,
        "data":{
            'salt': userMd5,
            **userData
        },

    }
    return returnBody



# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    uvicorn.run('main:app',port=4000,debug=True)

