import boto3


def list_functions(session):
    try:
        # Create Lambda client
        lambda_client = session.client('lambda')

        # Initialize variables
        functions = []
        next_marker = None

        # Paginate through all Lambda functions
        while True:
            if next_marker:
                response = lambda_client.list_functions(Marker=next_marker)
            else:
                response = lambda_client.list_functions()

            # Process functions in the current response
            functions_in_response = response.get('Functions', [])
            
            # Filter functions based on runtime
            functions.extend([function['FunctionName'] for function in functions_in_response if function.get('PackageType') == 'Zip'])

            # Check if there are more functions to retrieve
            next_marker = response.get('NextMarker')
            if not next_marker:
                break

        # Return the list of non-excluded Lambda functions
        return functions

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
