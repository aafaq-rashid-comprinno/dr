

---

# Disaster Recovery Infrastructure Migration Repository

Welcome to the Disaster Recovery (DR) Infrastructure Migration Repository! This repository houses a collection of scripts and utilities designed to automate the migration of essential infrastructure components from a production (Prod) environment to a disaster recovery (DR) environment within the Amazon Web Services (AWS) ecosystem.

## Purpose

The primary purpose of this repository is to streamline and automate the migration process of critical infrastructure components, such as Lambda functions, API Gateway configurations, AWS Batch jobs, Elastic Container Registry (ECR) configurations, and Lambda layers, from a Prod environment to a DR environment. By providing a set of scripts, this repository aims to minimize manual effort, reduce the risk of errors, and ensure consistency and reliability during the migration process.

## Prerequisites
1. Install AWS CLI 2 on the local or EC2 machine.
2. Ensure proper AWS CLI configurations and permissions for both source and destination profiles.
3. Verify the existence of the S3 bucket (`layers-aafaq`) mentioned in the scripts in the DR account.
4. Update VPC and subnet configurations in the migrate_lambda module as per requirements.

---

## Repository Structure with Detailed info

### 1. [migrate_layers](https://github.com/aafaq-rashid-comprinno/dr/tree/master/migrate_layers)

- **Purpose**: Automates the migration of Lambda layers from a Prod to a DR environment.
- **Usage**: 
  - Configure AWS profiles.
  - Execute the script (`python migrate_layers.py`) for each layer migration specify the layer name in the sctipt.
  - Verify successful migration using the AWS Management Console or CLI.

### 2. [migrate_ecr](https://github.com/aafaq-rashid-comprinno/dr/tree/master/migrate_ecr)

- **Purpose**: Automates the replication of ECR repositories from a source to a destination AWS account.
- **Usage**: 
  - Configure AWS profiles.
  - Execute the script (`python migrate_ecr.py`).
  - Verify successful replication using the AWS Management Console or CLI.

### 3. [migrate_lambda](https://github.com/aafaq-rashid-comprinno/dr/tree/master/migrate_lambda)

- **Purpose**: Automates the migration and management of Lambda functions.
- **Usage**: 
  - Configure AWS profiles.
  - Execute the scripts (`python main.py`, `python update_alias.py`, `python update_concurrency.py`).
  - Verify successful migration/update using the AWS Management Console or CLI.

### 4. [attach_layers_to_lambda](https://github.com/aafaq-rashid-comprinno/dr/tree/master/attach_layers_to_lambda)

- **Purpose**: Automates the attachment of Lambda layers to Lambda functions.
- **Usage**: 
  - Configure AWS profiles.
  - Execute the script (`python attach_layers_to_lambda.py`).
  - Verify successful attachment using the AWS Management Console or CLI.

### 5. [migrate_api_gateway](https://github.com/aafaq-rashid-comprinno/dr/tree/master/migrate_api_gateway)

- **Purpose**: Automates the migration and management of API Gateway configurations.
- **Usage**: 
  - Configure AWS profiles.
  - Execute the scripts (`python main.py`, `python update_authorizers.py`, `python update_stage_deployments.py`).
  - Verify successful migration/update using the AWS Management Console or CLI.

### 6. [migrate_batch](https://github.com/aafaq-rashid-comprinno/dr/tree/master/migrate_batch)

- **Purpose**: Automates the migration of AWS Batch jobs.
- **Usage**: 
  - Configure AWS profiles.
  - Execute the script (`python migrate_batch.py`).
  - Verify successful migration using the AWS Management Console or CLI.

