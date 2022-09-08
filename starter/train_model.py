# Script to train machine learning model.
#
from sklearn.model_selection import train_test_split

# Add the necessary imports for the starter code.
from ml.data import load_data, clean_data, process_data
from ml.model import train_model
from os import environ as env
# import pickle
import joblib
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO)

# Add code to load in the data.
#root_dir = '/content/'
#
root_dir = env['GITHUB_WORKSPACE']
path_file = root_dir + '/data/census.csv'

# ***** Add code to load in the data. 
data_l = load_data(path_file)
data = clean_data(data_l)

# Optional enhancement, use K-fold cross validation instead of a train-test split.
train, test = train_test_split(data, test_size=0.20)
#
cat_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]
X_train, y_train, encoder, lb = process_data(
    train, categorical_features=cat_features, label="salary", training=True
)

# Proces the test data with the process_data function.

# Train and save a model.
model=train_model(X_train, y_train)
#
logging.info("Saving Model...")
print("Saving Model...")

joblib.dump(model, "random_forest.joblib")

logging.info("Saving Model2...")
print("Saving Model2...")

filename = 'rfc_model.joblib'
joblib.dump(model, open(root_dir+filename, 'wb'))

filename1 = '/model/encoder.joblib'
joblib.dump(encoder, open(root_dir+filename1, 'wb'))
#
filename2 = '/model/lb.joblib'
joblib.dump(lb, open(root_dir+filename2, 'wb'))

f=open('readme.txt', 'x')
with open('readme.txt', 'w') as f:
    f.write('Create a new text file!')



