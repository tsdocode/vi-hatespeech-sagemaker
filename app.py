import streamlit as st
import boto3

from sagemaker.huggingface import HuggingFacePredictor
from sagemaker.session import Session


@st.cache(allow_output_mutation=True)
def load_endpoint():
    sagemaker_session = Session(boto_session=boto3.session.Session())

    predictor = HuggingFacePredictor(
        endpoint_name='huggingface-pytorch-inference-2022-05-07-04-03-22-044', 
        sagemaker_session=sagemaker_session
    )

    return predictor


def predict(text, predictor):
    predicition = predictor.predict({"inputs": text})[0]

    return predicition


CLASS_NAME = {
    'LABEL_0' : "Bình thường",
    'LABEL_1' : "Công kích",
    'LABEL_2' : "Thù ghét"
}




def main():
    st.title('Hate Speech Detection')

    predictor = load_endpoint()

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

    
