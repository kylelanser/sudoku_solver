# Architecture
Core business logic is contained in short running serverless lambda functions. 
Access to core business logic is through an API hosted on AWS API Gateway.
Authentication to the API is provided by third party IdP's. 
Authorization to the API is provided by AWS Cognito.
The primary user interface is a WebUI hosted on S3 via CloudFront. 
State data storage is DynamoDB
Persistent storage is DynamoDB


