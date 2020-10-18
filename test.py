from fastapi import FastAPI, Query, Body
import uvicorn

test = FastAPI()


@test.get('/')
async def test1(
        name: str
):
    return name

if __name__ == '__main__':
    uvicorn.run('test:test', port=4001, debug=False)