import streamlit as st
import boto3

from sagemaker.huggingface import HuggingFacePredictor
from sagemaker.session import Session
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

import seaborn as sn
import matplotlib.pyplot as plt


sagemaker_session = Session(boto_session=boto3.session.Session())

predictor = HuggingFacePredictor(
    endpoint_name='huggingface-pytorch-inference-2022-05-21-08-08-26-236', 
    sagemaker_session=sagemaker_session
)


def predict(text):
    predicition = predictor.predict({"inputs": text})
    print(predicition)

    if len(predicition) > 1:
        return predicition
    else:
        return predicition[0]

