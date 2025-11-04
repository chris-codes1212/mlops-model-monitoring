from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import joblib
import json
import os
import sklearn

# create FastAPI app
app = FastAPI(
    title="Sentiment Analysis API"
)

# try and load model, if not successful, print error message
try:
    model = joblib.load('sentiment_model.pkl')
    print("Model Loaded Successfull")
except FileNotFoundError:
    print("Error: Model file 'sentiment_model.pkl' not found.")
    model = None

# create a class for the /predict endpoint
class predict_input(BaseModel):
    text: str
    true_label: str

# create a class for the logs we will create
class log(BaseModel):
    timestamp: datetime
    request_text: str
    predicted_label: str
    true_label: str

# create a funciton to handle writing json logs
def write_logs(input_data, prediction):

    # create new log object
    new_log = log( 
        timestamp = datetime.now(),
        request_text = input_data.text,
        predicted_label = prediction[0],
        true_label = input_data.true_label
        )

    # format log object as a json object
    new_log_json = new_log.model_dump_json()
    
    # set log file path -- Using .jsonl b/c will be cleaner than using a list format
    file_path = "../logs/prediction_logs.ndjson"

    # check if logs directory exists, if not create it and logs file and write new log to file
    if not os.path.isdir("../logs"):
        os.makedirs("../logs", exist_ok=True)
        with open(file_path, "w") as log_file:
            log_file.write(new_log_json)
            return 

    # check if log file exists, if not, create it and write new log to file then return
    # also checks if file is empty, if so, write new log then return
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as log_file:
            log_file.write(new_log_json)
            return 
        
    # otherwise, write new log with new line
    else:
        existing_logs_list = []
        with open(file_path, "a") as log_file:
            log_file.write(f'\n{new_log_json}')

# create startup event to print if model is not loaded
@app.on_event("startup")
def startup_event():
    if model is None:
        print("WARNING: Model is not loaded. Prediction endpoints will not work properly")

# create health get endpoint to show 'status: ok' to confirm API is working
@app.get('/health')
async def root():
    return{'status': 'ok'}

# create predict endpoint to make predictions using loaded model
@app.post("/predict")
async def make_prediction(input_data: predict_input):

    # if model did not load properly, give 503 error
    if model is None:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = 'Model is not loaded. Cannot make predictions'
        )
    
    # turn input text into an array of words for correct model input data type
    text_array = [input_data.text]

    # make prediction with the model
    prediction = model.predict(text_array)
    
    # write new log to logs file by calling write_logs function
    write_logs(input_data, prediction)

    # return the prediction from the model
    return {'Sentiment': prediction[0]}