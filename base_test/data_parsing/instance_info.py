import re
import json
import os
from io import StringIO

def get_aws_instance_price(instance_type):
    # File is downloaded https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20231222042846/us-east-1/index.json
    pattern = re.compile(rf'(.+) per On Demand Linux {instance_type} Instance Hour')
    with open('../../s3/info-ec2-us-east-1.json', 'r') as file:
        jason = json.load(file)
    on_demand_jason = jason['terms']["OnDemand"]
    for instance in on_demand_jason:
        for instance_sub in on_demand_jason[instance]:
            for a in on_demand_jason[instance][instance_sub]['priceDimensions']:
                if match := pattern.findall(
                        on_demand_jason[instance][instance_sub]['priceDimensions'][a]['description']):
                    return match[0]
    return '-'


def get_aws_instance_value(instance_type, requested_attribut: str, operating_system='Linux'):
    # File is downloaded https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/20231222042846/us-east-1/index.json
    with open('../../s3/info-ec2-us-east-1.json', 'r') as file:
        jason = json.load(file)
    producktes_jason = jason['products']
    for instance in producktes_jason:
        attributes = producktes_jason[instance]['attributes']
        try:
            if 'instanceType' and 'operatingSystem' and requested_attribut in attributes:
                if attributes['instanceType'] == instance_type and \
                        attributes['operatingSystem'] == operating_system:
                    return attributes[requested_attribut]
        except:
            print(attributes)
    return '-'


def lscpu_extract_architecture(text):
    pattern = re.compile(r'Architecture:\s+(\S+)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def lscpu_extract_model_name(text):
    pattern = re.compile(r'Model name:\s+(.+)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def lscpu_extract_thread_per_core(text):
    pattern = re.compile(r'Thread\(s\) per core:\s+(\d+)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def lscpu_extract_cores_per_socket(text):
    pattern = re.compile(r'Core\(s\) per socket:\s+(\d+)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def lscpu_extract_sockets(text):
    pattern = re.compile(r'Socket\(s\):\s+(\d+)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def lscpu_extract_min_speed(text):
    pattern = re.compile(r'CPU min MHz:\s+(\d+)')
    matches = pattern.findall(text)
    return int(matches[0]) / 1000. if matches else "-"


def lscpu_extract_max_speed(text):
    pattern = re.compile(r'CPU max MHz:\s+(\d+)')
    matches = pattern.findall(text)
    return int(matches[0]) / 1000. if matches else "-"


def dmidecode_extract_total_memory_size(text):
    pattern = re.compile(r'Size:\s+(\d+)\s+GB')
    matches = pattern.findall(text)
    total_memory_size = sum(int(match) for match in matches) if matches else 0
    return total_memory_size if total_memory_size else "-"


def dmidecode_extract_memory_stickes(text):
    pattern = re.compile(r'Size:\s+(\d+)\s+GB')
    matches = pattern.findall(text)
    return len(matches) if matches else "-"


def dmidecode_extract_memory_type(text):
    pattern = re.compile(r'Type:\s+(\S+\d)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def dmidecode_extract_memory_speed(text):
    pattern = re.compile(r'Configured Memory Speed:\s+(\S+\s\S+)')
    matches = pattern.findall(text)
    if matches:
        return matches[0]
    pattern = re.compile(r'Speed:\s+(\S+\s\S+)')
    matches = pattern.findall(text)
    return matches[0] if matches else "-"


def lstopo_extract_sum_cache_sizes(text: str, cache_type: str) -> str:
    # Define a regular expression pattern to match cache sizes
    pattern = re.compile(f'{cache_type} L#\\d+ \\(\\d+(\\S\\S)\\)')

    # Use findall to get all matches in the text
    matches = pattern.findall(text)
    if not matches:
        return '-'
    pattern2 = re.compile(f'{cache_type} L#\\d+ \\((\\d+){matches[0]}\\)')
    matches2 = pattern2.findall(text)

    # If there are matches, sum up the sizes and count; otherwise, return 0
    total_cache_size = sum(int(size) for size in matches2) if matches else 0

    return f"{total_cache_size} {matches[0]} in {len(matches)} instances"


def main():
    # Specify the path to the directory
    directory_path = '../../s3/results/1-base-test'

    # Get a list of all items (files and folders) in the directory
    folder_paths = sorted(os.listdir(directory_path))
    result_text_lscpu = '| System | Price | CPU Model Name | Architecture | Cores per socket | Threads per core | Sockets | max frequency (GHz) | min frequency (GHz) | L3 Cash | L2 Cash| L1d | L1i | RAM (GB) | RAM Strikes | RAM Speed | RAM Type | EBS Bandwidth | Networke Bandwith |\n' \
                        + '|-----|-------|--------|------------|------------|-------------|---------|----------|------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|\n'

    for instance_name in folder_paths:
        import pandas as pd
        result_text_lscpu += '| ' + instance_name + ' | ' + get_aws_instance_price(instance_name) + ' | '
        with open(directory_path + '/' + instance_name + '/lscpu.data', 'r') as file:
            text_lscpu = file.read()
        result_text_lscpu += lscpu_extract_model_name(text_lscpu) + ' | ' + lscpu_extract_architecture(
            text_lscpu) + ' | ' + lscpu_extract_cores_per_socket(text_lscpu) + ' | ' + lscpu_extract_thread_per_core(
            text_lscpu) + ' | ' + lscpu_extract_sockets(
            text_lscpu) + ' | ' + f"{lscpu_extract_max_speed(text_lscpu)}" + ' | ' + f"{lscpu_extract_min_speed(text_lscpu)}" + ' | '
        with open(directory_path + '/' + instance_name + '/lstopo.data', 'r') as file:
            text_lstopo = file.read()
        result_text_lscpu += f'{lstopo_extract_sum_cache_sizes(text_lstopo,"L3")} | {lstopo_extract_sum_cache_sizes(text_lstopo, "L2")} | {lstopo_extract_sum_cache_sizes(text_lstopo, "L1d")} | {lstopo_extract_sum_cache_sizes(text_lstopo, "L1i")} | '
        with open(directory_path + '/' + instance_name + '/dmidecode.data', 'r') as file:
            text_dmidecode = file.read()
        result_text_lscpu += f'{dmidecode_extract_total_memory_size(text_dmidecode)} | {dmidecode_extract_memory_stickes(text_dmidecode)} | {dmidecode_extract_memory_speed(text_dmidecode)} | {dmidecode_extract_memory_type(text_dmidecode)} | '
        result_text_lscpu += get_aws_instance_value(instance_name,
                                                    'dedicatedEbsThroughput') + ' | ' + get_aws_instance_value(
            instance_name, 'networkPerformance') + ' |\n'
    with open('instance_info.md', 'w') as file:
        # Write a string to the file
        file.write(result_text_lscpu)

    # Convert Markdown to CSV
    df = pd.read_csv(StringIO(result_text_lscpu), delimiter="|", skipinitialspace=True)

    # Save the DataFrame to a CSV file
    df.to_csv('instance_info.csv', index=False)


if __name__ == '__main__':
    main()
