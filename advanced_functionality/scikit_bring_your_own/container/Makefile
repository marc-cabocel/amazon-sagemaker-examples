all: run

# This makefile contains some convenience commands for deploying and publishing.

# For example, to build and run the docker container locally, just run:
# $ make

# or to publish the :latest version to the specified registry as :1.0.0, run:
# $ make publish version=1.0.0

training_job_name = TrainingDecisionTree
profile = Test
bucket = marc-stationf-sagemaker

training:
		$(call blue, "building code...")
		aws sagemaker create-training-job \
    --training-job-name ${training_job_name} \
    --algorithm-specification \
        TrainingImage=542104878797.dkr.ecr.eu-west-1.amazonaws.com/decision_trees:latest,TrainingInputMode=File \
    --role-arn arn:aws:iam::542104878797:role/service-role/AmazonSageMaker-ExecutionRole-20180301T173668 \
    --input-data-config \
			'{"ChannelName":"training", \
           "DataSource":{"S3DataSource":{"S3DataType":"S3Prefix", \
                                         "S3Uri":"s3://marc-stationf-sagemaker/data/training/", \
                                         "S3DataDistributionType":"FullyReplicated" \
                                         } \
                         } \
           }' \
		--output-data-config \
        S3OutputPath=s3://${bucket}/models/ \
    --resource-config \
        InstanceType=ml.m4.xlarge,InstanceCount=1,VolumeSizeInGB=1 \
    --stopping-condition \
        MaxRuntimeInSeconds=86400 \
    --hyper-parameters \
        max_leaf_nodes=5 \
		--profile ${profile}

load:
		$(call blue, "reloading process_billboard.zip...")
		aws s3 cp ./deployment/dist/ s3://${bucket}/media-analysis-solution/${version}/ \
		--recursive \
		--acl bucket-owner-full-control \
		--profile ${profile}

create:
	$(call blue, " stack ${stackname}")
	aws cloudformation create-stack --stack-name ${stackname} --template-body file://${CFTemplate} --parameters \
		ParameterKey=Email,ParameterValue=${email} \
		ParameterKey=Size,ParameterValue=${size} \
		ParameterKey=SendAnonymousData,ParameterValue=${sendanonymousdata} \
		--capabilities CAPABILITY_NAMED_IAM \
		--profile ${profile}

validate:
	$(call blue, "Validate stack ${stackname}")
	aws cloudformation validate-template --template-body file://${CFTemplate} --profile ${profile}

update:
	$(call blue, "Updating stack ${stackname}")
	aws cloudformation update-stack --stack-name ${stackname} --template-body file://${CFTemplate} --parameters \
		ParameterKey=KeyName,ParameterValue=${keyname} \
		--capabilities CAPABILITY_IAM \
		--profile ${profile}

delete:
	$(call blue, "Updating stack ${stackname}")
	aws cloudformation delete-stack --stack-name ${stackname} --profile ${profile}

clean:
	@rm -f app

define blue
	@tput setaf 6
	@echo $1
	@tput sgr0
endef
