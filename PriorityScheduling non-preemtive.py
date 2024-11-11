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
    remaining_processes = processes[:]  # Work with a copy of the original list

    # Process the sorted list by priority
    while remaining_processes:
        # Choose the next process with the highest priority (lowest priority value)
        remaining_processes.sort(key=lambda x: (x[1], x[3]))  # Sort by priority and arrival time
        process = remaining_processes.pop(0)
        process_id, priority, burst_time, arrival_time = process

        # Wait if the next process arrives later than the current time
        if arrival_time > current_time:
            current_time = arrival_time

        # Calculate completion time
        completion_time[process_id] = current_time + burst_time
        current_time += burst_time  # Update current time after process completes

        # Record Gantt chart data
        gantt_chart.append((process_id, completion_time[process_id] - burst_time, completion_time[process_id]))

    # Calculate turnaround time and waiting time for each process
    for process in processes:
        process_id = process[0]
        burst_time = process[2]
        arrival_time = process[3]

        turnaround_time[process_id] = completion_time[process_id] - arrival_time
        waiting_time[process_id] = turnaround_time[process_id] - burst_time

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
    gnt.set_title("Gantt Chart for Non-Preemptive Priority Scheduling")

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
