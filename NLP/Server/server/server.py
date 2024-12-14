from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import xgboost as xgb
import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer


# Set up server
app = FastAPI()
origins = ["http://localhost:5173"] 
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

model = xgb.XGBRegressor()
model.load_model('xgb_model.json')

df = pd.read_csv("cleanedData.csv")

embeddingModel = SentenceTransformer("dunzhang/stella_en_1.5B_v5", trust_remote_code=True)

@app.get("/game/")
async def game(gameId: int = 0):
    print(gameId)
    gameRows = df[df['game_id'] == int(gameId)]
    plays = list(gameRows['desc'])
    playIds = list(gameRows['play_id'])


    playEmbeddings = embeddingModel.encode(plays)
    predictions = model.predict(playEmbeddings)
    
    results = []
    for x in range(len(predictions)):
        results.append({"playId": playIds[x], "description": plays[x], "predictedWpa": str(predictions[x])})

    results.sort(key = lambda x: x["predictedWpa"], reverse=True)
    results = results[:10]

    top10 = gameRows.sort_values(by='wpa', ascending=False)
    top10plays = list(top10['play_id'])[:10]
    
    top10desc = list(top10['desc'])[:10]
    relevantItems = ['TOUCHDOWN', 'INTERCEPTED', 'SAFETY', 'PENALTY', 'FUMBLES', 'GOOD', 'No Good']
    
    print(top10)
    # calculate accuracy
    compare = []
    accuracy = 0
    for obj in results:
        if (obj['playId'] in top10plays):
            accuracy+=1
        found = False
        for item in relevantItems:
            if (item in obj["description"]):
                compare.append(1)
                found = True
                break
        if (not found):
            compare.append(0)

    accuracy = int((accuracy / 10) * 100)
    
    # calculate NDCG@10
    base = []
    for desc in top10desc:
        found = False
        for item in relevantItems:
            if (item in desc):
                base.append(1)
                found = True
                break
        if (not found):
            base.append(0)
    def dcg(arr): 
        arr = np.asfarray(arr)[:10] 
        return np.sum(arr / np.log2(np.arange(2, arr.size + 2))) 
    
    def idcg(arr): 
        arr.sort(reverse=True)
        arr = np.asfarray(arr)[:10] 
        return np.sum(arr / np.log2(np.arange(2, arr.size + 2))) 

    print(base)
    print(compare)
    ndcg = int((dcg(compare) / dcg(base)) * 100)
    return {"predictions": results, "accuracy": accuracy, "ndcg": ndcg}


@app.get("/games")
async def root():
    gameDescriptions = []
    for description in list(df["gameDescription"].unique()):
        gameDescriptions.append(description)
    return {"games": gameDescriptions}

