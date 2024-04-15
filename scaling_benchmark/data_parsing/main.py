import matplotlib.pyplot as plt
import os
import re
import csv
import numpy as np
import cmcrameri.cm as cmc

# Set global font size
plt.rcParams.update({'font.size': 16})

color = cmc.batlowS


def get_top_x_percent_value(arr, x=0.05):
    # Sort the array in descending order
    sorted_arr = sorted(arr, reverse=True)

    # Calculate the index corresponding to the 5th percentile
    index_5_percent = int(x * len(sorted_arr))

    # Retrieve the element at that index
    top_5_percent_value = sorted_arr[index_5_percent]

    return top_5_percent_value


def get_WH(content: str) -> list[list[int]]:
    return re.compile(rf'Double-Precision Whetstone\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)').findall(content)


def plot_abs(score_per, frequency, instance_name):
    # Extracting x values
    x_values = list(score_per.keys())

    # Extracting y values
    y1_values = np.array(list(score_per.values()))
    y2_values = np.array(list(frequency.values()))

    # Creating the plot
    fig, ax1 = plt.subplots()

    # Plotting the first set of data
    ax1.plot(x_values, y1_values, label='Whetstone score / vCPU', color=color(3))
    ax1.set_xlabel('used vCPU')
    ax1.set_ylabel('score_per', color=color(3))

    # Creating the second y-axis (right)
    ax2 = ax1.twinx()
    ax2.plot(x_values, y2_values, label='CPU frequency top 5%', color=color(2))
    ax2.set_ylabel('frequency', color=color(2))
    plt.xlim(1, 96)
    plt.axline((0.5, 0), slope=1, color='k', transform=plt.gca().transAxes, linestyle="--")

    # Adding legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True,
               shadow=True, ncol=3)

    plt.title('Development of CPU frequency and points per used vCPU')
    fig.tight_layout()  # Adjust layout to make room for the second axis
    plt.savefig(f'{instance_name}.svg', format='svg', bbox_inches='tight')
    plt.show()


def plot_norm(score_per, frequency, instance_name):
    # Extracting x values
    x_values = list(score_per.keys())

    # Extracting y values
    y1_values = np.array(list(score_per.values()))
    y2_values = np.array(list(frequency.values()))
    y1_values = y1_values / np.max(y1_values) * 100
    y2_values = y2_values / np.max(y2_values) * 100
    print(y2_values)

    # Creating the plot
    fig, ax1 = plt.subplots()

    # Plotting the first set of data
    ax1.plot(x_values, y1_values, label='Whetstone score / vCPU', color=color(3))
    ax1.set_xlabel('used vCPU')
    ax1.set_ylabel('% of max')

    ax1.plot(x_values, y2_values, label='CPU frequency top 5%', color=color(2))

    ax1.legend( )
    plt.xlim(1, 96)
    plt.ylim(78, 102)
    plt.vlines(x=[48], ymin=[75], ymax=[105], color='k', linestyle='dashed')
    plt.title('Development of CPU frequency and points per used vCPU')
    fig.tight_layout()  # Adjust layout to make room for the second axis
    plt.savefig(f'norm_{instance_name}.svg', format='svg', bbox_inches='tight')
    plt.show()


def plot_frequency(frequency, instance_name):
    # Extracting x values
    x_values = list(frequency.keys())
    print(x_values)

    # Extracting y values
    y_values = np.array(list(frequency.values()))
    # Creating the second y-axis (right)
    plt.plot(x_values, y_values, label='CPU frequency top 5%', color=color(2))
    plt.xlim(1, 96)
    plt.axline((0.5, 0), slope=1, color='k', transform=plt.gca().transAxes, linestyle="--")

    plt.ylabel('frequency in GHz')
    plt.xlabel('used vCPU')

    plt.title('Development of CPU frequency per used vCPU')
    plt.savefig(f'frequency_{instance_name}.svg', format='svg', bbox_inches='tight')
    plt.show()


def main():
    directory_path = '../../s3/results/scaling_benchmark_test_2'
    folder_paths = sorted(os.listdir(directory_path))
    score: dict[int, float] = dict()
    frequency: dict[int, float] = dict()

    for instance_name in ['c7i.metal-24xl', 'c7i.metal-24xl-r2']:
        # points
        files = sorted(os.listdir(directory_path + '/' + instance_name))
        for f in files:
            pattern = r'result_(\d+)\.txt'
            match = re.search(pattern, f)
            if match:
                cores = int(match.group(1))
                with open(directory_path + '/' + instance_name + f'/result_{cores}.txt') as a:
                    if cores in frequency:
                        score[cores] += float(get_WH(a.read())[0][2])
                        score[cores] /= 2
                    else:
                        score[cores] = float(get_WH(a.read())[0][2])
        score = dict(sorted(score.items()))
        score_per = {key: value / key for key, value in score.items()}
        print(score_per)

        # frequency
        for f in files:
            pattern = r'output_(\d+)\.csv'
            match = re.search(pattern, f)
            if match:
                cores = int(match.group(1))
                ghz_values = []
                with open(directory_path + '/' + instance_name + f'/output_{cores}.csv', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        ghz_values.append(float(row['GHz']))
                if cores in frequency:
                    frequency[cores] += get_top_x_percent_value(ghz_values, 0.05 * cores / 96)
                    frequency[cores] /= 2
                else:
                    frequency[cores] = get_top_x_percent_value(ghz_values, 0.05 * cores / 96)
        frequency = dict(sorted(frequency.items()))
        print(frequency)

    #plot_abs(score_per, frequency, 'c7i.metal-24xl')
    plot_norm(score_per, frequency, 'c7i.metal-24xl')
    #plot_frequency(frequency, 'c7i.metal-24xl')


if __name__ == '__main__':
    main()
