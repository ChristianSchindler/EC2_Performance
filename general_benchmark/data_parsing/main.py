import os
import re
import base_test.data_parsing.instance_info as instance_info
from plot import *


def find_file(folder_path: str) -> str:
    extension = ".html"
    # Get a list of all files in the folder
    all_files = os.listdir(folder_path)

    # Filter files that end with the specified extension
    html_files = [file for file in all_files if file.endswith(extension)]
    return os.path.splitext(html_files[0])[0]


def general_results_single(filter_keys=None, suffix='', extra_with=False):
    categories = ['Single Core Score']
    instances: dict[str, list[str]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
            content = file.read()
            matches = pattern.findall(content)
            print(matches)
            instances[instance_name] = [matches[0]]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='System_Index',
         title='UnixBench Single Core', filename='general_results_single', extra_with=extra_with)


def general_results_multi(filter_keys=None, suffix='', extra_with=False):
    categories = ['Multi Core Score']
    instances: dict[str, list[str]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
            content = file.read()
            matches = pattern.findall(content)
            print(matches)
            instances[instance_name] = [matches[1]]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='System_Index',
         title='UnixBench Multi Core', filename='general_results_multi', extra_with=extra_with)


def general_results_multi_scaling(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    categories = ['Multi Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
            content = file.read()
            matches = pattern.findall(content)
            print(matches)
            instances[instance_name] = [float(matches[1]) / float(matches[0]) / int(
                instance_info.get_aws_instance_value(instance_name, 'vcpu')) * 100.]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='System_Index scaling in %',
         title='UnixBench Scaling: \n Multi Core / (Single Core* vCPU)', filename='general_results_multi_scaling',
         extra_with=extra_with)


def DH_multi_scaling(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    categories = ['Multi Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            dh = get_DH(content)
            instances[instance_name] = [float(dh[1][2]) / float(dh[0][2]) / int(
                instance_info.get_aws_instance_value(instance_name, 'vcpu')) * 100.]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index scaling in %',
         title='UnixBench Dhrystone Scaling: \n Multi Core / (Single Core* vCPU)', filename='dh_multi_scaling',
         extra_with=extra_with)


def WH_multi_scaling(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    categories = ['Multi Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            dh = get_WH(content)
            instances[instance_name] = [float(dh[1][2]) / float(dh[0][2]) / int(
                instance_info.get_aws_instance_value(instance_name, 'vcpu')) * 100.]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index scaling in %',
         title='UnixBench Whetstone Scaling: \n Multi Core / (Single Core* vCPU)', filename='wh_multi_scaling',
         extra_with=extra_with)

def get_DH(content: str) -> list[list[int]]:
    return re.compile(rf'Dhrystone 2 using register variables\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_WH(content: str) -> list[list[int]]:
    return re.compile(rf'Double-Precision Whetstone\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_ET(content: str) -> list[list[int]]:
    return re.compile(rf'Double-Precision Whetstone\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_FC1(content: str) -> list[list[int]]:
    return re.compile(rf'File Copy 1024 bufsize 2000 maxblocks\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_FC2(content: str) -> list[list[int]]:
    return re.compile(rf'File Copy 256 bufsize 500 maxblocks\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_FC3(content: str) -> list[list[int]]:
    return re.compile(rf'File Copy 4096 bufsize 8000 maxblocks\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_PT(content: str) -> list[list[int]]:
    return re.compile(rf'Pipe Throughput\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_CS(content: str) -> list[list[int]]:
    return re.compile(rf'Pipe-based Context Switching\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_PC(content: str) -> list[list[int]]:
    return re.compile(rf'Process Creation\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_SS1(content: str) -> list[list[int]]:
    return re.compile(rf'Shell Scripts \(1 concurrent\)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_SS8(content: str) -> list[list[int]]:
    return re.compile(rf'Shell Scripts \(8 concurrent\)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def get_SC(content: str) -> list[list[int]]:
    return re.compile(rf'System Call Overhead\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def alle_categories_single(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    categories = ['DH', 'WH', 'ET', 'FC1', 'FC2', 'FC3', 'PT', 'CS', 'PC', 'SS1', 'SS8', 'SC']
    instances: dict[str, list[str]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            instances[instance_name] = [get_DH(content)[0][2], get_WH(content)[0][2], get_ET(content)[0][2],
                                        get_FC1(content)[0][2], get_FC2(content)[0][2], get_FC3(content)[0][2],
                                        get_PT(content)[0][2], get_CS(content)[0][2], get_PC(content)[0][2],
                                        get_SS1(content)[0][2], get_SS8(content)[0][2], get_SC(content)[0][2]]
    print(instances)
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index',
         title='UnixBench Individual Tests Single Core', filename='alle_categories_single', extra_with=extra_with)

    # normalize it
    instances = normalize(instances)
    plot(categories, instances, suffix=suffix, ylabel='Index',
         title='UnixBench Individual Tests Single Core Normalised', filename='alle_categories_single_norm',
         extra_with=extra_with)


def alle_categories_multi(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    if filter_keys is None:
        filter_keys = []
    categories = ['DH', 'WH', 'ET', 'FC1', 'FC2', 'FC3', 'PT', 'CS', 'PC', 'SS1', 'SS8', 'SC']
    instances: dict[str, list[str]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            instances[instance_name] = [get_DH(content)[1][2], get_WH(content)[1][2], get_ET(content)[1][2],
                                        get_FC1(content)[1][2], get_FC2(content)[1][2], get_FC3(content)[1][2],
                                        get_PT(content)[1][2], get_CS(content)[1][2], get_PC(content)[1][2],
                                        get_SS1(content)[1][2], get_SS8(content)[1][2], get_SC(content)[1][2]]
    print(instances)
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index',
         title='UnixBench Individual Tests Multi Core', filename='alle_categories_multi', extra_with=extra_with)

    # normalize it
    instances = normalize(instances)
    plot(categories, instances, suffix=suffix, ylabel='Index',
         title='UnixBench Individual Tests Multi Core Normalised', filename='alle_categories_multi_norm',
         extra_with=extra_with)


def alle_categories_multi_scaling(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    categories = ['DH', 'WH', 'ET', 'FC1', 'FC2', 'FC3', 'PT', 'CS', 'PC', 'SS1', 'SS8', 'SC']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            a = [get_DH(content)[0][2], get_WH(content)[0][2], get_ET(content)[0][2],
                 get_FC1(content)[0][2], get_FC2(content)[0][2], get_FC3(content)[0][2],
                 get_PT(content)[0][2], get_CS(content)[0][2], get_PC(content)[0][2],
                 get_SS1(content)[0][2], get_SS8(content)[0][2], get_SC(content)[0][2]]
            b = [get_DH(content)[1][2], get_WH(content)[1][2], get_ET(content)[1][2],
                 get_FC1(content)[1][2], get_FC2(content)[1][2], get_FC3(content)[1][2],
                 get_PT(content)[1][2], get_CS(content)[1][2], get_PC(content)[1][2],
                 get_SS1(content)[1][2], get_SS8(content)[1][2], get_SC(content)[1][2]]
            instances[instance_name] = div_array(b, a, float(
                instance_info.get_aws_instance_value(instance_name, 'vcpu')) / 100.)
        print(instances)
    instances = filter_dictionary(instances, filter_keys)

    plot(categories, instances, suffix=suffix, ylabel='Index scaling in %',
         title='UnixBench Individual Tests\nMulti Core / (Single Core* vCPU)', filename='alle_categories_multi_scaling',
         extra_with=extra_with)

    # normalize it
    instances = normalize(instances)
    plot(categories, instances, suffix=suffix, ylabel='Index scaling in %',
         title='UnixBench Individual Tests\nMulti Core / (Single Core* vCPU) norm',
         filename='alle_categories_multi_scaling_norm', extra_with=extra_with)


def perf_data(text: str, value: str) -> int | str:
    instructions_match = re.search(rf"(\d+)----{value}--", text)
    if instructions_match:
        instructions_value = int(instructions_match.group(1))
        print(f"Value of instructions: {instructions_value}")
        return instructions_value
    else:
        print("Instructions not found in the data.")
        return 0


def perf_parsing(filter_keys=None, suffix='', extra_with=False):
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'
    categories = ['Cash misses']
    instances: dict[str, list[float]] = {}
    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/perf.csv', 'r') as file:
            content = file.read()
            a = perf_data(content, 'instructions')
            instances[instance_name] = [a]
    print(instances)
    plot(categories, instances, suffix=suffix, xlabel='', ylabel='Cash misses',
         title='Total Cash misses', filename='branch-misses', extra_with=extra_with)


def multi_score_per_dollar(filter_keys=None, suffix='', extra_with=False):
    categories = ['Multi Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
            content = file.read()
            matches = pattern.findall(content)
            print(matches)
            instances[instance_name] = [
                float(matches[1]) / float(instance_info.get_aws_instance_price(instance_name)[1:])]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index per US$',
         title='UnixBench Multi Core per US$', filename='multi_score_per_dollar', extra_with=extra_with)

    # normalize it
    instances = normalize(instances)
    print(instances)
    plot(categories, instances, suffix=suffix, ylabel='Index per US$',
         title='UnixBench Multi Core per US$ Normalised', filename='multi_score_per_dollar_norm', extra_with=extra_with)


def multi_dray_per_dollar(filter_keys=None, suffix='', extra_with=False):
    categories = ['Multi Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        print(path)
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            instances[instance_name] = [
                float(get_DH(content)[1][2]) / float(instance_info.get_aws_instance_price(instance_name)[1:])]
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index per US$',
         title='UnixBench Dhrystone Multi Core per US$', filename='multi_score_dhry_per_dollar', extra_with=extra_with)

    # normalize it
    instances = normalize(instances)
    print(instances)
    plot(categories, instances, suffix=suffix, ylabel='Index per US$',
         title='UnixBench Dhrystone Multi Core per US$ Normalised', filename='multi_score_dhry_per_dollar_norm',
         extra_with=extra_with)


def alle_categories_multi_per_dollar(filter_keys=None, suffix='', extra_with=False):
    # Sample data
    categories = ['DH', 'WH', 'ET', 'FC1', 'FC2', 'FC3', 'PT', 'CS', 'PC', 'SS1', 'SS8', 'SC']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            # print(instance_name)
            instances[instance_name] = convert_strings_to_floats(
                [get_DH(content)[1][2], get_WH(content)[1][2], get_ET(content)[1][2],
                 get_FC1(content)[1][2], get_FC2(content)[1][2], get_FC3(content)[1][2],
                 get_PT(content)[1][2], get_CS(content)[1][2], get_PC(content)[1][2],
                 get_SS1(content)[1][2], get_SS8(content)[1][2], get_SC(content)[1][2]])
            # print(f'normal: {instances[instance_name]}')
            price = float(instance_info.get_aws_instance_price(instance_name)[1:])
            # print(f'price: {price}')
            instances[instance_name] = [x / price for x in instances[instance_name]]
            # print(float(instance_info.get_aws_instance_price(instance_name)[1:]))
            # print(f'per: {instances[instance_name]}')
    # print(instances)
    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index per US$',
         title='UnixBench Individual Tests Multi Core per US$', filename='alle_categories_multi_per_dollar',
         extra_with=extra_with)

    # normalize it
    max_list = [max(convert_strings_to_floats(values)) for values in zip(*instances.values())]  # print(result_list)
    for instance_name in instances.keys():
        instances[instance_name] = div_array(instances[instance_name], max_list)
    # print(instances)
    plot(categories, instances, suffix=suffix, ylabel='Index per US$',
         title='UnixBench Individual Tests Multi Core per US$ Normalised',
         filename='alle_categories_multi_per_dollar_norm', extra_with=extra_with)


def cs_categories_single(filter_keys=None, suffix=''):
    # Sample data
    categories = ['Single Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            instances[instance_name] = [get_CS(content)[0][2]]

    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index',
         title='UnixBench Context Switching Performance', filename='cs_categories_single', extra_with=True)


def cs_categories_multi(filter_keys=None, suffix=''):
    # Sample data
    categories = ['Multi Core Score']
    instances: dict[str, list[float]] = {}
    # Specify the path to the directory
    directory_path = '../../s3/results/2-general_benchmark'

    # Get a list of all items (files and folders) in the directory
    folder_paths = os.listdir(directory_path)
    for instance_name in folder_paths:
        if filter_keys and instance_name not in filter_keys:
            continue
        path = directory_path + '/' + instance_name
        with open(path + '/' + find_file(path), 'r') as file:
            content = file.read()
            instances[instance_name] = [get_CS(content)[1][2]]

    instances = filter_dictionary(instances, filter_keys)
    plot(categories, instances, suffix=suffix, ylabel='Index',
         title='UnixBench Context Switching Performance', filename='cs_categories_multi')


def execute_all(instances: list[str] = None, suffix: str = '', extra_with=False):
    DH_multi_scaling(instances, suffix, extra_with=extra_with)
    WH_multi_scaling(instances, suffix, extra_with=extra_with)
    multi_dray_per_dollar(instances, suffix, extra_with=extra_with)
    multi_score_per_dollar(instances, suffix, extra_with=extra_with)
    alle_categories_multi_per_dollar(instances, suffix, extra_with=extra_with)

    general_results_single(instances, suffix, extra_with=extra_with)
    general_results_multi(instances, suffix, extra_with=extra_with)
    general_results_multi_scaling(instances, suffix, extra_with=extra_with)

    alle_categories_multi(instances, suffix, extra_with=extra_with)
    alle_categories_single(instances, suffix, extra_with=extra_with)
    alle_categories_multi_scaling(instances, suffix, extra_with=extra_with)


def all_intel():
    instances = ['c3.8xlarge', 'c4.8xlarge', 'c5.metal', 'c6i.metal', 'c7i.metal-48xl']
    suffix = '_intel'
    execute_all(instances, suffix)


def all_amd():
    instances = ['m5a.24xlarge', 'c5a.24xlarge', 'c6a.metal', 'c7a.metal-48xl']
    suffix = '_amd'
    execute_all(instances, suffix)


def all_graviton():
    instances = ['a1.metal', 'c6g.metal', 'c7g.metal', 'c7gn.16xlarge']
    suffix = '_graviton'
    execute_all(instances, suffix)


def all_overview():
    instances = ['a1.metal', 'c3.8xlarge', 'c4.8xlarge', 'c5.metal', 'm5a.24xlarge', 'c5a.24xlarge', 'c6a.metal',
                 'c6g.metal', 'c6i.metal', 'c7a.metal-48xl', 'c7g.metal', 'c7gn.16xlarge', 'c7i.metal-48xl']
    suffix = '_overview'
    execute_all(instances, suffix, True)


def all_apendix():
    instances = ['a1.metal', 'c3.8xlarge', 'c4.8xlarge', 'c5.metal', 'm5a.24xlarge', 'c5a.24xlarge', 'c6a.metal',
                 'c6g.metal', 'c6i.metal', 'c7a.metal-48xl', 'c7g.metal', 'c7gn.16xlarge', 'c7i.metal-48xl',
                 'd2.8xlarge', 'i3.metal', 'm5.metal']
    suffix = '_apendix'
    execute_all(instances, suffix, True)


def all_c7g():
    instances = ['c7g.16xlarge', 'c7g.metal', 'c7gn.metal', 'c7gn.16xlarge']
    suffix = '_c7g'
    execute_all(instances, suffix)


def all_c5a():
    instances = ['m5a.24xlarge', 'c5a.24xlarge', 'c6a.metal', 'c6a.48xlarge']
    suffix = '_c5a'
    execute_all(instances, suffix)


def cs():
    instances = ['c3.8xlarge', 'c4.8xlarge', 'c5.metal', 'a1.metal', 'c6g.metal', 'c5a.24xlarge', 'c6a.metal',
                 'c6a.48xlarge', 'c7a.48xlarge','c7i.48xlarge',
                 'c7g.metal', 'c7g.16xlarge', 'c7g.metal', 'c7gn.16xlarge', 'c6i.metal', 'c7i.metal-48xl',
                 'c7a.metal-48xl', 'm5a.24xlarge', 'c5.24xlarge','c6i.32xlarge', 'c6g.16xlarge', 'a1.4xlarge']
    cs_categories_single(instances)
    #cs_categories_multi(instances)


if __name__ == '__main__':
    #execute_all()
    #all_intel()
    #all_amd()
    #all_graviton()
    #all_overview()
    #all_apendix()
    #all_c7g()
    #all_c5a()
    cs()
