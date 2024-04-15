import threading
import subprocess
import os
import csv
from datetime import datetime


def run_bash_script(copies: int = 1):
    bash_script_path = f"./Run -c {copies} -i 1 whets > ../result_{copies}.txt"
    process = subprocess.Popen([bash_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()

    if process.returncode == 0:
        print("Bash script executed successfully.")
    else:
        print(f"Error executing Bash script. Exit code: {process.returncode}")


data: list[list[str]] = []


def process_and_write_to_csv(line):
    cpu_pos = line.find("CPU")
    ghz_pos = line.find("GHz")
    hash_pos = line.find('#')
    current_datetime = datetime.now()
    # time = current_datetime - start_time
    if cpu_pos != -1 and ghz_pos != -1:
        cpu_info = line[cpu_pos + 3:cpu_pos + 6].replace(' ', '')
        ghz_info = line[hash_pos + 1:ghz_pos - 1].replace(' ', '')

        data.append([cpu_info, current_datetime, ghz_info])


def parse_csv():
    with open("perf.out", "r") as input_file:
        for line in input_file:
            process_and_write_to_csv(line.strip())


def do_something_else(csv_file_name: str = 'output.csv'):
    command = "perf stat -d -o \"perf.out\" --per-thread -A & sleep 0.5 && kill -INT $!"
    for i in range(0, 45):
        # print(i)
        subprocess.run(command, shell=True)
        # print(i)
        parse_csv()

    # Open the CSV file in write mode
    with open(f'./results/{csv_file_name}', 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the header (keys) to the CSV file
        csv_writer.writerow(['CPU', 'Time', 'GHz'])

        # Write each key-value pair to the CSV file
        for a in data:
            csv_writer.writerow(a)


def main(copies, csv_file_name):
    data.clear()
    # Create a thread for running the Bash script
    bash_script_thread = threading.Thread(target=run_bash_script, args=(copies,))

    # Start the thread for running the Bash script
    bash_script_thread.start()

    # Start a separate thread for doing something else in Python
    python_task_thread = threading.Thread(target=do_something_else, args=(csv_file_name,))
    python_task_thread.start()

    # Wait for both threads to finish
    bash_script_thread.join()
    python_task_thread.join()


if __name__ == "__main__":
    num_cores = os.cpu_count()
    print(num_cores)
    for i in range(1, num_cores + 1):
        main(i, f"output_{i}.csv")
