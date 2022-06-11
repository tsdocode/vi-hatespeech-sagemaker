import streamlit as st
import boto3
import os
from dotenv import load_dotenv

from sagemaker.huggingface import HuggingFacePredictor
from sagemaker.session import Session
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

import seaborn as sn
import matplotlib.pyplot as plt

load_dotenv()

@st.cache(allow_output_mutation=True)
def load_endpoint():
    sagemaker_session = Session(boto_session=boto3.session.Session())

    predictor = HuggingFacePredictor(
        endpoint_name=os.getenv('SAGEMAKER_ENDPOINT'), 
        sagemaker_session=sagemaker_session
    )

    return predictor


def predict(text, predictor):
    predicition = predictor.predict({"inputs": text})
    print(predicition)

    if len(predicition) > 1:
        return predicition
    else:
        return predicition[0]



CLASS_NAME = {
    'LABEL_0' : "Bình thường",
    'LABEL_1' : "Công kích",
    'LABEL_2' : "Thù ghét"
}

TEST_CLASS_NAME = {
    '0' : "Bình thường",
    '1' : "Công kích",
    '2' : "Thù ghét"
}




def main():
    st.title('Hate Speech Detection')
    ui = st.sidebar.selectbox('', ['METRICS', 'Hate Speech Detection'])

    predictor = load_endpoint()
    result = pd.read_csv('result.csv')


    confusion_matrix = pd.crosstab(result['label'], result['pred'], rownames=['Actual'], colnames=['Predicted'])

    if ui == 'METRICS':
        fig, ax = plt.subplots(figsize=(5, 5))

        st.subheader("Accuracy")
        st.write(accuracy_score(result['label'], result['pred']))

        st.subheader("Confusion Matrix")

        sn.heatmap(confusion_matrix, annot=True)
        st.write(fig)   

        st.subheader("Metrics")


        report = classification_report(result['label'], result['pred'], target_names=CLASS_NAME.values(), digits=4, output_dict=True)
        
        metrics = pd.DataFrame(report).transpose()
        print(report)
        st.table(metrics[:3])
    else:
        text = st.text_input(label='Input text')
        button = st.button(label='Kiểm tra')


        if button:
            result = predict(text, predictor)
            print(result)

            label = result['label']

            if '0' in label:
                st.info(CLASS_NAME[label])
            elif '1' in label:
                st.warning(CLASS_NAME[label])
            else:
                st.error(CLASS_NAME[label]) 


if __name__ == '__main__':
    main()

    
