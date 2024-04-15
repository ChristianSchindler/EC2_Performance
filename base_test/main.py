import os
import time
from aws import *


def test_base_case():
    x86_instances = ['t2.micro']
    arm_instances: [str] = ['t4g.small']
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/base_test.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        create_instance(instance_type=instance, image_id=ImageId_x86,
                        user_data=skript)
        time.sleep(5)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/base_test.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        create_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)
        time.sleep(5)


def a1_base_case():
    x86_instances: [str] = []
    arm_instances: [str] = ['a1.metal']
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/base_test.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        create_instance(instance_type=instance, image_id=ImageId_x86, user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/base_test.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        print(skript)
        create_instance(instance_type=instance, image_id='ami-04c97e62cb19d53f1', user_data=skript)


def base_case():
    # set instance
    x86_instances = []
    arm_instances: [str] = []
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/base_test.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        create_spot_instance(instance_type=instance, image_id=ImageId_x86,
                        user_data=skript)
        time.sleep(5)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/base_test.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        create_spot_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)
        time.sleep(5)


if __name__ == '__main__':
    base_case()
    a1_base_case()
