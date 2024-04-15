import re
import os
from plot import *
from general_benchmark.data_parsing.main import find_file, get_WH

import base_test.data_parsing.instance_info as instance_info


def highway_meam(content: str):
    pattern = re.compile(r'BM_Mandelbrot_Highway/repeats:100_mean\s+(\d+)\s+')
    return pattern.findall(content)


def scalar_meam(content: str):
    pattern = re.compile(r'BM_Mandelbrot_Scalar/repeats:100_mean\s+(\d+)\s+')
    print(content)
    print(pattern.findall(content))
    return pattern.findall(content)


def multi(name):
    directory_path = '../../s3/results/2-general_benchmark'
    path = directory_path + '/' + name + '/'
    # Get a list of all items (files and folders) in the directory
    with open(path + find_file(path), 'r') as file:
        pattern = re.compile(rf'System Benchmarks Index Score\s+([\d.]+)')
        content = file.read()
        matches = pattern.findall(content)
        return matches[1]


def main(dir = './'):

    # Get a list of all items (files and folders) in the directory
    for instance_name in folder_paths:
        path = '../../s3/results/2-general_benchmark/' + instance_name
        with open(path + '/' + find_file(path), 'r') as file:
            m[instance_name] = [float(get_WH(file.read())[0][2])]

    normalize(m)

    print(m)

    categories = ['scalar']
    instances_s = {}
    for instance_name in folder_paths:
        with open(directory_path + '/' + instance_name + '/scalar_100.log', 'r') as file:
            scalar = file.read()
            scalar = pow(10, 9) / int(scalar_meam(scalar)[0])
        instances_s[instance_name] = [scalar]
    plot(categories, instances_s, filename='scalar', ylabel='executions per second', title='Mandelbrot Scalar Implementation', )

    categories = ['highway']
    instances_h = {}
    for instance_name in folder_paths:
        with open(directory_path + '/' + instance_name + '/highway_100.log', 'r') as file:
            highway = file.read()
            highway = pow(10, 9) / int(highway_meam(highway)[0])
        instances_h[instance_name] = [highway]
    plot(categories, instances_h, filename='highway', ylabel='executions per second', title='Mandelbrot Highway Implementation')

    categories = ['']
    instances_d = {}
    for instance_name in folder_paths:
        instances_d[instance_name] = [instances_h[instance_name][0] / instances_s[instance_name][0]]
    print('dif')
    print(instances_d)
    plot(categories, instances_d, filename='dif', ylabel='relative performance', title='Mandelbrot Highway / Scalar Implementation')

    instances_p = {}
    for instance_name in folder_paths:
        a = float(instance_info.get_aws_instance_price(instance_name)[1:])
        print(a)
        instances_p[instance_name] = [instances_h[instance_name][0] / a]
    normalize(instances_p)
    print(instances_h)
    print(instances_p)
    plot(categories, instances_p, filename='h_dollar', ylabel='relative performance', title='Mandelbrot Highway / Instance Price Normelised')


    instances_ps = {}
    for instance_name in folder_paths:
        a = float(instance_info.get_aws_instance_price(instance_name)[1:])
        print(a)
        instances_ps[instance_name] = [instances_s[instance_name][0] / a]
    normalize(instances_ps)
    print(instances_ps)
    plot(categories, instances_ps, filename='s_dollar', ylabel='executions per second', title='Mandelbrot Scalar / Instance Price')


    instances_s = normalize(instances_s)
    categories = ['scalar']
    plot(categories, instances_s, filename='scalar_norm')
    instances_h = normalize(instances_h)
    categories = ['highway']
    plot(categories, instances_h, filename='highway_norm')

    instances_s = {}
    for instance_name in folder_paths:
        with open(directory_path + '/' + instance_name + '/scalar_100.log', 'r') as file:
            scalar = file.read()
            scalar = pow(10, 9) / int(scalar_meam(scalar)[0]) / m[instance_name][0]
        instances_s[instance_name] = [scalar]
    categories = ['scalar']
    plot(categories, instances_s, filename='scalar_ref')
    instances_s = normalize(instances_s)
    plot(categories, instances_s, filename='scalar_ref_norm', ylabel='executions per second', title='Mandelbrot Scalar / Whetstone')

    instances_h = {}
    for instance_name in folder_paths:
        with open(directory_path + '/' + instance_name + '/highway_100.log', 'r') as file:
            highway = file.read()
            highway = pow(10, 9) / int(highway_meam(highway)[0]) / m[instance_name][0]
        instances_h[instance_name] = [highway]
    categories = ['highway']
    plot(categories, instances_h, filename='highway_ref')
    instances_h = normalize(instances_h)
    plot(categories, instances_h, filename='highway_ref_norm')


def AVX_comp():
    instance = ['c7a.metal-48xl', 'c7i.metal-48xl']
    avx = {}
    for instance_name in instance:
        with open(directory_path + '/' + instance_name + '/AVX-2' + '/highway_100.log', 'r') as file:
            highway = file.read()
        with open(directory_path + '/' + instance_name + '/AVX-2' + '/scalar_100.log', 'r') as file:
            scalar = file.read()
        avx[instance_name] = [float(scalar_meam(scalar)[0]) / float(highway_meam(highway)[0])]
    for instance_name in instance:
        with open(directory_path + '/' + instance_name + '/AVX-512' + '/highway_100.log', 'r') as file:
            highway = file.read()
        with open(directory_path + '/' + instance_name + '/AVX-2' + '/scalar_100.log', 'r') as file:
            scalar = file.read()
        avx[instance_name] += [float(scalar_meam(scalar)[0]) / float(highway_meam(highway)[0])]
    print('avx')
    print(avx)
    categories = ['AVX-2', 'AVX-512']
    plot(categories, avx, filename='AVX', ylabel='executions per second', title='x86 SIMD implementation')


def NEON_comp():
    instance = ['c7g.metal', 'c7gn.16xlarge']
    avx = {}

    for instance_name in instance:
        with open(directory_path + '/' + instance_name + '/NEON' + '/highway_100.log', 'r') as file:
            highway = file.read()
        with open(directory_path + '/' + instance_name + '/NEON' + '/scalar_100.log', 'r') as file:
            scalar = file.read()
        avx[instance_name] = [float(scalar_meam(scalar)[0]) / float(highway_meam(highway)[0])]
    for instance_name in instance:
        with open(directory_path + '/' + instance_name + '/SVE' + '/highway_100.log', 'r') as file:
            highway = file.read()
        with open(directory_path + '/' + instance_name + '/SVE' + '/scalar_100.log', 'r') as file:
            scalar = file.read()
        avx[instance_name] += [float(scalar_meam(scalar)[0]) / float(highway_meam(highway)[0])]
    print('sve')
    print(avx)
    categories = ['NEON', 'SVE']
    plot(categories, avx, filename='NEON', ylabel='executions per second', title='ARM SIMD implementation')


if __name__ == '__main__':
    directory_path = '../../s3/results/9-simd'
    categories = ['highway']
    m = {}

    # Get a list of all items (files and folders) in the directory
    folder_paths = sorted(os.listdir(directory_path))
    for instance_name in folder_paths:
        m[instance_name] = [multi(instance_name)]

    main()
    AVX_comp()
    NEON_comp()

