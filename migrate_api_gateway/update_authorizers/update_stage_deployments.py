import boto3
import time

def list_api_gateways(client):
    # Create a paginator for the get_rest_apis operation
    paginator = client.get_paginator('get_rest_apis')

    # Iterate through pages
    for page in paginator.paginate():
        # Print API Gateway details for each page
        for index, api in enumerate(page['items']):
            #print(f"Name: {api['name']}, ID: {api['id']}, Created Date: {api['createdDate']}")
            # Example: Get details for a specific API Gateway by providing its ID
            api_id = api['id']
            print(index,"----------")
            list_authorizers(client=client, api_id=api_id)


def list_authorizers(client, api_id):
    # List authorizers for a specific API Gateway
    response = client.get_authorizers(restApiId=api_id)
    # print(response['items'])
    
    # if authorizer is present
    if len(response['items']) > 0:

        # Get information about stages for the specified API Gateway
        stages_response = client.get_stages(
            restApiId=api_id
        )

        for index, stage in enumerate(stages_response['item']):
            print(api_id)
            print(index,":", stage['stageName'])
            deployment_response = client.create_deployment(
                restApiId=api_id,
                stageName=stage['stageName'],  # Replace with the name of your stage
                description=f"updated on jan 23 2024 after authorizer modification for {stage['stageName']}"   # Optional: Replace with a description for your deployment
            )

            time.sleep(5)
                        
    else:
        print("Authorozers not found!")


if __name__ == "__main__":
    # Destination account acess profile 
    destination_session = boto3.Session(profile_name="destinationfibe")
    destination_client = destination_session.client('apigateway')

    # List all API Gateways and their authorizers
    list_api_gateways(client=destination_client)
