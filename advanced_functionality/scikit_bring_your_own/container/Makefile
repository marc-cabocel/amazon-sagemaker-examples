all: run

# This makefile contains some convenience commands for deploying and publishing.

# For example, to build and run the docker container locally, just run:
# $ make

# or to publish the :latest version to the specified registry as :1.0.0, run:
# $ make publish version=1.0.0



profile = Test
region = eu-west-1
account_number = $(shell aws sts get-caller-identity --profile ${profile} | jq '.Account')

bucket = marc-stationf-sagemaker
image = decision_trees_inference
tag = latest
model_name = marc-test
random = $(shell echo $$RANDOM)
dockerfile = Dockerfile.inference

### Training Parameters
training_job_name = TrainingDecisionTree-${random}
training_image = ${account_number}.dkr.ecr.${region}.amazonaws.com/${image}:${tag}
training_input_mode = File
training_role_arn = arn:aws:iam::${account_number}:role/service-role/AmazonSageMaker-ExecutionRole-20180301T173668
training_instance_type = ml.m4.xlarge
training_instance_count = 1
training_instance_size = 1

### Inference parameters
inference_name = InferenceDecisionTree
inference_instance_type = ml.m4.xlarge
inference_instance_count = 1


test:
		echo ${random}

build:
	  $(call blue, "building and pushing image...")
		./build_and_push.sh ${image} ${profile} ${tag} ${dockerfile}

### Training
local_training:
	$(call blue, "Locally testing container ...")
	cd ./local_test; ./train_local.sh ${image}

training: local_training
		$(call blue, "Create bucket ...")
		aws s3api put-object --bucket ${bucket} --key data/training/ --profile ${profile}
		$(call blue, "Create training job...")
		aws sagemaker create-training-job \
	  --training-job-name ${training_job_name} \
	  --algorithm-specification \
	      TrainingImage=${training_image},TrainingInputMode=${training_input_mode} \
	  --role-arn ${training_role_arn} \
	  --input-data-config \
			'{"ChannelName":"training", \
	         "DataSource":{"S3DataSource":{"S3DataType":"S3Prefix", \
	                                       "S3Uri":"s3://${bucket}/data/training/", \
	                                       "S3DataDistributionType":"FullyReplicated" \
	                                       } \
	                       } \
	         }' \
		--output-data-config \
	      S3OutputPath=s3://${bucket}/models/ \
	  --resource-config \
	      InstanceType=${training_instance_type},InstanceCount=${training_instance_count},VolumeSizeInGB=${training_instance_size} \
	  --stopping-condition \
	      MaxRuntimeInSeconds=86400 \
	  --hyper-parameters \
	      max_leaf_nodes=5 \
		--profile ${profile}

### Inference

model:
		$(call blue, "Create sagemaker model...")
		aws sagemaker create-model \
		--model-name ${inference_name} \
		--primary-container \
				Image=${training_image},ModelDataUrl=s3://${bucket}/models/TrainingDecisionTree-5620/output/model.tar.gz \
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

clean:
	@rm -f app

define blue
	@tput setaf 6
	@echo $1
	@tput sgr0
endef
