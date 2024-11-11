import matplotlib.pyplot as plt
import threading

# List of processes with attributes: (Process ID, Priority, Burst Time, Arrival Time)
processes = [
    ("P1", 8, 15, 0),
    ("P2", 3, 20, 0),
    ("P3", 4, 20, 20),
    ("P4", 4, 20, 25),
    ("P5", 5, 5, 45),
    ("P6", 5, 15, 55)
]

# Sort processes by arrival time, and in case of tie, by priority (lower value is higher priority)
processes.sort(key=lambda x: (x[3], x[1]))

# Initialize variables for storing times and Gantt chart data
completion_time = {}
turnaround_time = {}
waiting_time = {}
gantt_chart = []  # For storing Gantt chart information

# Function to calculate scheduling times and populate Gantt chart
def calculate_times():
    global current_time
    current_time = 0

    remaining_burst_time = {process[0]: process[2] for process in processes}  # Remaining burst time of each process
    arrival_time = {process[0]: process[3] for process in processes}  # Arrival time of each process
    ready_queue = []  # A queue to store the ready processes
    gantt_chart_local = []  # Store Gantt chart for this function

    # Run until all processes are completed
    while remaining_burst_time:
        # Add processes to the queue which have arrived by current time
        for process in processes:
            process_id, priority, burst_time, arrival_time_value = process
            if arrival_time_value <= current_time and process_id not in [p[0] for p in ready_queue] and remaining_burst_time[process_id] > 0:
                ready_queue.append(process)

        # If no processes are in the ready queue, just increment time
        if not ready_queue:
            current_time += 1
            continue

        # Sort the ready queue by priority and by arrival time
        ready_queue.sort(key=lambda x: (x[1], arrival_time[x[0]]))

        # Select the process with the highest priority (lowest priority number)
        current_process = ready_queue[0]
        process_id = current_process[0]
        priority = current_process[1]
        burst_time = remaining_burst_time[process_id]

        # Execute one unit of time for the selected process
        remaining_burst_time[process_id] -= 1
        gantt_chart_local.append((process_id, current_time, current_time + 1))

        # If process is completed, record its completion time
        if remaining_burst_time[process_id] == 0:
            completion_time[process_id] = current_time + 1
            ready_queue = [p for p in ready_queue if p[0] != process_id]

        current_time += 1  # Move time forward by 1 unit

    # Calculate turnaround time and waiting time for each process
    for process in processes:
        process_id = process[0]
        burst_time = process[2]
        arrival_time_value = process[3]

        turnaround_time[process_id] = completion_time[process_id] - arrival_time_value
        waiting_time[process_id] = turnaround_time[process_id] - burst_time

    # Store the local gantt chart for plotting
    global gantt_chart
    gantt_chart = gantt_chart_local

    # Display results in a table format
    print(f"{'Process':<10}{'Arrival Time':<15}{'Burst Time':<15}{'Priority':<10}{'Completion Time':<20}{'Turnaround Time':<20}{'Waiting Time':<15}")
    for process in processes:
        process_id = process[0]
        print(f"{process_id:<10}{process[3]:<15}{process[2]:<15}{process[1]:<10}{completion_time[process_id]:<20}{turnaround_time[process_id]:<20}{waiting_time[process_id]:<15}")

# Function to plot the Gantt chart
def plot_gantt_chart():
    fig, gnt = plt.subplots(figsize=(12, 4))

    # Gantt Chart settings
    gnt.set_ylim(0, 10)
    gnt.set_xlim(0, max(completion_time.values()) + 10)
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_title("Gantt Chart for Preemptive Priority Scheduling")

    # Adding labels for each process
    gnt.set_yticks([5])
    gnt.set_yticklabels(['Processes'])

    # Plotting Gantt chart for each process
    for process in gantt_chart:
        process_id, start, finish = process
        gnt.broken_barh([(start, finish - start)], (3, 4), facecolors=('tab:blue'))

        # Display the process ID in the middle of the bar
        gnt.text(start + (finish - start) / 2, 5, process_id, ha='center', va='center', color='white', fontweight='bold')

        # Display the start and finish times at the edges of the bar
        gnt.text(start, 4.5, f'{start}', ha='center', va='center', color='black')
        gnt.text(finish, 4.5, f'{finish}', ha='center', va='center', color='black')

    # Show Gantt chart
    plt.tight_layout()
    plt.show()

# Start the calculation in a separate thread
calculation_thread = threading.Thread(target=calculate_times)
calculation_thread.start()
calculation_thread.join()  # Ensure calculations are complete before plotting

# Plot the Gantt chart in the main thread
plot_gantt_chart()
