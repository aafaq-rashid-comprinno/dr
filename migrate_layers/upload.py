import os
import boto3
import subprocess

def upload(destination_session, layer_name, layer_runtimes, layer_description,layer_key):

    # Create a Boto3 Lambda client for the target account    
    target_lambda_client = destination_session.client('lambda')

    # Create the same Lambda Layer in the target account
    target_lambda_client.publish_layer_version(
        LayerName=layer_name,
        Content={
            'S3Bucket': 'layers-aafaq',  # Replace with your S3 bucket
            'S3Key': f'{layer_key}',  # Adjust S3 key as needed
        },
        CompatibleRuntimes=layer_runtimes,
        Description=layer_description,
    )

    print(f'Created {layer_name} in target account')


