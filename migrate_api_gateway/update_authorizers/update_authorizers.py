import boto3

def list_api_gateways(client):
    # Create a paginator for the get_rest_apis operation
    paginator = client.get_paginator('get_rest_apis')

    # Iterate through pages
    for page in paginator.paginate():
        # Print API Gateway details for each page
        for api in page['items']:
            #print(f"Name: {api['name']}, ID: {api['id']}, Created Date: {api['createdDate']}")
            # Example: Get details for a specific API Gateway by providing its ID
            api_id = api['id']
            list_authorizers(client=client, api_id=api_id)


def list_authorizers(client, api_id):
    # List authorizers for a specific API Gateway
    response = client.get_authorizers(restApiId=api_id)
    # print(response['items'])
    
    # Print authorizer details
    if len(response['items']) > 0:
        for authorizer in response['items']:
            print(f"API ID: {api_id} Authorizer ID: {authorizer['id']}, Name: {authorizer['name']}, Uri: {authorizer['authorizerUri']}")
            updated_uri = authorizer['authorizerUri'].replace("ap-south-1", "ap-south-2").replace("432542842095", "142792260686")
            #print(ur)
            update_authorizer(client=client, rest_api_id=api_id, authorizer_id=authorizer['id'], new_uri=updated_uri)
    else:
        #print("Authorozers not found!")
        pass    

def update_authorizer(client, rest_api_id, authorizer_id, new_uri,):
    try:
        response = client.update_authorizer(
            restApiId=rest_api_id,
            authorizerId=authorizer_id,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/authorizerUri',
                    'value': new_uri
                },
            ]
        )
        print("Authorizer updated successfully")
    except Exception as e:
        print(f"Error updating authorizer: {e}")


if __name__ == "__main__":
    # Source client session
    destination_session = boto3.Session(profile_name="destinationfibe")
    destination_client = destination_session.client('apigateway')

    # List all API Gateways and their authorizers
    list_api_gateways(client=destination_client)
