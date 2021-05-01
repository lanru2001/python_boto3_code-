#Python code to create an ec2 instance 
import boto3
ec2=boto3.resource('ec2')
#create a new EC2 instance
instances=ec2.create_instances(
       ImageId='ami-083ebc5a49573896a',
       MinCount=1,
       MaxCount=2,
       InstanceType='t2.micro',
       KeyName='key06042020',
)

#Python code with boto3 to create security group,ingress and vpc in AWS 
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('vpc-00ec7198236e70521', '')

try:
    response = ec2.create_security_group(GroupName='webappsecuritygroup',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)
