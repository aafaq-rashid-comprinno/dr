import boto3
from botocore.exceptions import ClientError



def create_security_group(group_name, vpc_id, session):
    try:
        # Create EC2 client with the specified AWS profile
        ec2_client = session.client('ec2')
        description = f'{group_name} security group'
        tags = [
            {
                'Key': 'Name',
                'Value': group_name
            },
            {
                 'Key': 'Environment',
                 'Value': "DR"                            
           }
        ] 
        
        # Create security group
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': tags
                },
            ]
        )
        # Return the ID of the created security group
        return response['GroupId']

    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return None
