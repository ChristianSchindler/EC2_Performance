import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import cmcrameri.cm as cmc

# Set global font size
plt.rcParams.update({'font.size': 16})

color = cmc.batlow
def plot(impute_csv, output_svg='test.svg'):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(impute_csv, parse_dates=['Time'])

    # Plot GHz over time for each CPU
    plt.figure(figsize=(10, 6))

    # Assuming you have a column named 'CPU' that identifies different CPUs
    for i, cpu in enumerate(df['CPU'].unique()):
        cpu_data = df[df['CPU'] == cpu]
        plt.step(cpu_data['Time'], cpu_data['GHz'], where='post', label=f'CPU {cpu}', color=color(i))

    plt.title('CPU frequency in GHz over time for each thread')
    plt.xlabel('Time')
    plt.ylabel('GHz')
    # plt.legend()
    plt.grid(True)
    plt.savefig(output_svg, format='svg', bbox_inches='tight')
    plt.show()


def plot_amd_zoom(impute_csv, output_svg='test.svg'):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(impute_csv, parse_dates=['Time'])

    # Plot GHz over time for each CPU
    plt.figure(figsize=(10, 6))

    # Assuming you have a column named 'CPU' that identifies different CPUs
    for i, cpu in enumerate(df['CPU'].unique()):
        cpu_data = df[df['CPU'] == cpu]
        plt.step(cpu_data['Time'], cpu_data['GHz'], where='post', label=f'CPU {cpu}', color=color(i))

    plt.title('CPU frequency in GHz over time for each thread')
    plt.xlabel('Time')
    plt.ylabel('GHz')
    plt.ylim(3.02, 3.06)
    start_time = datetime.strptime('2024-03-10 15:31:29', '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime('2024-03-10 15:31:34', '%Y-%m-%d %H:%M:%S')

    plt.xlim(start_time, end_time)
    # plt.legend()
    plt.grid(True)
    plt.savefig(output_svg, format='svg', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    plot(impute_csv='../../s3/results/4-cpu-frequency/c7i.metal-48xl/output_single.csv', output_svg='c7i.metal-48xl_single.svg')
    plot(impute_csv='../../s3/results/4-cpu-frequency/c7i.metal-48xl/output_multi.csv', output_svg='c7i.metal-48xl_multi.svg')
    plot(impute_csv='../../s3/results/4-cpu-frequency/c7g.metal/output_single.csv',output_svg='c7g.metal_single.svg')
    plot(impute_csv='../../s3/results/4-cpu-frequency/c7g.metal/output_multi.csv',output_svg='c7g.metal_multi.svg')
    plot(impute_csv='../../s3/results/4-cpu-frequency/c7a.metal-48xl/output_single.csv', output_svg='c7a.metal-48xl_single.svg')
    plot(impute_csv='../../s3/results/4-cpu-frequency/c7a.metal-48xl/output_multi.csv', output_svg='c7a.metal-48xl_multi.svg')
    plot_amd_zoom(impute_csv='../../s3/results/4-cpu-frequency/c7a.metal-48xl/output_multi.csv', output_svg='c7a.metal-48xl_multi_zoom.svg')

    #plot(impute_csv='C:/Users/Christian\PycharmProjects/bachelor-thesis/s3/results/scaling_benchmark_test_2/c7i.metal-24xl/output_50.csv')
