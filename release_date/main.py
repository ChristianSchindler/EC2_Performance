import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})

def vcpu():
    # Load the CSV files into pandas DataFrames
    intel_path = 'intel_data.csv'
    amd_path = 'amd_data.csv'
    graviton_path = 'graviton_data.csv'

    intel_df = pd.read_csv(intel_path, parse_dates=['Released'], dayfirst=True)
    amd_df = pd.read_csv(amd_path, parse_dates=['Released'], dayfirst=True)
    graviton_df = pd.read_csv(graviton_path, parse_dates=['Released'], dayfirst=True)

    # Sort the DataFrames by 'Released' (optional but recommended for time series data)
    intel_df = intel_df.sort_values(by='Released')
    amd_df = amd_df.sort_values(by='Released')
    graviton_df = graviton_df.sort_values(by='Released')

    # Plot the time series graph with step lines and markers for each architecture
    plt.figure(figsize=(10, 6))

    plt.step(intel_df['Released'], intel_df['vCPU'], where='post', label='Intel', color='#0068B5', marker='o')
    plt.step(amd_df['Released'], amd_df['vCPU'], where='post', label='AMD', color='#ED1C24', marker='o')
    plt.step(graviton_df['Released'], graviton_df['vCPU'], where='post', label='Amazon', color='#FF9900',
             marker='o')

    # Annotate each data point with its corresponding row information
    for i, row in intel_df.iterrows():
        if row['Name'] == 'c7i':
            plt.annotate(f"c7i  c7a", (row['Released'], row['vCPU'] + 2), ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}", (row['Released'], row['vCPU'] + 2), ha='center', fontsize=15)

    for i, row in amd_df.iterrows():
        if row['Name'] == 'c7a':
            continue
        plt.annotate(f"{row['Name']}", (row['Released'], row['vCPU'] + 2), ha='center', fontsize=15)

    for i, row in graviton_df.iterrows():
        plt.annotate(f"{row['Name']}", (row['Released'], row['vCPU'] + 2), ha='center', fontsize=15)

    # Add labels and title
    plt.xlabel('Release Date')
    plt.ylabel('vCPU')
    # plt.title('Time Series Graph of vCPU with Step Lines, Markers, and Data Point Labels')

    plt.ylim(0, 210)

    # Display the legend
    plt.legend()
    plt.savefig('release_date.svg', format='svg', bbox_inches='tight')

    # Show the plot
    plt.show()


def multi():
    # Load the CSV files into pandas DataFrames
    intel_path = 'intel_data_multi.csv'
    amd_path = 'amd_data_multi.csv'
    graviton_path = 'graviton_data_multi.csv'

    intel_df = pd.read_csv(intel_path, parse_dates=['Released'], dayfirst=True)
    amd_df = pd.read_csv(amd_path, parse_dates=['Released'], dayfirst=True)
    graviton_df = pd.read_csv(graviton_path, parse_dates=['Released'], dayfirst=True)

    # Sort the DataFrames by 'Released' (optional but recommended for time series data)
    intel_df = intel_df.sort_values(by='Released')
    amd_df = amd_df.sort_values(by='Released')
    graviton_df = graviton_df.sort_values(by='Released')

    # Plot the time series graph with step lines and markers for each architecture
    plt.figure(figsize=(10, 6))

    plt.step(intel_df['Released'], intel_df['score'], where='post', label='Intel', color='#0068B5', marker='o')
    plt.step(amd_df['Released'], amd_df['score'], where='post', label='AMD', color='#ED1C24', marker='o')
    plt.step(graviton_df['Released'], graviton_df['score'], where='post', label='Amazon', color='#FF9900',
             marker='o')

    # Annotate each data point with its corresponding row information
    for i, row in intel_df.iterrows():
        plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 1000), ha='center', fontsize=15)

    for i, row in amd_df.iterrows():
        plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 1000), ha='center', fontsize=15)

    for i, row in graviton_df.iterrows():
        if row['Name'] == 'c7gn':
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] - 6000), ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}",
                     (row['Released'], row['score'] + 1000),
                     ha='center', fontsize=15)

    # Add labels and title
    plt.xlabel('Release Date')
    plt.ylabel('UnixBench multi-core score')
    # plt.title('Time Series Graph of Multicore Score')

    plt.ylim(0, 100_000)

    # Display the legend
    plt.legend()
    plt.savefig('release_date_multi.svg', format='svg', bbox_inches='tight')

    # Show the plot
    plt.show()


