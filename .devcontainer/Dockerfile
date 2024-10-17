FROM python:3.9-slim

RUN apt-get update

RUN apt-get install -y nano htop curl git unzip wget

RUN pip install pandas==1.3.1

RUN pip install boto3

RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

RUN npm install -g aws-cdk

# RUN cd infra/vpc

# RUN pip install -r requirements.txt

RUN wget https://releases.hashicorp.com/terraform/1.9.5/terraform_1.9.5_linux_amd64.zip \
    && unzip terraform_1.9.5_linux_amd64.zip \ 
    && mv terraform /usr/local/bin \
    && rm terraform_1.9.5_linux_amd64.zip

WORKDIR /WORKDIR

CMD ["bash"]
