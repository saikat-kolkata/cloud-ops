import boto3

def deploy_ecs_container():
    # Define ECS task parameters including container definition with environment variables
    ecs_task_params = {
        'taskDefinition': 'task-definition',
        'cluster': 'ecs-cluster-name',
        'overrides': {
            'containerOverrides': [
                {
                    'name': 'container-name',
                    'environment': [
                        {
                            'name': 'ENV_VAR1',
                            'value': 'value1'
                        },
                        {
                            'name': 'ENV_VAR2',
                            'value': 'value2'
                        }
                        
                    ]
                }
            ]
        }
    }
    
    # Create or update ECS task
    ecs_client = boto3.client('ecs')
    response = ecs_client.run_task(**ecs_task_params)
    print(response)
    
def lambda_handler(event, context):
    deploy_ecs_container()

    return {
        'statusCode': 200,
        'body': 'ECS container deployment initiated'
    }
