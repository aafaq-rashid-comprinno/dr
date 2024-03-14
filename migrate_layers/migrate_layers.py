import os
import boto3
import subprocess
from upload import upload

def download_lambda_layers(source_session, destination_session, put_folder):

    # Create a Boto3 Lambda client    
    lambda_client = source_session.client('lambda')

    # Initialize the NextMarker for pagination
    next_marker = None
    all_versions = []
    layer_name = "s8_bs_responsiveness_layer"
    # Use Paginator to handle pagination for layer versions
    paginator = lambda_client.get_paginator('list_layer_versions')
    response_iterator = paginator.paginate(LayerName=layer_name)

    for page in response_iterator:
        versions = page['LayerVersions']

        all_versions.extend(versions)

    print(all_versions)

    # Process and upload layers in order
    for version in reversed(all_versions):

        version_number = version['Version']
        print(version_number)
        download_path = os.path.join(output_folder, f'{layer_name}_v{version_number}.zip')

        print(f'Downloading {layer_name} v{version_number} to {download_path}')

        # Download the Lambda Layer version
        response = lambda_client.get_layer_version_by_arn(
            Arn=version['LayerVersionArn']
        )

        url = response['Content']['Location']
        layer_description = response['Description']
        print(layer_description)
        layer_runtimes = response['CompatibleRuntimes']

        try:
            subprocess.run(["wget", url, "-O", download_path], check=True)

            # Now you can upload these layers to the destination account
            aws_cli_command = ["aws", "s3", "cp", f'{download_path}', "s3://layers-aafaq", "--region", "ap-south-2"]
            subprocess.run(aws_cli_command, check=True)
            print(f'Copied {download_path} to S3')

            key = f'{layer_name}_v{version_number}.zip'
            upload(destination_session, f'{layer_name}', layer_runtimes, layer_description, key)

        except subprocess.CalledProcessError as e:
            print(f"Error running wget: {e}")

if __name__ == "__main__":
    
    # Source Lambda session
    source_session = boto3.Session(profile_name="sourcefibe")
    # source_lambda = source_session.client('lambda')

    # Destination Lambda session
    destination_session = boto3.Session(profile_name="destinationfibe")

    # Specify the output folder where you want to save the Lambda Layers
    output_folder = 'lambda_layers'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Download Lambda Layers
    download_lambda_layers(source_session, destination_session, output_folder)