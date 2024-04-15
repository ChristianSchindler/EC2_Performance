import boto3
import os

# Create an EC2 client
ec2 = boto3.resource('ec2')
# Image Config Amazon Linux
ImageId_x86 = 'ami-079db87dc4c10ac91'
ImageId_ARM = 'ami-02cd6549baea35b55'

aws_s3_configer = \
    f"""#!/bin/bash
export AWS_ACCESS_KEY_ID={os.getenv('AWS_ACCESS_KEY_ID')}
export AWS_SECRET_ACCESS_KEY={os.getenv('AWS_SECRET_ACCESS_KEY')}
export AWS_DEFAULT_REGION={os.getenv('AWS_DEFAULT_REGION', 'us-east-1')}
aws s3 sync s3://{os.getenv('AWS_BUCKET_NAME')}/skripts ~/skripts
chmod +x -R ~/skripts
"""

aws_shutdown = "\nshutdown -h now"


def create_spot_instance(instance_type: str, image_id: str, user_data: str = '', what_until_start: bool = False):
    """
    create 1 spot instance of instance_type and given distribution.
    Whatis until started and returns instance
    """
    instances = ec2.create_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        InstanceMarketOptions={
            'MarketType': 'spot'
        },
        UserData=user_data,
        KeyName='schindler',
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': f'schindler-{instance_type}'
                    },
                ]
            },
        ]
    )
    print(instances)

    # Extract the instance ID
    for instance in instances:
        instance_id = instance.id
        print(f"{instance_type} EC2 instance {instance_id} created successfully.")
    if what_until_start:
        instance.wait_until_running()
        print(f"EC2 instance {instance_id} started successfully.")
    return instance


def create_instance(instance_type: str, image_id: str, user_data: str = '', what_until_start: bool = False):
    """
    create 1 on demand instance of instance_type and given distribution.
    Whatis until started and returns instance
    """

    instances = ec2.create_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        UserData=user_data,
        KeyName='schindler',
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': f'schindler-{instance_type}'
                    },
                ]
            },
        ]
    )
    print(instances)

    # Extract the instance ID
    for instance in instances:
        instance_id = instance.id
        print(f"{instance_type} EC2 instance {instance_id} created successfully.")
        if what_until_start:
            instance.wait_until_running()
            print(f"EC2 instance {instance_id} started successfully.")
        return instance


def stop_instance(instance) -> None:
    """"Stops a given instance"""
    instance.stop()
    print(f'Stopping EC2 instance: {instance.id}')
    instance.wait_until_stopped()
    print(f'EC2 instance "{instance.id}" has been stopped')


def terminate_instance(instance) -> None:
    """"terminates a given instance"""
    instance.terminate()
    print(f'Terminate EC2 instance: {instance.id}')
    instance.wait_until_terminated()
    print(f'EC2 instance "{instance.id}" has been terminated')


def create_spot_instance_mem(instance_type: str, image_id: str, user_data: str = '', what_until_start: bool = False):
    """
    create 1 spot instance of instance_type and given distribution.
    Whatis until started and returns instance
    """
    instances = ec2.create_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sdh',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 50,
                    'VolumeType': 'standard',
                },
            },
        ],
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        InstanceMarketOptions={
            'MarketType': 'spot'
        },
        UserData=user_data,
        KeyName='schindler',
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': f'schindler-{instance_type}'
                    },
                ]
            },
        ]
    )
    print(instances)

    # Extract the instance ID
    for instance in instances:
        instance_id = instance.id
        print(f"{instance_type} EC2 instance {instance_id} created successfully.")
    if what_until_start:
        instance.wait_until_running()
        print(f"EC2 instance {instance_id} started successfully.")
    return instance


def create_instance_mem(instance_type: str, image_id: str, user_data: str = '', what_until_start: bool = False):
    """
    create 1 on demand instance of instance_type and given distribution.
    Whatis until started and returns instance
    """

    instances = ec2.create_instances(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sdh',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 50,
                    'VolumeType': 'standard',
                },
            },
        ],
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        UserData=user_data,
        KeyName='schindler',
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': f'schindler-{instance_type}'
                    },
                ]
            },
        ]
    )
    print(instances)

    # Extract the instance ID
    for instance in instances:
        instance_id = instance.id
        print(f"{instance_type} EC2 instance {instance_id} created successfully.")
        if what_until_start:
            instance.wait_until_running()
            print(f"EC2 instance {instance_id} started successfully.")
        return instance


if __name__ == '__main__':
    create_spot_instance('c7g.large', image_id=ImageId_ARM, what_until_start=True, user_data=aws_s3_configer)
