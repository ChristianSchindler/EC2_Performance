from aws import *


def simd():
    x86_instances: [str] = []
    arm_instances: [str] = ['c7g.metal', 'c7gn.16xlarge']
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/simd.sh {instance} {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        print(skript)
        create_spot_instance_mem(instance_type=instance, image_id=ImageId_x86, user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/simd_arm.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance_mem(instance_type=instance, image_id=ImageId_ARM, user_data=skript)


if __name__ == '__main__':
    simd()

