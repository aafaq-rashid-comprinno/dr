import boto3
import json
import string
import random
 
# initializing size of string
N = 30



def list_api_gateways(client):
    paginator = client.get_paginator('get_rest_apis')
    apis = []
    for page in paginator.paginate():
        # Extend the list with the APIs from the current page
        apis.extend(page['items'])
            
    return apis

def get_integrations_for_stages(client, api_id):
    # Get integrations for all stages of an API Gateway
    response = client.get_stages(restApiId=api_id)

    stages = response['item']
    for stage in stages:
        stage_name = stage['stageName']
        print(f"Integrations for Stage: {stage_name}")

        deployment_id = stage['deploymentId']
        resources = client.get_resources(restApiId=api_id)

        for resource in resources['items']:
            path =  resource['path']
            resource_id = resource['id']
            resource_methods = resource.get('resourceMethods', {})

            if resource_methods:
                print(f"Resource ID: {resource_id}, Resource Methods: {', '.join(resource_methods.keys())}")

                for http_method, integration_id in resource_methods.items():
                    integration = client.get_integration(
                        restApiId=api_id,
                        resourceId=resource_id,
                        httpMethod=http_method
                    )
                    

                    # Extract Lambda function ARN based on integration type
                    try: 
                        if 'uri' in integration:
                            integration_uri = integration['uri']
                            lambda_function_name= f"{integration_uri.split(':function:')[1]}".split('/')[0]
                            print(f"  Integration ID: {integration_id}, HTTP Method: {http_method}, Lambda Function ARN: {lambda_function_name}")
                            create_lambda_resource_based_policy(lambda_function=lambda_function_name, api_id=api_id, http_method=http_method, path=path, stage_name=stage_name)
                        elif 'credentials' in integration:
                            lambda_function_name = integration['credentials']
                            print(f"  Integration ID: {integration_id}, HTTP Method: {http_method}, Lambda Function ARN: {lambda_function_name}")
                            create_lambda_resource_based_policy(lambda_function=lambda_function_name, api_id=api_id, http_method=http_method, path=path, stage_name=stage_name)
                        else:
                            print(f"  Integration ID: {integration_id}, HTTP Method: {http_method}, Integration type not supported")

                        # You can do more with the integration information if needed
                    except :
                        print("Error handled")

                
            else:
                print(f"Resource ID: {resource_id} has no resource methods.")
            
            



def create_lambda_resource_based_policy(lambda_function, api_id, http_method, path, stage_name):
    #Create a Lambda resource-based policy for an integration
    session  = boto3.Session(profile_name="destinationfibe")
    sts_client = session.client('sts')
    account_id = sts_client.get_caller_identity()['Account']
    region = sts_client.meta.region_name
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=N))

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "apigateway.amazonaws.com"
                },
                "Action": "lambda:InvokeFunction",
                "Resource": f"arn:aws:lambda:{region}:{account_id}:function:{lambda_function}",
                "Condition": {
                    "ArnLike": {
                        "AWS:SourceArn": f"arn:aws:execute-api:{region}:{account_id}:{api_id}/*/{http_method}{path}"
                    }
                }
            }
        ]
    }
    print(policy_document)

    policy_name = str(res)

    # Attach the policy to the Lambda function
    lambda_client.add_permission(
        FunctionName=f"arn:aws:lambda:{region}:{account_id}:function:{lambda_function}",
        StatementId=policy_name,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
        SourceArn=f"arn:aws:execute-api:{region}:{account_id}:{api_id}/*/{http_method}{path}",
    )

    #print(f"Lambda resource-based policy '{policy_name}' created and attached to the Lambda function.")

# Example usage
if __name__ == "__main__":
    # Task 1: List all API Gateways
    # Initialize AWS clients
    destination_session  = boto3.Session(profile_name="destinationfibe")
    api_gateway_client = destination_session.client('apigateway')
    lambda_client = destination_session.client('lambda')
    
    api_gateways= list_api_gateways(api_gateway_client)
    init_val = 0
    for index, api in enumerate(api_gateways[init_val:]): 
        print("##############################################################################################################")
        print(index+init_val,":", api['id'])
        get_integrations_for_stages(client=api_gateway_client, api_id=api['id'])

    # # Task 3: Create a Lambda resource-based policy
    # lambda_function = "ESAPI"  # Replace with the actual Lambda function ARN
    # stage_name = "PROD"  # Replace with the actual API Gateway stage name