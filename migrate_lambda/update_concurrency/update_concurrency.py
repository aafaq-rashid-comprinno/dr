import boto3

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

def get_lambda_concurrency(source_client, function_name):
    """
    Get the concurrency configuration of a Lambda function in the source account.
    """
    response = source_client.get_function_concurrency(FunctionName=function_name)
    return response.get('ReservedConcurrentExecutions')

def update_lambda_concurrency(destination_client, function_name, concurrency):
    """
    Update the concurrency configuration of a Lambda function in the destination account.
    """
    destination_client.put_function_concurrency(FunctionName=function_name, ReservedConcurrentExecutions=concurrency)

def main():
    # AWS credentials and regions for source and destination accounts

    # Source Lambda session
    source_session = boto3.Session(profile_name="sourcefibe")
    source_lambda_client = source_session.client('lambda')

    # Destination Lambda session
    destination_session = boto3.Session(profile_name="destinationfibe")
    destination_lambda_client = destination_session.client('lambda')

    # Get Lambda functions in the source account
    functions = get_lambda_functions(source_lambda_client)
    start = 0
    for index, function in enumerate(functions[0:]):
        function_name = function['FunctionName']

        # Get concurrency details of the Lambda function in the source account
        concurrency = get_lambda_concurrency(source_lambda_client, function_name)

        if concurrency is not None:
            # Update concurrency details in the destination account
            update_lambda_concurrency(destination_lambda_client, function_name, concurrency)
            print(f"{index}: Updated concurrency for {function_name} to {concurrency} in the destination account.")
        else:
            print(f"{index}: Concurrency information not available for {function_name} in the source account.")

if __name__ == "__main__":
    main()