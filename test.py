import mlflow.sklearn

import pickle

model_directory = 'model/random_forest_model.pkl'

with open(f'model/random_forest_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

print("okkk")