import boto3
import os
from dotenv import load_dotenv
load_dotenv()
import json
import yaml 

# configFilePath = "config/timezon_config.yml"
# with open(configFilePath, "r") as file:
#     setting_dic = yaml.safe_load(file)
# marketplace = os.getenv("market_places").split(',')[0]
# timezone = setting_dic.get(marketplace)

# print(marketplace)
# print(setting_dic.get(marketplace))

scheduler = boto3.client('scheduler',aws_access_key_id="your_access_key_id",
    aws_secret_access_key="your_secret_key",
    region_name='us-west-2')

# response = scheduler.get_schedule(
#     GroupName='ecs-schedulers',
#     Name='PROD-amazon_sellercentral_salesdata'
# )
# print(response)


# input_param = json.dumps({"containerOverrides": [ { "name": "prod-weekly-glance-report", "command" : [ "python3", "main.py" ], "environment" : [ { "name" : "market_places" , "value" : "A13V1IB3VIYZZH,AMEN7PMS3EDWL,A1805IZSGTT6HS,A1PA6795UKMFR9,APJ6JRA9NG5V4,A2NODRKZP88ZB9,A1C3SOZRARQ6R3" } ] } ], 'taskRoleArn': 'arn:aws:iam::566178068807:role/ecsTaskExecutionRole'}) #EU

# input_param = json.dumps({"containerOverrides": [ { "name": "prod-weekly-glance-report", "command" : [ "python3", "main.py" ], "environment" : [ { "name" : "market_places" , "value" : "ATVPDKIKX0DER,A2EUQ1WTGCTBG2,A1AM78C64UM0Y8" } ] } ], 'taskRoleArn': 'arn:aws:iam::566178068807:role/ecsTaskExecutionRole'}) #USA

input_param = json.dumps({"containerOverrides": [ { "name": "amazon_report_processing_SB", "command" : [ "python3", "main.py" ], "environment" : [ { "name" : "market_places" , "value" : "A21TJRUUN4KGV" } ] } ], 'taskRoleArn': 'arn:aws:iam::566178068807:role/ecsTaskExecutionRole'}) #in

# input_param = json.dumps({"containerOverrides": [ { "name": "prod-weekly-glance-report", "command" : [ "python3", "main.py" ], "environment" : [ { "name" : "market_places" , "value" : "A1F83G8C2ARO7P" } ] } ], 'taskRoleArn': 'arn:aws:iam::566178068807:role/ecsTaskExecutionRole'}) #UK

# input_param = json.dumps({"containerOverrides": [ { "name": "prod-weekly-glance-report", "command" : [ "python3", "main.py" ], "environment" : [ { "name" : "market_places" , "value" : "A2VIGQ35RCS4UG,A17E79C6D8DWNP" } ] } ], 'taskRoleArn': 'arn:aws:iam::566178068807:role/ecsTaskExecutionRole'}) #uae

# input_param = json.dumps({"containerOverrides": [ { "name": "prod-daily_pipeline_status", "command" : [ "python3", "main.py" ], "environment" : [ { "name" : "timezone" , "value" : "Europe/Paris" } ] } ], 'taskRoleArn': 'arn:aws:iam::566178068807:role/ecsTaskExecutionRole'}) 

