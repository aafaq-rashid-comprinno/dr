import boto3
import time
from layer_match import layer_match_map

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

def match_layers(destination_lambda_client, layer_name, description):
    response = destination_lambda_client.list_layer_versions(LayerName=layer_name)
    # Extract and print information about each version
    for version in response['LayerVersions']:
        # print(f"Layer Version ARN: {version['LayerVersionArn']}")
        # print(f"Version Number: {version['Version']}")
        # print(f"Description: {version.get('Description', 'No description available')}")
        
        source_description = description
        destination_description = version.get('Description')

        
        if source_description == destination_description:
            # print(F"Source_description: {source_description}")
            # print(f"Destination_description: {destination_description}")
            #print(f"destination_version {version['Version']}")
            return version['LayerVersionArn']
        else:
            pass





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
        
        if function.get('Layers'):
            
           # time.sleep(1)
            function_name = function['FunctionName']
            function_layers = function['Layers']

            #print(function_name)
            #print(function_layers)
            layers_list = []
            for layer in function_layers:
                layer_arn = layer.get('Arn')
                layer_name = layer_arn.split(':')[-2]
                layer_version = int(layer_arn.split(':')[-1])

                # Get information about the Lambda layer version
                response = source_lambda_client.get_layer_version(
                    LayerName=layer_name,
                    VersionNumber=layer_version  # Replace with the version number you want to get information about
                )


                if response.get('Description'):
                    print(layer_name)
                    description = response['Description']
                    #print(f"source_version: {layer_version}")
                    destination_layer_arn = match_layers(destination_lambda_client, layer_name, description)
                    #print(f"destination_layer_arn: {destination_layer_arn}")
                    if destination_layer_arn is not None:
                        layers_list.append(destination_layer_arn)
                    else:
                        pass


                    #print(f"Description: {response['Description']}")
                else:
                    # print(layer_name)
                    # print(layer_version)
                    #print("Description not found!")
                    source_layer_arn = response.get('LayerVersionArn')
                    destination_layer_arn = layer_match_map(source_layer_arn)
                    if destination_layer_arn is not None:
                        layers_list.append(destination_layer_arn)
                        #print(layers_list)
                    else:
                        pass


            if len(layers_list) >= 1: 
                print(function_name)
                print(layers_list)
                try: 
                    destination_lambda_client.update_function_configuration(
                        FunctionName=function_name,
                        Layers=layers_list,
                    )
                except:
                    print("function not found")
                
            else:
                print(function_name)
                print("layers not available")
                        
                    
                
  

if __name__ == "__main__":
    main()