import boto3
from lambda_security_group import create_security_group
from lambda_basic_execution_role import create_lambda_role
from runtimes import get_latest_runtime_version
import time

def replicate_lambda_function(function_name, vpc_id, subnet_ids, source_session, destination_session):
    
    # Source Client to retrive lambda function details in source account
    source_lambda = source_session.client('lambda')

    
    # Get source Lambda function details
    source_function = source_lambda.get_function(
        FunctionName=function_name
    )

    # Create lambda exection role
    role_arn = create_lambda_role(function_name, destination_session)
    print(role_arn)

    time.sleep(5)
   
   # Extract relevant details
    runtime = source_function['Configuration']['Runtime']
    print(runtime)
 
    handler = source_function['Configuration']['Handler']
    print(handler)

    description = source_function['Configuration']['Description']
    print(description)
    
    Timeout=int(source_function['Configuration']['Timeout']),
    print(Timeout)
     
    MemorySize=source_function['Configuration']['MemorySize'],
    print(MemorySize)
    

    # Handle the case where EnvironmentVariables may be missing
    try:
        EnvironmentVariables = {'Variables': source_function['Configuration']['Environment']['Variables']}
    except KeyError:
        EnvironmentVariables = {'Variables': {}}

    print(EnvironmentVariables)
     
    # codeRespository = source_function['Code']['RepositoryType']
    # print(codeRespository)

    # codeLocation = source_function['Code']['Location']
    # print(codeLocation)

    Architectures = source_function['Configuration']['Architectures']
    print(Architectures)
 
    EphemeralStorage = source_function['Configuration'].get('EphemeralStorage', {}).get('Size')
    print(EphemeralStorage)

    # Create security group for lambda function
    security_group_name = f'{function_name}-lambdafunction-security-group'
    security_group_id =  create_security_group(security_group_name, vpc_id, destination_session)
    security_group_ids = [security_group_id]
    print(security_group_ids)

    # security_group_ids = ["sg-0c326651b788f8cf5"]

    # VPC configurations for lambda function
    VpcConfig = {
            'SubnetIds':  subnet_ids,
            'SecurityGroupIds': security_group_ids
     }



    #role_arn = "arn:aws:iam::142792260686:role/CustomerMultipl-lambda-role"
    
    # Get latest runtime
    latest_runtime = get_latest_runtime_version(runtime)
    print(latest_runtime)


    # Destination client to create lambda function in destination account
    destination_lambda = destination_session.client('lambda')

    # Create Lambda function in the destination account
    destination_lambda.create_function(
        FunctionName=function_name,
        Runtime=latest_runtime,
        Role=role_arn,
        Handler=handler,
        Description=description,
        Timeout=Timeout[0],
        MemorySize=MemorySize[0],
        Environment = EnvironmentVariables,
        Architectures = Architectures,
        EphemeralStorage = {
            'Size': EphemeralStorage
        },

        VpcConfig={
            'SubnetIds':  subnet_ids,
            'SecurityGroupIds': security_group_ids
        },
        Code={
            'S3Bucket': 'layers-aafaq',
            'S3Key': 'app.zip'
        },
        Tags = {
        'Name': function_name,
        'Environment': 'DR'
        }
    )

    print(function_name, "migrated")
    print("____________________________________________________________________________")


    