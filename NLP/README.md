# CS 410: NFL Game Summarizer
## SETUP
### UI Bundling
To get the UI working follow these steps
1. Navigate to ui/src/
2. Run **npm i**
3. Run **npm run dev**
4. Navigate to the URL displayed on the console and select a game


### Server Bundling
To get the backend server running
1. Install all of the required packages
2. Download the data from https://www.kaggle.com/datasets/maxhorowitz/nflplaybyplay2009to2016
3. Run jupyter notebook and execute the code required to generate cleanedData.csv
4. If you want to override the model, run **python3 embedding.py**
5. Navigate to server/server and run **fastapi dev server.py**

## High Level Documentation
1. I have provided a pretrained xgboost model to process api requests
2. The server filters all of the data based off of the selected game
3. Text embeddings are then generated which the model then uses to predict the most impactful plays
4. I calculate ndcg@10 and accuracy alongside the predicted WPA which is then displayed on the front end
