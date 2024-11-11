import threading
import time
import matplotlib.pyplot as plt

# List of processes with their attributes: (Process ID, Priority, Burst Time, Arrival Time)
processes = [
    ("P1", 8, 15, 0),
    ("P2", 3, 20, 0),
    ("P3", 4, 20, 20),
    ("P4", 4, 20, 25),
    ("P5", 5, 5, 45),
    ("P6", 5, 15, 55)
]

# Sorting processes by arrival time for FCFS
processes.sort(key=lambda x: x[3])

# Initializing required data structures
completion_times = [0] * len(processes)
turnaround_times = [0] * len(processes)
waiting_times = [0] * len(processes)
gantt_chart = []

# Lock to simulate process execution order in the main thread
lock = threading.Lock()
current_time = 0  # shared time counter

# Function to simulate each process
def run_process(process_id, burst_time, arrival_time, index):
    global current_time

    # Waiting until the arrival time
    while current_time < arrival_time:
        time.sleep(0.1)  # Pause briefly

    # Process enters the CPU
    with lock:
        start_time = max(current_time, arrival_time)
        finish_time = start_time + burst_time
        current_time = finish_time  # Move current time forward

        # Calculating times
        completion_times[index] = finish_time
        turnaround_times[index] = finish_time - arrival_time
        waiting_times[index] = turnaround_times[index] - burst_time

        # Adding to Gantt chart
        gantt_chart.append((process_id, start_time, finish_time))

# Creating and starting threads for each process
threads = []
for i, process in enumerate(processes):
    process_id, priority, burst_time, arrival_time = process
    thread = threading.Thread(target=run_process, args=(process_id, burst_time, arrival_time, i))
    threads.append(thread)
    thread.start()

# Waiting for all threads to complete
for thread in threads:
    thread.join()

# Displaying the table of times
print(
    f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Completion Time':<20}{'Turnaround Time':<20}{'Waiting Time':<15}")
for i, process in enumerate(processes):
    process_id, priority, burst_time, arrival_time = process
    print(
        f"{process_id:<10}{arrival_time:<15}{burst_time:<15}{completion_times[i]:<20}{turnaround_times[i]:<20}{waiting_times[i]:<15}")

# Plotting the Gantt chart
fig, gantt_ax = plt.subplots(figsize=(10, 4))

# Gantt Chart
gantt_ax.set_ylim(0, 10)
gantt_ax.set_xlim(0, max(completion_times) + 10)
gantt_ax.set_xlabel('Time')
gantt_ax.set_ylabel('Processes')
gantt_ax.set_title("Gantt Chart for FCFS Scheduling with Threads")

# Adding labels for each process
gantt_ax.set_yticks([5])
gantt_ax.set_yticklabels(['Processes'])

# Plotting the Gantt chart for each process
for process in gantt_chart:
    process_id, start, finish = process
    gantt_ax.broken_barh([(start, finish - start)], (3, 4), facecolors=('tab:blue'))

    # Display the process ID in the middle of the bar
    gantt_ax.text(start + (finish - start) / 2, 5, process_id, ha='center', va='center', color='white', fontweight='bold')

    # Display the start and finish times at the edges of the bar
    gantt_ax.text(start, 4.5, f'{start}', ha='center', va='center', color='black')
    gantt_ax.text(finish, 4.5, f'{finish}', ha='center', va='center', color='black')

# Show plot
plt.tight_layout()
plt.show()
