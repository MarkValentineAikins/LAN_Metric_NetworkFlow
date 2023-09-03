import time
import psutil
import csv

# Set the duration of monitoring in seconds
monitoring_duration = 10

# Destination IP address or domain for latency measurement
destination_address = '192.168.8.103'  # Change this to your desired destination

# Lists to store metric samples
throughput_samples = []
packet_loss_samples = []
latency_samples = []

# Function to calculate the maximum efficient data transmission rate
def calculate_max_efficient_throughput():
    max_throughput = psutil.net_if_stats().get('eth0', {}).get('speed', 100) * 10**6 / 8  # Assuming 'eth0' as the network interface
    return max_throughput

# Start monitoring
start_time = time.time()

while time.time() - start_time < monitoring_duration:
    # Get current network statistics
    net_io = psutil.net_io_counters()

    # Calculate throughput (bytes per second)
    throughput = net_io.bytes_sent + net_io.bytes_recv
    throughput_samples.append(throughput)

    # Calculate packet loss rate
    packet_loss_rate = net_io.dropin + net_io.dropout  # Use dropin and dropout for packet loss
    packet_loss_samples.append(packet_loss_rate)

    # Measure latency (ping to a specific IP or domain)
    try:
        ping_result = psutil.subprocess.Popen(['ping', '-c', '1', destination_address], stdout=psutil.subprocess.PIPE).communicate()
        latency = float(ping_result[0].decode().split('time=')[1].split(' ms')[0])
        latency_samples.append(latency)
    except Exception as e:
        print(f"Error measuring latency: {e}")

    # Sleep for a brief interval
    time.sleep(1)

# Calculate average metrics
average_throughput = sum(throughput_samples) / len(throughput_samples)
average_packet_loss = sum(packet_loss_samples) / len(packet_loss_samples)
average_latency = sum(latency_samples) / len(latency_samples)

# Calculate maximum efficient data transmission rate
max_efficient_throughput = calculate_max_efficient_throughput()

# Print metrics
print("Average Throughput: {:.2f} bytes/s".format(average_throughput))
print("Average Packet Loss Rate: {:.2f}".format(average_packet_loss))
print("Average Latency: {:.2f} ms".format(average_latency))
print("Maximum Efficient Throughput: {:.2f} bytes/s".format(max_efficient_throughput))

# Export metrics to CSV file
def export_metrics_to_csv(throughput_samples, packet_loss_samples, latency_samples, max_efficient_throughput):
    filename = "lan_metrics.csv"

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Throughput (bytes/s)", "Packet Loss Rate", "Latency (ms)", "Max Efficient Throughput (bytes/s)"])

        for i in range(len(throughput_samples)):
            writer.writerow([throughput_samples[i], packet_loss_samples[i], latency_samples[i], max_efficient_throughput])

    print("Metrics exported to {}".format(filename))

# Export metrics to CSV file
export_metrics_to_csv(throughput_samples, packet_loss_samples, latency_samples, max_efficient_throughput)
