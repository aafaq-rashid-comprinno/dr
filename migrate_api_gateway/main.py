import boto3
import json

import time


import boto3
import json

def list_api_gateways(source_client):
    paginator = source_client.get_paginator('get_rest_apis')
    apis = []
    for page in paginator.paginate():
        # Extend the list with the APIs from the current page
        apis.extend(page['items'])
            
    return apis



def download_merged_swaggers(source_client, api_id):
    stages = source_client.get_stages(restApiId=api_id)
    swaggers = {}
    
    for stage in stages['item']:
        stage_name = stage['stageName']
        response = source_client.get_export(
            restApiId=api_id,
            stageName=stage_name,
            exportType='swagger',
            parameters={'extensions': 'integrations,authorizers'}
        )
        swaggers[stage_name] = response['body'].read().decode('utf-8')

    return swaggers

def get_lambda_function_names(swagger):
    lambda_function_names = set()

    swagger_json = json.loads(swagger)
    for path, methods in swagger_json.get('paths', {}).items():
        for method, details in methods.items():
            integration = details.get('x-amazon-apigateway-integration', {})
            uri = integration.get('uri', '')

            # Extract Lambda function name from the URI
            parts = uri.split(':function:')
            print(parts)
            if len(parts) > 1:
                lambda_function_arn_parts = parts[-1].split('/')
                lambda_function_name = lambda_function_arn_parts[0]
                lambda_function_names.add(lambda_function_name)

    return lambda_function_names

def update_swagger_for_destination(swagger, source_account_id, source_region, destination_account_id, destination_region):
    swagger_json = json.loads(swagger)
    
    for path, methods in swagger_json.get('paths', {}).items():
        for method, details in methods.items():
            integration = details.get('x-amazon-apigateway-integration', {})
            uri = integration.get('uri', '')
            print("uri: ", uri)

            # Construct the updated URI using string concatenation
            updated_uri = uri.replace(f":{source_region}:", f":{destination_region}:").replace(f":{source_account_id}:", f":{destination_account_id}:")

            print("updated_uri", updated_uri)
            integration['uri'] = updated_uri
            details['x-amazon-apigateway-integration'] = integration

    print(json.dumps(swagger_json, indent=2))
    return json.dumps(swagger_json, indent=2)



def import_merged_swagger(destination_client, api_name, endpoint, swaggers,source_account_id, source_region, destination_account_id, destination_region):
    for stage_name, swagger in swaggers.items():

        # Update Swagger for destination account
        updated_swagger = update_swagger_for_destination(swagger, source_account_id, source_region, destination_account_id, destination_region)
        

        # Import Swagger into destination account
        response = destination_client.import_rest_api(
            failOnWarnings=True,
            parameters={'extensions': 'integrations,authorizers', 'endpointConfigurationTypes': endpoint},
            body=updated_swagger
        )
        api_id = response['id']
        break
    
    for stage_name, swagger in swaggers.items():
        destination_client.create_deployment(
            restApiId=api_id,
            stageName=stage_name
        )
        
        print(f"Swagger imported for {stage_name} in API Gateway {api_name}\n")
def main():
    # source client session
    source_session = boto3.Session(profile_name="sourcefibe")

    # Destination client session
    destination_session = boto3.Session(profile_name="destinationfibe")
    source_client = source_session.client('apigateway')
    destination_client = destination_session.client('apigateway')
    
    # Destination account ID (replace with your destination account ID)
    source_account_id = '432542842095'
    source_region = 'ap-south-1'  # Replace with your destination AWS region

    # Destination account ID (replace with your destination account ID)
    destination_account_id = '142792260686'
    destination_region = 'ap-south-2'  # Replace with your destination AWS region

    # Task 1: List API Gateways in Source Account
    api_gateways = list_api_gateways(source_client)
    # print("API Gateways in Source Account:")
    # for index, api_gateway in enumerate(api_gateways):
    #     print(f"{index + 1}- {api_gateway['name']} (ID: {api_gateway['id']})")

    val = 0
    # Task 2: Download Merged Swaggers
    for index, api_gateway in enumerate(api_gateways[val:]):
        api_name = api_gateway['name']
        api_id = api_gateway['id']
        endpoint = api_gateway['endpointConfiguration']['types'][0]

        print(f"{ index + val} Downloading merged swaggers for API Gateway {api_name} - {api_id} - {endpoint}.")
        swaggers = download_merged_swaggers(source_client, api_id)
        time.sleep(7)

        # Task 3: Import Merged Swagger in Destination Account
        import_merged_swagger(destination_client, api_name, endpoint, swaggers,source_account_id, source_region, destination_account_id, destination_region)

if __name__ == "__main__":
    main()