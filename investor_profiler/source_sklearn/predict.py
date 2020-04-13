import os
from io import StringIO, BytesIO
import argparse

from google.oauth2 import service_account

import numpy as np
import pandas as pd
import pandas_gbq
import s3fs

import sagemaker
from sagemaker_inference import encoder

# clustering algorithms
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

# save the model
from sklearn.externals import joblib

from utils import feature_extraction_individual_address

# accepts and returns json data
CONTENT_TYPE_INPUT = 'text/plain'
CONTENT_TYPE_OUTPUT = 'application/json'


# Model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")

    # load using joblib
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    print("Done loading model.")

    return model

def input_fn(serialized_input_data, content_type):
    print('Deserializing the input data.')
    if content_type == CONTENT_TYPE_INPUT:
        return serialized_input_data.decode('utf-8')
    raise Exception('Requested unsupported ContentType in content_type: ' + content_type)
    
def output_fn(prediction_output, accept):
    print('Serializing the generated output.')
    if accept == CONTENT_TYPE_OUTPUT:
          return encoder.encode(prediction_output, accept)
    raise Exception('Requested unsupported ContentType in Accept: ' + accept)
    
def predict_fn(input_data, model):
    print('Extracting features for the address instance')
    instance_features = feature_extraction_individual_address(input_data)
    print('Predicting cluster for the input data...')
    prediction = model.predict(instance_features)[0]
    return prediction
