from aws import *


def test_general_benchmark():
    x86_instances: [str] = ['t2.micro']
    arm_instances: [str] = []
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/general_benchmark.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_instance(instance_type=instance, image_id=ImageId_x86,
                        user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/general_benchmark.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)


def general_benchmark():
    x86_instances: [str] = []
    arm_instances: [str] = ['c7gd.metal']
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/general_benchmark.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_x86,
                        user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/general_benchmark.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)


def general_benchmark_aws_linux_2():
    instance: str = 'a1.metal'
    aws_skript = f"\n~/skripts/general_benchmark_a1.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
    skript = aws_s3_configer + aws_skript
    create_spot_instance(instance_type=instance, image_id='ami-048d7f5ca8e2edd06', user_data=skript)


def general_benchmark_con():
    x86_instances: [str] = ['c7i.metal-48xl', 'c7a.metal-48xl']
    arm_instances: [str] = ['c7g.metal']
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/general_benchmark_con.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_x86,
                        user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/general_benchmark_con.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)


def cs_singel():
    x86_instances: [str] = ['c5.24xlarge','c6i.32xlarge']
    arm_instances = ['c6g.16xlarge']
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/general_benchmark_cs.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_x86,
                        user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/general_benchmark_cs.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_ARM,
                        user_data=skript)
    instance = 'a1.4xlarge'
    aws_skript = f"\n~/skripts/general_benchmark_cs_a1.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
    skript = aws_s3_configer + aws_skript
    create_spot_instance(instance_type=instance, image_id='ami-048d7f5ca8e2edd06',
                         user_data=skript)


if __name__ == '__main__':
    cs_singel()
