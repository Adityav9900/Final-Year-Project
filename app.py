# app.py (Streamlit Web Application)

import streamlit as st
import pandas as pd
import pickle
import os
from src.preprocess import preprocess_data

class ModelLoader:
    def __init__(self, model_path):
        self.model_path = model_path

    def load_model(self):
        if not os.path.exists(self.model_path):
            st.error(f"Error: Model file '{self.model_path}' not found.")
            st.stop()

        try:
            with open(self.model_path, 'rb') as model_file:
                model = pickle.load(model_file)
            return model
        except EOFError:
            st.error("Error loading the model: The file is empty.")
            st.stop()
        except Exception as e:
            st.error(f"Error loading the model: {e}")
            st.stop()

class StressPredictor:
    def __init__(self, model):
        self.model = model

    def predict_stress_level(self, data):
        prediction = self.model.predict(data)
        return prediction

class App:
    def __init__(self):
        self.model_loader = ModelLoader(model_path='models/svm_model.pkl')
        self.model = self.model_loader.load_model()
        self.stress_predictor = StressPredictor(model=self.model)

    def run(self):
        self.display_header()
        self.get_user_input()
        self.predict_stress_level()

    def display_header(self):
        st.title("Stress Detection System")
        st.write("Enter your physiological data to predict stress level:")

    def get_user_input(self):
        self.temp = st.number_input("Temperature", min_value=0, max_value=100, step=1, value=25)
        self.hr = st.number_input("Heart Rate", min_value=0, max_value=200, step=1, value=75)
        self.humidity = st.slider("Skin Conductance", min_value=0, max_value=100, value=50, step=1)

    def predict_stress_level(self):
        if st.button("Predict"):
            input_data = pd.DataFrame({
                'TEMP': [self.temp],
                'Heart Rate': [self.hr],
                'Humidity': [self.humidity]
            })
            stress_level = self.stress_predictor.predict_stress_level(input_data)
            self.display_result(stress_level)

    def display_result(self, stress_level):
        if stress_level[0] == 0:
            st.write("Predicted Stress Level: Low Stress")
        elif stress_level[0] == 1:
            st.write("Predicted Stress Level: Neutral Stress")
        elif stress_level[0] == 2:
            st.write("Predicted Stress Level: High Stress")

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
