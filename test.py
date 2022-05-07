import boto3

from sagemaker.huggingface import HuggingFacePredictor
from sagemaker.session import Session

sagemaker_session = Session(boto_session=boto3.session.Session())

predictor = HuggingFacePredictor(
    endpoint_name='huggingface-pytorch-inference-2022-05-07-04-03-22-044', sagemaker_session=sagemaker_session
)

prediciton = predictor.predict({"inputs": 'hello'})[0]


print(prediciton)