response = scheduler.create_schedule(
    ActionAfterCompletion='NONE',
    # ClientToken='string',
    Description='Scheduler for amazon_report_processing_SB for India region',
    # EndDate=datetime(2015, 1, 1),
    FlexibleTimeWindow={
        # 'MaximumWindowInMinutes': 123,
        'Mode': 'OFF'#|'FLEXIBLE'
    },
    GroupName='IN_Jobs_AmazonMarketPlace',#'USA_Jobs_AmazonMarketPlace',UK_Jobs_AmazonMarketPlace,IN_Jobs_AmazonMarketPlace,EU_Jobs_AmazonMarketPlace,UAE_Jobs_AmazonMarketPlace
    # KmsKeyArn='string',
    Name='dev-amazon_report_processing_SB_IN',
    ScheduleExpression='cron(0 8 * * ? *)',
    ScheduleExpressionTimezone='Asia/Kolkata',#'Asia/Kolkata', America/Los_Angeles, Europe/London, Asia/Dubai, Europe/Paris
    State='ENABLED',#|'DISABLED',
    Target={
        'Arn': 'arn:aws:ecs:us-west-2:566178068807:cluster/uniQin-dev',
        'EcsParameters': {
            'CapacityProviderStrategy': [ 
                {
                    "capacityProvider": "FARGATE_SPOT",
                    "weight": 1,
                    "base": 0
                },
                {
                    "capacityProvider": "FARGATE",
                    "weight": 1,
                    "base": 0
                }
            ],
            'EnableECSManagedTags': True,#|False,
            'EnableExecuteCommand': False, #True|False,
            'NetworkConfiguration': {
                'awsvpcConfiguration': {
                    'AssignPublicIp': 'ENABLED',#|'DISABLED',
                    'SecurityGroups': [
                        "sg-05600cf8e82bbe7c2"
                    ],
                    'Subnets': [
                        "subnet-02676d5969981d9cc","subnet-098dbf5f30eda523d","subnet-05b86ac1c0a9abb69"
                    ]
                }
            },

            'TaskCount': 1,
            'TaskDefinitionArn': "arn:aws:ecs:us-west-2:566178068807:task-definition/amazon_report_processing_SB"
        },

        'Input': input_param,

        'RetryPolicy': {
            'MaximumEventAgeInSeconds': 300,
            'MaximumRetryAttempts': 2
        },
        'RoleArn': 'arn:aws:iam::566178068807:role/service-role/Amazon_EventBridge_Scheduler_ECS_01fe32494c',

    }
)


print(response)




"""
response = scheduler.create_schedule(
    ActionAfterCompletion='NONE',
    # ClientToken='string',
    Description='Scheduler for test, ',
    # EndDate=datetime(2015, 1, 1),
    FlexibleTimeWindow={
        # 'MaximumWindowInMinutes': 123,
        'Mode': 'OFF'#|'FLEXIBLE'
    },
    GroupName='USA_Jobs_AmazonMarketPlace',
    # KmsKeyArn='string',
    Name='DEV-amazon_test',
    ScheduleExpression='cron(0 16 * * ? *)',
    ScheduleExpressionTimezone='Asia/Kolkata',
    State='DISABLED',#|'DISABLED',
    Target={
        'Arn': 'arn:aws:ecs:us-west-2:566178068807:cluster/uniQin-dev',
        'EcsParameters': {
            'CapacityProviderStrategy': [ 
                {
                    "capacityProvider": "FARGATE_SPOT",
                    "weight": 1,
                    "base": 0
                },
                {
                    "capacityProvider": "FARGATE",
                    "weight": 1,
                    "base": 0
                }
            ],
            'EnableECSManagedTags': True,#|False,
            'EnableExecuteCommand': False, #True|False,
            'NetworkConfiguration': {
                'awsvpcConfiguration': {
                    'AssignPublicIp': 'ENABLED',#|'DISABLED',
                    'SecurityGroups': [
                        "sg-05600cf8e82bbe7c2"
                    ],
                    'Subnets': [
                        "subnet-02676d5969981d9cc","subnet-098dbf5f30eda523d","subnet-05b86ac1c0a9abb69"
                    ]
                }
            },

            'TaskCount': 1,
            'TaskDefinitionArn': "arn:aws:ecs:us-west-2:566178068807:task-definition/dev-parameter-testing"
        },

        'Input': input_param,

        'RetryPolicy': {
            'MaximumEventAgeInSeconds': 300,
            'MaximumRetryAttempts': 2
        },
        'RoleArn': 'arn:aws:iam::566178068807:role/service-role/Amazon_EventBridge_Scheduler_ECS_01fe32494c',

    }
)
"""