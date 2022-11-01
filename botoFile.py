from cgitb import handler
import os
import boto3
import json
import json_operations



config_data=json_operations.loadJsonData("./config.json")


key_path=config_data['key_path']
key_name=config_data['key_name']
ami_id=config_data['ami_id']
instance_type = config_data['instance_type']
region_name=config_data['region_name']


# creating client file

ec2_client=boto3.client("ec2", region_name=region_name)

def create_key_pair():
    if not os.path.exists(key_path):
        key_pair=ec2_client.create_key_pair(KeyName=key_name)
        private_key=key_pair['bt3-keyLocalNone']
        with os.fdopen(os.open(key_path,os.O_WRONLY | os.O_CREAT,0o400),"w+")as handle:
            handle.write(private_key)
create_key_pair()



def create_instances():
    instances=ec2_client.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_name
    )
    instance_id=instances['Instances'][0]['InstanceId']
    print(instance_id)
    

create_instances()
