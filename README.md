# mlops-model-monitoring

## Project Description
This repository contains two major directories, the 'api' directory and the 'monitoring' directory.

### FastAPI Component
The 'api' directory contains the code to run the FastAPI app. The primary endpoint of the FastAPI app is '/predict'. When using this endpoint, the user will provide an example movie review and the true sentiment of the example review (either 'positive' or 'negative'). The response from the app will be the predicted sentiment of the review. Refer to the 'Instructions' section of this README file for more information on testing.

### Streamlit Component
The 'monitoring' directory contains the code necessary to run the streamlit app. This streamlit app is a model-monitoring dashboard designed to provide visualizations to help identify data drift, concept drift, and reductions in accuracy and/or preceision related to the sentiment model making predictions from the '/predict' FastAPI endpoint.

Each of these directories, api and monitoring, contains their own unique dockerfiles to run the api and monitoring applications seperately, however their is a Makefile in the root directory which will build and run containers for the api and monitoring applications.

## Instructions
### Running the Applications
In order to run the applications, you must have docker installed. Following this, you can run the applications using commands below (as defined in the makefile):

To build the containers
```bash
make build
```

To run the containers
```bash
make run
```

If you wish to stop the containers and remove the images you can use the following make commands:

To stop the containers and remove them
```bash
make stop
```

To remove the images
```bash
make clean
```

### Testing the FastAPI Component 

In Postman or another API platform make a post request to the /predict FastAPI endpoint (ex: http://localhost:8000/predict if running locally) with a json formatted body like the following:

```json
{
    "text": "I thought it was a great movie. I really enjoyed the final scene.",
    "true_label": "positive"
}
```

You should see a response back that is the predicted sentiment:

```json
{
    "Sentiment": "positive"
}
```

### Testing the Streamlit (Model-Monitoring) Component

In your browser, http://host-ip-address:8501 to reach the dashboard and there you will be able to see the different visualizations and metrics for monitoring the model performance.

This application measures the models performance using data from the shared logs/ directory (shared with the FastAPI app). In order to quickly test the application as well as generate log data, run the evaluate.py script described below.

### Testing and Log Generation Using evaluate.py

The evaluate.py is a python script designed to repeatedly test the /predict FastAPI endpoint and generate log data. evaluate.py the test_data.json file with a list of hundreds of request body examples to send requests to the /predict FastAPI endpoint which will then send data to the logs file. You may update the url on line 10 of this file to one containing the appropriate IP address of the host machine:

If running locally:
```python
url = "http://localhost:8000/predict" 
```

To run evaluate.py:
```bash
python3 evaluate.py
```