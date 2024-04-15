from aws import *


def test_scaling_benchmark():
    x86_instances: [str] = ['c7a.metal-48xl']
    arm_instances: [str] = []
    for instance in x86_instances:
        aws_skript = f"\n~/skripts/scaling_benchmark.sh c7i.metal-24xl-r2 {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        print(skript)
        create_instance(instance_type=instance, image_id=ImageId_x86, user_data=skript)
    for instance in arm_instances:
        aws_skript = f"\n~/skripts/scaling_benchmark.sh {instance}  {os.getenv('AWS_BUCKET_NAME')}"
        skript = aws_s3_configer + aws_skript
        create_spot_instance(instance_type=instance, image_id=ImageId_ARM, user_data=skript)


if __name__ == '__main__':
    test_scaling_benchmark()

