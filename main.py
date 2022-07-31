from fastapi import FastAPI
import pandas as pd
from fastapi.staticfiles import StaticFiles
from instagram import runScript
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq
import numpy as np
import tensorflow as tf
from keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics.pairwise import pairwise_distances

df_embs = pd.read_csv('embedding.csv')
img_width, img_height, _ = 224, 224, 3
model = tf.keras.models.load_model('saved_model')


pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ["clothing", "shoe", "shirt", "trouser",
           "nike"]  # list of keywords to get data
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
data = pytrends.related_queries()
top = pd.DataFrame(data['clothing']['top']).iloc[:-1]
top.value = top.value.apply(lambda x: int(x))
raising = pd.DataFrame(data['clothing']['rising'])


app = FastAPI()
app.mount("/files", StaticFiles(directory="files"), name="files")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        return {'code': '400'}


@app.get('/trends')
def searchTrends():
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ["clothing", "shoe", "shirt", "trouser",
               "nike"]  # list of keywords to get data
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
    data = pytrends.related_queries()
    top = pd.DataFrame(data['clothing']['top']).iloc[:-1]
    top.value = top.value.apply(lambda x: int(x))
    top.columns = ['itemName', 'famous']
    #raising = pd.DataFrame(data['clothing']['rising'])
    return [top.T.to_dict()[i] for i in range(len(top))]


pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ["clothing", "shoe", "shirt", "trouser",
           "nike"]  # list of keywords to get data
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
data = pytrends.related_queries()
top = pd.DataFrame(data['clothing']['top']).iloc[:-1]
top.value = top.value.apply(lambda x: int(x))
raising = pd.DataFrame(data['clothing']['rising'])


app = FastAPI()
app.mount("/files", StaticFiles(directory="files"), name="files")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_embeddingxx(model, img_name):
    img = image.load_img(img_name, target_size=(img_width, img_height))
    x   = image.img_to_array(img)
    x   = np.expand_dims(x, axis=0)
    x   = preprocess_input(x)
    return model.predict(x).reshape(-1)


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
        return {'code': '400'}

'''
Similar Item predict
'''

@app.get('/getsimilaritem')
def getsimilaritem(photoname:str):
    data = pd.read_csv('fdata.csv')
    emb = get_embeddingxx(model,f'./files/{photoname}.jpg')
    t = 1-pairwise_distances(X = df_embs,Y = emb.reshape(1, -1) , metric='cosine')
    img = []
    for index,item in enumerate(t.squeeze()):
        if item > 0.7:
            k = {}
            k['img'] = data.img[index]
            k['title'] = data.title[index]
            k['price'] = int(data.price[index])
            k['rating'] = data.rating[index]
            k['link'] = data.link[index]
            img.append(k)        
    return img




@app.get('/trends')
def searchTrends():
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ["fashion", "shoe", "shirt", "trouser",
               "nike"]  # list of keywords to get data
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
    data = pytrends.related_queries()
    top = pd.DataFrame(data['fashion']['top']).iloc[:-1]
    top.value = top.value.apply(lambda x: int(x))
    top.columns = ['itemName', 'famous']
    #raising = pd.DataFrame(data['clothing']['rising'])
    return [top.T.to_dict()[i] for i in range(len(top))]
