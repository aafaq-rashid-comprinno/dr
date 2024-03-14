import boto3
from botocore.exceptions import ClientError

def create_lambda_role(role_name,session):
    try:
        # Create IAM client with the specified AWS profile
        iam_client = session.client('iam')
    
        description = f'{role_name} lambda function role'
        role_name = f'{role_name[:52]}-lambda-role'
     
        # Create IAM role
        response = iam_client.create_role(
            Description=description,
            RoleName=role_name,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': role_name
                },
                {
                   'Key': 'Environment',
                   'Value': 'Dr'
                }

            ],
            AssumeRolePolicyDocument='''{
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }'''
        )


        # Attach AWSLambdaBasicExecutionRole managed policy to enable basic access
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
                

        # Attach AWSLambdaVPCAccessExecutionRole managed policy to enable VPC access
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole'
        )

        # Return the ARN of the created IAM role
        return response['Role']['Arn']

    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return None
