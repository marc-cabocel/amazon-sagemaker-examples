import boto3
import io
import csv

session = boto3.Session(profile_name='Test')
sm = session.client('sagemaker')

r_training_params = {
    "RoleArn": "arn:aws:iam::542104878797:role/service-role/AmazonSageMaker-ExecutionRole-20180301T173668",
    "TrainingJobName": "test1",
    "AlgorithmSpecification": {
        "TrainingImage": '542104878797.dkr.ecr.eu-west-1.amazonaws.com/r_training_inference:latest',
        "TrainingInputMode": "File"
    },
    "ResourceConfig": {
        "InstanceCount": 1,
        "InstanceType": "ml.m4.xlarge",
        "VolumeSizeInGB": 10
    },
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": "s3://marc-stationf-sagemaker/demoR/data/training/",
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            "CompressionType": "None",
            "RecordWrapperType": "None"
        }
    ],
    "OutputDataConfig": {
        "S3OutputPath": "s3://marc-stationf-sagemaker/demoR/models/"
    },
    "HyperParameters": {
        "target": "Sepal.Length",
        "degree": "2"
    },
    "StoppingCondition": {
        "MaxRuntimeInSeconds": 60 * 60
    }
}

sm.create_training_job(**r_training_params)
