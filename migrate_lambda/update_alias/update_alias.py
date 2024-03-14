import boto3
from botocore.exceptions import ClientError

def get_lambda_functions(source_client):
    """
    Get a list of zip-based Lambda functions in the source account.
    """
    functions = []
    marker = None

    while True:
        if marker:
            response = source_client.list_functions(Marker=marker)
        else:
            response = source_client.list_functions()

        functions.extend(response['Functions'])
        marker = response.get('NextMarker')

        if not marker:
            break

    # Filter functions based on PackageType
    zip_based_functions = [func for func in functions if func.get('PackageType') == 'Zip']

    return zip_based_functions

def get_latest_lambda_version(destination_client, function_name):
    """
    Get the latest version of a Lambda function in the destination account.
    """
    response = destination_client.list_versions_by_function(FunctionName=function_name)
    versions = response['Versions']
    
    # Sorting the versions in descending order
    sorted_versions = sorted(versions, key=lambda x: x['Version'], reverse=True)
    
    if sorted_versions:
        return sorted_versions[0]['Version']
    else:
        return None

def get_lambda_aliases(source_client, function_name):
    """
    Get the aliases of a Lambda function in the source account.
    """
    response = source_client.list_aliases(FunctionName=function_name)
    return response.get('Aliases', [])

def update_lambda_aliases(destination_client, function_name, aliases, latest_version):
    """
    Update the aliases of a Lambda function in the destination account.
    """
    for alias in aliases:
        try:
            destination_client.create_alias(
                FunctionName=function_name,
                Name=alias['Name'],
                FunctionVersion=latest_version,
                Description=alias.get('Description', '')
            )
            print(f"Updated alias {alias['Name']} for {function_name} in the destination account.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceConflictException':
                print(f"Alias {alias['Name']} already exists for {function_name} in the destination account. Skipping.")
            else:
                # Handle other exceptions
                print(f"Error updating alias {alias['Name']} for {function_name}: {e}")

def main():
    # AWS credentials and regions for source and destination accounts

    # Source Lambda session
    source_session = boto3.Session(profile_name="sourcefibe")
    source_lambda_client = source_session.client('lambda')

    # Destination Lambda session
    destination_session = boto3.Session(profile_name="destinationfibe")
    destination_lambda_client = destination_session.client('lambda')

    # Get zip-based Lambda functions in the source account
    zip_based_functions = get_lambda_functions(source_lambda_client)

    for function in zip_based_functions:
        function_name = function['FunctionName']

        # Get aliases of the Lambda function in the source account
        aliases = get_lambda_aliases(source_lambda_client, function_name)

        if aliases:
            # Get the latest version of the Lambda function in the destination account
            latest_version = get_latest_lambda_version(destination_lambda_client, function_name)

            # Update aliases in the destination account
            update_lambda_aliases(destination_lambda_client, function_name, aliases, latest_version)
        else:
            print(f"No aliases found for {function_name} in the source account.")

if __name__ == "__main__":
    main()