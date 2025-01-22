import boto3

def list_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])
    return instances

