#!/usr/local/bin/python3.7

import boto3
import io
import csv
import pandas as pd
import json

# Set below parameters
endpointName = 'Inference-MARS'
session = boto3.Session(profile_name='Test')
runtime = session.client('runtime.sagemaker')

# Read Data
iris = pd.read_csv('iris.csv')
iris = iris[:3]
payload = iris.drop(['Sepal.Length'], axis=1).to_csv(index=False)

response = runtime.invoke_endpoint(EndpointName=endpointName,
                                   ContentType='text/csv',
                                   Body=payload)

result = json.loads(response['Body'].read().decode())
print(result[0])
