import matplotlib.pyplot as plt
import numpy as np
import cmcrameri.cm as cmc

# Set global font size
plt.rcParams.update({'font.size': 16})

color = cmc.batlowS


def convert_strings_to_floats(string_array) -> list[float]:
    float_array = [float(value) for value in string_array]
    return float_array


def div_array(array1: list, array2: list, factor: int | float = 1) -> list[float]:
    array1 = convert_strings_to_floats(array1)
    array2 = convert_strings_to_floats(array2)
    result_array = [a / b / factor for a, b in zip(array1, array2)]
    return result_array


def normalize(instances: dict[str, list[float | str]]) -> dict[str, list[float]]:
    max_list = [max(convert_strings_to_floats(values)) for values in zip(*instances.values())]  # print(result_list)
    for instance_name in instances.keys():
        instances[instance_name] = div_array(instances[instance_name], max_list)
    return instances


def plot(categories: list[str], instances: dict[str, list[str | float | int]], xlabel='', ylabel='', title='',
         filename='test', suffix='', rotation_x=0, extra_with=False):
    bar_width = 0.35
    bar_positions = np.arange(len(categories)) * len(instances) / 2.5
    if extra_with:
        plt.figure(figsize=(16, 6))  # Width: 8 inches, Height: 6 inches
    else:
        plt.figure(figsize=(8, 6))  # Width: 8 inches, Height: 6 inches

    for i, instance in enumerate(sorted(instances.keys())):
        # Create grouped bar chart
        plt.bar(bar_positions, convert_strings_to_floats(instances[instance]),
                width=bar_width, label=instance, color=color(i))
        bar_positions = bar_positions + bar_width

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # Add a legend
    if extra_with:
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    else:  # Set x-axis ticks and labels
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
    plt.xticks(bar_positions - bar_width * (len(instances) + 1) / 2, categories, rotation=rotation_x)

    # Save the figure to an SVG file
    plt.savefig(filename + suffix + '.svg', format='svg', bbox_inches='tight')

    # Display the plot (optional)
    plt.show()


def to_float_array(string_array: list[str]) -> list[float]:
    return [float(x) for x in string_array]


def average(float_array: list[float]) -> float:
    return round(sum(float_array) / len(float_array), 2)


def filter_dictionary(input_dict, filter_keys):
    if not filter_keys:
        return input_dict
    # Using dictionary comprehension to filter keys
    filtered_dict = {key: value for key, value in input_dict.items() if key in filter_keys}
    return filtered_dict
