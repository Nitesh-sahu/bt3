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
ec2_data_path=config_data['ec2_data_path']
ec2_data=json_operations.loadJsonData(ec2_data_path)

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
    if "ec2_instance_ids" in ec2_data:
        ec2_data["ec2_instance_ids"].append(instance_id)
    else:
        ec2_data["ec2_instance_ids"]=[instance_id]
    if json_operations.saveJsonData(ec2_data_path,ec2_data):
        print("Sucessfulyy Created")     
    

# create_instances()
def get_public_ip(instance_id):
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))
# get_public_ip()
            
            
def get_running_instances():
    
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")


get_running_instances()
print("Boto file change")
print("jenkins version 3 checking")
print("jenkins version 4 checking")
print("jenkin version 5 checking")
print("jenkin version 6 checking")
