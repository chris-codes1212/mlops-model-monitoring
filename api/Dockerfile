# Select base python image
FROM python:3.11-slim

# set working directory inside container
WORKDIR /api

# copy the requirements.txt file into the container
COPY requirements.txt .

# Intall the Python dependencies
RUN pip install -r requirements.txt

# Install Uvicorn
RUN pip install uvicorn

# Copy the application code into the container
COPY main.py .

# Copy the model pipeline into the container
COPY sentiment_model.pkl .

# # Copy the data into the container
# COPY ../data/test.txt .

# Expose the port that FastAPI runs on (default is 8000)
EXPOSE 8000

# Define command to run the application when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]