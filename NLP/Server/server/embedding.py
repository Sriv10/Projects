import pandas as pd

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import GridSearchCV

embeddingModel = SentenceTransformer("dunzhang/stella_en_1.5B_v5", trust_remote_code=True)

df = pd.read_csv("cleanedData.csv")
df = df.sample(n=100000)
print(df.shape)
plays = list(df['desc'])
winPercentages = list(df['wpa'])


playEmbeddings = embeddingModel.encode(plays)
print(playEmbeddings.shape)
print("Finished Training Embeddings")

X_train, X_test, y_train, y_test = train_test_split(playEmbeddings, winPercentages, test_size=.3, random_state=42)

# Implement Grid Search CV
model = xgb.XGBRegressor(learning_rate=0.1, max_depth = 3, reg_lambda = .5, alpha = .5, verbose_eval=True)
model.fit(X_train, y_train)

model.save_model("xgb_model.json")
print("Finished training, saved model")

'''
predictions = model.predict(X_test)
print(y_test)
for x in range(3):
    print(plays[6+x], winPercentages.iloc[6+x], predictions[x])

mse = mean_squared_error(y_test, predictions)
'''

# Embed Test Data
# testDf = pd.read_csv("testingData.csv")

# testPlays = testDf['desc']
# testWinPercentages = testDf['wpa']

# testPlayEmbeddings = embeddingModel.encode(testPlays)
# print(testPlayEmbeddings.shape)
# print("Finished Testing Embeddings")

# output = []
# predictions = model.predict(testPlayEmbeddings)
# for x in range(len(predictions)):
#     output.append((testPlays[x], predictions[x], testWinPercentages[x]))


# top10 = testDf.sort_values(by='wpa', ascending=False)
# print("TOP 10")
# print(top10.head(10))


# print("MY PLAYS")
# output.sort(key = lambda x: x[1], reverse=True)
# for play, prediction, wpa in output[:10]:
#     print(play, prediction, wpa)
    

#ndcg
#accuracy
#mse = mean_squared_error(predictions, testWinPercentages)

#print(f"Mean Squared Error: {mse}")