FROM ubuntu:16.04

MAINTAINER Amazon SageMaker Examples <amazon-sagemaker-examples@amazon.com>

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    wget \
    r-base \
    r-base-dev \
    ca-certificates

RUN R -e "install.packages(c('mda', 'plumber'), repos='https://cloud.r-project.org')"

ENV PATH="/opt/program:${PATH}"

#COPY mars.R /opt/ml/mars.R
#COPY plumber.R /opt/ml/plumber.R

# Set up the program in the image
COPY mars.R /opt/program/
COPY plumber.R /opt/program/

WORKDIR /opt/program

ENTRYPOINT ["/usr/bin/Rscript", "/opt/program/mars.R", "--no-save"]
