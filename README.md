# Udacity Machine Learning Engineering Nanodegree

##  Crypto investor profiler
#### Capstone project

#### Project overview:
The aim of this project is to combine blockchain data, machine learning and cloud managed services into a final product as a web app. Ethereum blockchain data is publicly available as a GCP public dataset.
The web app predicts the investor profile (cluster) of the Ethereum address that is entered into the user interface. The deployed model is served as an API.

This is based on three features that are extracted from the above-mentioned data source: 
- Current Ethereum balance
- Number of Ethereum token transfers
- Number of unique Ethereum tokens held

The project is formulated as an unsupervised machine learning problem.
In the finance lingo, an investor profile defines an individual's preference in investing decisions. Examples of this are risk-averse/risk-tolerant, diversity of  asset classes and individual assets, investment in growth stocks or value stocks, etc.
In this project, it refers to any kind of investing behavior that can be quantified and used to differentiate between different Ethereum addresses.

It's important to note that a lot of code is built by combining code from different projects throughout the nanodegree program. The aim is to create a minimum viable model.

The prediction script performs on-the-fly calculation of feature values of the provided Ethereum address. It queries the Ethereum data source and returns the normalized feature values. These are then used as input into the trained model which returns the predicted cluster value.


AWS services used in the project:
- S3 to store training data, pre-processing transformer object and GCP credentials
- SageMaker to leverage notebook instances and connect the project end-to-end
- Lambda function to trigger the prediction script
- API Gateway to create an API that is used in the web UI that a user interacts with
- CloudWatch to log and debug possible issues that were encountered in the process of building the solution


GCP services used in the project:
- BigQuery to extract Ethereum's transaction data



Project execution: All the dependendies are either available by default in Sagamaker's Python 3.6 PyTorch kernel or installed in the beginning of the project's notebook.
Meanwhile, the IAM setup is needed to be able to work with different AWS services. Also, if you want to query BigQuery's Ethereum data you need a service account to authenticate the executed queries.


