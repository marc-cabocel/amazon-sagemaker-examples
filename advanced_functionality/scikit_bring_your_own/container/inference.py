import boto3
import io
import csv

# Set below parameters
endpointName = 'InferenceDecisionTree'
session = boto3.Session(profile_name='Test')


# Convert the dataframe to csv data
test_file = io.BytesIO()
inference = ["6.4", "3.1",
             "5.5", "1.8"]

writer = csv.writer(test_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
writer.writerow(inference)


# Talk to SageMaker
client = session.client('sagemaker-runtime')
response = client.invoke_endpoint(
    EndpointName=endpointName,
    Body=test_file.getvalue(),
    ContentType='text/csv',
    Accept='Accept'
)

print(response['Body'].read())
