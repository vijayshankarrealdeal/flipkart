from fastapi import FastAPI
import pandas as pd
from fastapi.staticfiles import StaticFiles
from instagram import runScript


app = FastAPI()
app.mount("/files", StaticFiles(directory="files"), name="files")
@app.get('/instagram')

def hello():
    df = pd.read_csv('./data.csv')
    data = df.T.to_dict()
    return [data[i] for i in range(len(data))]
@app.get('/instagram/scape')
def scrape(keyword):
    runScript(keyword)
    try:
        df = pd.read_csv('./calldata.csv')
        data = df.T.to_dict()
        return [data[i] for i in range(len(data))]
    except Exception as e:
        return {'code':'400'}

