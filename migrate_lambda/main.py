import boto3
from replicate_functions import replicate_lambda_function
from list_lambda_functions import list_functions


def main():

    vpc_id = 'vpc-00b150f131c3a7e7d'

    subnet_ids = ["subnet-03870d7b8932857e4", "subnet-0d5291d2690ad01ef", "subnet-015ac4a176f9bdc3b"]


    # Source Lambda session
    source_session = boto3.Session(profile_name="sourcefibe")
    # source_lambda = source_session.client('lambda')

    # Destination Lambda session
    destination_session = boto3.Session(profile_name="destinationfibe")
    

    
    functions = list_functions(source_session)
    val = 0
    for i, function in enumerate(functions[val:]):
        print(val+i," Replication for function: ", function)
        
        # Replicate Lambda function
        replicate_lambda_function(function_name=function, vpc_id=vpc_id, subnet_ids=subnet_ids, source_session=source_session, destination_session=destination_session)
        
    #     # Replicate Lambda function
    # replicate_lambda_function(function_name=functions[50], vpc_id=vpc_id, subnet_ids=subnet_ids, source_session=source_session, destination_session=destination_session)

if __name__ == '__main__':
    main()