def single():
    # Load the CSV files into pandas DataFrames
    intel_path = 'intel_data_single.csv'
    amd_path = 'amd_data_single.csv'
    graviton_path = 'graviton_data_single.csv'

    intel_df = pd.read_csv(intel_path, parse_dates=['Released'], dayfirst=True)
    amd_df = pd.read_csv(amd_path, parse_dates=['Released'], dayfirst=True)
    graviton_df = pd.read_csv(graviton_path, parse_dates=['Released'], dayfirst=True)

    # Sort the DataFrames by 'Released' (optional but recommended for time series data)
    intel_df = intel_df.sort_values(by='Released')
    amd_df = amd_df.sort_values(by='Released')
    graviton_df = graviton_df.sort_values(by='Released')

    # Plot the time series graph with step lines and markers for each architecture
    plt.figure(figsize=(10, 6))

    plt.step(intel_df['Released'], intel_df['score'], where='post', label='Intel', color='#0068B5', marker='o')
    plt.step(amd_df['Released'], amd_df['score'], where='post', label='AMD', color='#ED1C24', marker='o')
    plt.step(graviton_df['Released'], graviton_df['score'], where='post', label='Amazon', color='#FF9900',
             marker='o')

    # Annotate each data point with its corresponding row information
    for i, row in intel_df.iterrows():
        plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 30), ha='center', fontsize=15)

    for i, row in amd_df.iterrows():
        if row['Name'] == 'c7a':
            plt.annotate(f"{row['Name']}",
                         (row['Released'], row['score'] - 130),
                         ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 30), ha='center', fontsize=15)

    for i, row in graviton_df.iterrows():
        if row['Name'] == 'a1' or row['Name'] == 'c7gn':
            plt.annotate(f"{row['Name']}",
                         (row['Released'], row['score'] - 130),
                         ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}",
                     (row['Released'], row['score'] + 30),
                     ha='center', fontsize=15)

    # Add labels and title
    plt.xlabel('Release Date')
    plt.ylabel('UnixBench single-core score')
    # plt.title('Time Series Graph of Multicore Score')
    plt.ylim(0, 2_500)

    # Display the legend
    plt.legend()
    plt.savefig('release_date_singel.svg', format='svg', bbox_inches='tight')

    # Show the plot
    plt.show()


def single_dray():
    # Load the CSV files into pandas DataFrames
    intel_path = 'intel_data_single_dray.csv'
    amd_path = 'amd_data_single_dray.csv'
    graviton_path = 'graviton_data_single_dray.csv'

    intel_df = pd.read_csv(intel_path, parse_dates=['Released'], dayfirst=True)
    amd_df = pd.read_csv(amd_path, parse_dates=['Released'], dayfirst=True)
    graviton_df = pd.read_csv(graviton_path, parse_dates=['Released'], dayfirst=True)

    # Sort the DataFrames by 'Released' (optional but recommended for time series data)
    intel_df = intel_df.sort_values(by='Released')
    amd_df = amd_df.sort_values(by='Released')
    graviton_df = graviton_df.sort_values(by='Released')

    # Plot the time series graph with step lines and markers for each architecture
    plt.figure(figsize=(10, 6))

    plt.step(intel_df['Released'], intel_df['score'], where='post', label='Intel', color='#0068B5', marker='o')
    plt.step(amd_df['Released'], amd_df['score'], where='post', label='AMD', color='#ED1C24', marker='o')
    plt.step(graviton_df['Released'], graviton_df['score'], where='post', label='Amazon', color='#FF9900',
             marker='o')

    # Annotate each data point with its corresponding row information
    for i, row in intel_df.iterrows():
        plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 50), ha='center', fontsize=15)

    for i, row in amd_df.iterrows():
        if row['Name'] == 'c7a':
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] - 320), ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 50), ha='center', fontsize=15)

    for i, row in graviton_df.iterrows():
        plt.annotate(f"{row['Name']}",
                     (row['Released'], row['score'] - 300),
                     ha='center', fontsize=15)

    # Add labels and title
    plt.xlabel('Release Date')
    plt.ylabel('Dhrystone single-core score')
    # plt.title('Time Series Graph of Multicore Score')
    plt.ylim(0, 5_500)

    # Display the legend
    plt.legend()
    plt.savefig('release_date_single_dray.svg', format='svg', bbox_inches='tight')

    # Show the plot
    plt.show()


def multi_dray():
    # Load the CSV files into pandas DataFrames
    intel_path = 'intel_data_multi_dray.csv'
    amd_path = 'amd_data_multi_dray.csv'
    graviton_path = 'graviton_data_multi_dray.csv'

    intel_df = pd.read_csv(intel_path, parse_dates=['Released'], dayfirst=True)
    amd_df = pd.read_csv(amd_path, parse_dates=['Released'], dayfirst=True)
    graviton_df = pd.read_csv(graviton_path, parse_dates=['Released'], dayfirst=True)

    # Sort the DataFrames by 'Released' (optional but recommended for time series data)
    intel_df = intel_df.sort_values(by='Released')
    amd_df = amd_df.sort_values(by='Released')
    graviton_df = graviton_df.sort_values(by='Released')

    # Plot the time series graph with step lines and markers for each architecture
    plt.figure(figsize=(10, 6))

    plt.step(intel_df['Released'], intel_df['score'], where='post', label='Intel', color='#0068B5', marker='o')
    plt.step(amd_df['Released'], amd_df['score'], where='post', label='AMD', color='#ED1C24', marker='o')
    plt.step(graviton_df['Released'], graviton_df['score'], where='post', label='Amazon', color='#FF9900',
             marker='o')

    # Annotate each data point with its corresponding row information
    for i, row in intel_df.iterrows():
        plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 10000), ha='center', fontsize=15)

    for i, row in amd_df.iterrows():
        if row['Name'] == 'c5a':
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 20000), ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 10000), ha='center', fontsize=15)

    for i, row in graviton_df.iterrows():
        if row['Name'] == 'a1':
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] + 10000), ha='center', fontsize=15)
        else:
            plt.annotate(f"{row['Name']}", (row['Released'], row['score'] - 40000), ha='center', fontsize=15)

    # Add labels and title
    plt.xlabel('Release Date')
    plt.ylabel('Dhrystone multi-core score')
    # plt.title('Time Series Graph of Multicore Score')
    plt.ylim(0, 800_000)

    # Display the legend
    plt.legend()
    plt.savefig('release_date_multi_dray.svg', format='svg', bbox_inches='tight')

    # Show the plot
    plt.show()


if __name__ == '__main__':
    vcpu()
    single()
    multi()
    single_dray()
    multi_dray()
