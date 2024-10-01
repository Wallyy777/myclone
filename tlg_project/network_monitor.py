#!/user/bin/env python3

from scapy.all import sniff  # type: ignore
from anomaly_reporter import report_anomaly  # type: ignore
import psutil  # type: ignore
import time

# Thresholds for anomaly detection
MAX_PACKET_THRESHOLD = 1000  # Number of packets in a given time
HIGH_CPU_USAGE = 90  # Percentage of CPU usage considered suspicious

# Packet counter
packet_count = 0

# List to store captured packet info
captured_packets = []

# Callback function to analyze each captured packet
def analyze_packet(packet):
    global packet_count
    packet_count += 1
    captured_packets.append(packet.summary())

    # Example anomaly: Check for ICMP (ping) packets
    if packet.haslayer('ICMP'):
        report_anomaly("Suspicious ICMP packet detected!")

# Function to monitor system stats (CPU, memory, network I/O)
def monitor_system_stats():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > HIGH_CPU_USAGE:
            report_anomaly(f"High CPU usage detected: {cpu_usage}%")

        time.sleep(10)

# Function to monitor network traffic and check for anomalies
def monitor_network(interface):
    print(f"Starting network monitor on interface {interface}...")
    sniff(iface=interface, prn=analyze_packet, store=False)

# Function to check packet traffic and detect spikes
def monitor_packet_traffic(interval=10):
    global packet_count
    while True:
        time.sleep(interval)
        if packet_count > MAX_PACKET_THRESHOLD:
            report_anomaly(f"High packet traffic detected: {packet_count} packets in {interval} seconds")
        packet_count = 0  # Reset packet count for the next interval

if __name__ == "__main__":
    import threading

    # Set up monitoring on a specific network interface
    interface = "ens3"  # This is where we set your interface to "ens3"

    # Start system and network monitoring in separate threads
    system_thread = threading.Thread(target=monitor_system_stats)
    network_thread = threading.Thread(target=monitor_network, args=(interface,))
    traffic_thread = threading.Thread(target=monitor_packet_traffic)

    system_thread.start()
    network_thread.start()
    traffic_thread.start()

    system_thread.join()
    network_thread.join()
    traffic_thread.join()

