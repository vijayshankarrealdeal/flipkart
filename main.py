from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get('/instagram')
def hello():
    df = pd.read_csv('./data.csv')
    data = df.T.to_dict()
    return [data[i] for i in range(len(data))]

