all: run

# This makefile contains some convenience commands for deploying and publishing.

# For example, to build and run the docker container locally, just run:
# $ make

# or to publish the :latest version to the specified registry as :1.0.0, run:
# $ make publish version=1.0.0


### General Config
profile = Test
region = eu-west-1
account_number = $(shell aws sts get-caller-identity --profile ${profile} | jq --raw-output '.Account')
bucket = marc-stationf-sagemaker
image = r-inference2
tag = latest
model_name = marc-test
random = $(shell echo $$RANDOM)
dockerfile = Dockerfile

### Training Parameters
training_job_name = MARS-${random}
training_image = ${account_number}.dkr.ecr.${region}.amazonaws.com/${image}:${tag}
training_input_mode = File
training_role_arn = arn:aws:iam::${account_number}:role/service-role/AmazonSageMaker-ExecutionRole-20180301T173668
training_instance_type = ml.m4.xlarge
training_instance_count = 1
training_instance_size = 10
training_path = demoR/data/training
model_path = demoR/models

### Inference parameters
inference_name = Inference-MARS
inference_instance_type = ml.m4.xlarge
inference_instance_count = 1

###############
#### Local ####
###############

### local_build
local_build:
		$(call blue, "building image...")
		./local_build.sh ${image} ${profile} ${tag} ${dockerfile}

### Local Training
local_training:
		$(call blue, "Locally testing container ...")
		cd ./local_test; ./train_local.sh ${image}

### Local prediction
local_serve:
		$(call blue, "Locally server ...")
		cd ./local_test; ./serve_local.sh ${image}

### Local inference
local_inference:
		$(call blue, "Locally running inference ...")
		cd ./local_test; ./predict.sh payload.csv

###############
#### Build ####
###############

### Build docker image and load it to ECR
build:
	  $(call blue, "building and pushing image...")
		./build_and_push.sh ${image} ${profile} ${tag} ${dockerfile}


##################
#### Training ####
##################

### Create S3 bucket
upload:
		$(call blue, "Create bucket ...")
		aws s3api put-object --bucket ${bucket} --key ${training_path}/iris.csv --body iris.csv --profile ${profile}

### Start Training Job
# Make sure training channel is well define in mars.R
training:
		$(call blue, "Create training job...")
		aws sagemaker create-training-job \
	  --training-job-name ${training_job_name} \
	  --algorithm-specification \
	      TrainingImage=${training_image},TrainingInputMode=${training_input_mode} \
	  --role-arn ${training_role_arn} \
	  --input-data-config \
			'{"ChannelName":"train", \
	         "DataSource":{"S3DataSource":{"S3DataType":"S3Prefix", \
	                                       "S3Uri":"s3://${bucket}/${training_path}/", \
	                                       "S3DataDistributionType":"FullyReplicated" \
	                                       } \
	                       } \
	      }' \
		--output-data-config \
	      S3OutputPath=s3://${bucket}/${model_path}/ \
	  --resource-config \
	      InstanceType=${training_instance_type},InstanceCount=${training_instance_count},VolumeSizeInGB=${training_instance_size} \
	  --stopping-condition \
	      MaxRuntimeInSeconds=3600 \
	  --hyper-parameters \
				target=Sepal.Length,degree=2 \
		--profile ${profile}

#################
#### Hosting ####
#################

### Inference
JobName = MARS-10474

model:
		$(call blue, "Create sagemaker model...")
		aws sagemaker create-model \
		--model-name ${inference_name} \
		--primary-container \
				Image=${training_image},ModelDataUrl=s3://${bucket}/${model_path}/${JobName}/output/model.tar.gz \
		--execution-role-arn ${training_role_arn} \
		--profile ${profile}

endpoint_config: model
		$(call blue, "Create sagemaker endpoint config...")
		aws sagemaker create-endpoint-config \
		--endpoint-config-name ${inference_name} \
		--production-variants \
				VariantName=dev,ModelName=${inference_name},InitialInstanceCount=${inference_instance_count},InstanceType=${inference_instance_type},InitialVariantWeight=1.0 \
		--profile ${profile}

endpoint: endpoint_config
		$(call blue, "Create sagemaker endpoint...")
		aws sagemaker create-endpoint \
	    --endpoint-name ${inference_name} \
	    --endpoint-config-name ${inference_name} \
			--profile ${profile}

#################
#### CleanUp ####
#################

### CleanUp
delete_endpoint: delete_endpoint_config
	  $(call blue, "Delete sagemaker endpoint...")
		aws sagemaker delete-endpoint \
		--endpoint-name ${inference_name} \
		--profile ${profile}

delete_endpoint_config: delete_model
	  $(call blue, "Delete sagemaker endpoint config...")
		aws sagemaker delete-endpoint-config \
		--endpoint-config-name ${inference_name} \
		--profile ${profile}

delete_model:
		$(call blue, "Delete sagemaker model...")
		aws sagemaker delete-model \
		--model-name ${inference_name} \
		--profile ${profile}

clean: delete_endpoint
		@rm -f app

define blue
	@tput setaf 6
	@echo $1
	@tput sgr0
endef
