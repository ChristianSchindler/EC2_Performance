from aws import *


def frequency():
    x86_instances: list[str] = ['c7i.metal-48xl']
    arm_instances: list[str] = []
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/cpu_frequency.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        print(skript)
        create_instance(instance_type=instance, image_id=ImageId_x86,
                             user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/cpu_frequency.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript + aws_shutdown
        create_spot_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)


if __name__ == '__main__':
    frequency()
