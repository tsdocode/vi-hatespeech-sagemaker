import streamlit as st
import boto3
from dotenv import load_dotenv
import os

from sagemaker.huggingface import HuggingFacePredictor
from sagemaker.session import Session
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

import seaborn as sn
import matplotlib.pyplot as plt



load_dotenv()

sagemaker_session = Session(boto_session=boto3.session.Session())

predictor = HuggingFacePredictor(
    endpoint_name=os.getenv('SAGEMAKER_ENDPOINT'), 
    sagemaker_session=sagemaker_session
)


def predict(text):
    predicition = predictor.predict({"inputs": text})
    print(predicition)

    if len(predicition) > 1:
        return predicition
    else:
        return predicition[0]

