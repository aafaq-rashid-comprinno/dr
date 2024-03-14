import boto3
import time

source_profile = "sourcefibe"
destination_profile = "destinationfibe"

source_session = boto3.Session(profile_name=source_profile)
destination_session = boto3.Session(profile_name=destination_profile)

source_batch = source_session.client("batch")

destination_batch = destination_session.client("batch")

# Retrieve job definitions from the source account
response = source_batch.describe_job_definitions()
job_definitions = sorted(response['jobDefinitions'], key=lambda x: x['revision'])
#job_definitions = response['jobDefinitions']
#print(job_definitions)

# Iterate through job definitions and create them in the destination account
for index, job_definition in enumerate(job_definitions):
    if job_definition['status'] == "ACTIVE":
    
        name = job_definition['jobDefinitionName']

        source_revision = job_definition['revision']

        print(f'{index} : {name} : {source_revision}')

        type = job_definition['type']
        #print(f"type: {type}")

        containerProperties = job_definition['containerProperties']
        # print(f"containerProperties: {containerProperties}")

        parameters = job_definition['parameters']
        #print(f"parameters: {parameters}")
        
        tags = job_definition['tags']
        custom_tags = {
            "Name" : name,
            "Environment": "DR",
            "Source_Revision": f"{source_revision}"
        }
        merged_tags = {**tags, **custom_tags}
    
        #print(f"merged_tags: {merged_tags}")

        updated_image = containerProperties['image'].replace("432542842095.dkr.ecr.ap-south-1.amazonaws.com", "142792260686.dkr.ecr.ap-south-2.amazonaws.com")
        containerProperties['image'] = updated_image
        #print(f"containerProperties: {containerProperties}")

        if containerProperties.get('jobRoleArn'):
            jobRoleArn = containerProperties['jobRoleArn'].replace("arn:aws:iam::432542842095:role", "arn:aws:iam::142792260686:role")
            containerProperties['jobRoleArn'] = jobRoleArn
            print(containerProperties)
            print(f"jobRoleArn: {jobRoleArn}")
        else:
            print("jobRoleArn not found!")
        
        if containerProperties.get('executionRoleArn'):
            executionRoleArn = containerProperties['executionRoleArn'].replace("arn:aws:iam::432542842095:role", "arn:aws:iam::142792260686:role")
            containerProperties['executionRoleArn'] = executionRoleArn
            print(f"executionRoleArn: {executionRoleArn}")
        else:
            print("executionRoleArn not found!")
            
        if job_definition.get('retryStrategy'):
            retryStrategy = job_definition['retryStrategy']
            #print(f"retryStrategy: {retryStrategy}")
        else:
            retryStrategy = {'attempts': 1, 'evaluateOnExit': []}

        if job_definition.get('timeout'):
            timeout = job_definition['timeout']
            #print(f"timeout: {timeout}")
        else: 
            timeout = {'attemptDurationSeconds': 60}

        if job_definition.get('platformCapabilities'):
            platformCapabilities = job_definition['platformCapabilities']
            #print(f"platformCapabilities: {platformCapabilities}")
        else:
            platformCapabilities = ['EC2']


        destination_batch.register_job_definition(
            jobDefinitionName=name,
            type=type,
            containerProperties=containerProperties,
            retryStrategy=retryStrategy,
            timeout=timeout,
            platformCapabilities=platformCapabilities,
            tags=merged_tags,
            parameters=parameters
            # Add other parameters as needed
        )
        time.sleep(1)



