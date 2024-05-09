import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import numpy as np
import collections
import networkx as nx
import random
from collections import Counter

# Initialize subplots as a 5x2 grid
fig, axs = plt.subplots(5, 2, figsize=(15, 25))  # Increase the number of rows to 5

# Global variables to track packet statistics
packet_freqs = collections.defaultdict(int)
total_traffic_volume = 0

# Protocol Distribution Over Time
protocol_ax = axs[0, 0]
protocol_ax.set_title('Protocol Distribution Over Time')
protocol_ax.set_xlabel('Time')
protocol_ax.set_ylabel('Packet Count')
protocol_line, = protocol_ax.plot([], [], marker='o', linestyle='-')

# Packet Size Distribution by Protocol
packet_size_ax = axs[0, 1]
packet_size_ax.set_title('Packet Size Distribution by Protocol')
packet_size_ax.set_xlabel('Packet Size (bytes)')
packet_size_ax.set_ylabel('Frequency')
packet_size_ax.set_xlim(0, 2000)
packet_size_ax.set_ylim(0, 100)
packet_size_lines = {}

# Inter-arrival Time Analysis
inter_arrival_ax = axs[1, 0]
inter_arrival_ax.set_title('Inter-arrival Time Analysis')
inter_arrival_ax.set_xlabel('Packet Index')
inter_arrival_ax.set_ylabel('Inter-arrival Time (seconds)')
inter_arrival_lines, = inter_arrival_ax.plot([], [])

# Flow Duration Analysis
flow_duration_ax = axs[1, 1]
flow_duration_ax.set_title('Flow Duration Analysis')
flow_duration_ax.set_xlabel('Flow Index')
flow_duration_ax.set_ylabel('Flow Duration (seconds)')
flow_duration_lines, = flow_duration_ax.plot([], [])

# Top Conversations
top_conversations_ax = axs[2, 0]
top_conversations_ax.set_title('Top Conversations')
top_conversations_ax.set_xlabel('Source-Destination Pair')
top_conversations_ax.set_ylabel('Packet Count')
top_conversations_ax.set_xticklabels([])
top_conversations_bars = []

# DNS Request Analysis
dns_ax = axs[2, 1]
dns_ax.set_title('DNS Request Analysis')
dns_ax.set_xlabel('DNS Query')
dns_ax.set_ylabel('Frequency')
dns_ax.set_xticklabels([])
dns_bars = []

# HTTP Request Analysis
http_ax = axs[3, 0]
http_ax.set_title('HTTP Request Analysis')
http_ax.set_xlabel('HTTP Method')
http_ax.set_ylabel('Count')
http_ax.set_xticklabels([])
http_bars = []

# Geolocation Visualization
geo_ax = axs[3, 1]
geo_ax.set_title('Geolocation Visualization')
geo_ax.set_xlabel('Longitude')
geo_ax.set_ylabel('Latitude')
geo_ax.scatter([], [])
geo_scatter = None

# Anomaly Detection
anomaly_ax = axs[3, 0]
anomaly_ax.set_title('Anomaly Detection')
anomaly_ax.set_xlabel('Time')
anomaly_ax.set_ylabel('Inter-Arrival Time (seconds)')
anomaly_lines, = anomaly_ax.plot([], [])

# Bandwidth Utilization
bandwidth_ax = axs[3, 1]
bandwidth_ax.set_title('Bandwidth Utilization')
bandwidth_ax.set_xlabel('Time')
bandwidth_ax.set_ylabel('Bandwidth Utilization (bytes)')
bandwidth_line, = bandwidth_ax.plot([], [])

# Network Topology Visualization
network_topology_ax = axs[4, 0]  # Access the new row for network topology
network_topology_ax.set_title('Network Topology Visualization')
network_topology_ax.set_xlabel('Device')
network_topology_ax.set_ylabel('Connections')

# Initialize an empty networkx graph to represent the network topology
network_topology_graph = nx.Graph()

# Add code to generate or load network topology data and create a networkx graph
# Example: Add nodes
network_topology_graph.add_node('Node1')
network_topology_graph.add_node('Node2')
# Example: Add edges
network_topology_graph.add_edge('Node1', 'Node2')

# Draw the networkx graph on the subplot for visualization
nx.draw(network_topology_graph, ax=network_topology_ax)


def update_plot(packets):
    global packet_freqs, total_traffic_volume

    # Protocol Distribution Over Time
    protocol_counts = collections.Counter([packet['IP'].proto for packet in packets if 'IP' in packet])
    protocols = list(protocol_counts.keys())
    counts = list(protocol_counts.values())
    protocol_line.set_data(protocols, counts)

    # Packet Size Distribution by Protocol
    packet_sizes = {protocol: [] for protocol in protocols}
    for packet in packets:
        if 'IP' in packet:
            protocol = packet['IP'].proto
            packet_sizes[protocol].append(len(packet))
    for protocol, sizes in packet_sizes.items():
        packet_size_lines[protocol].set_data(np.histogram(sizes, bins=30, range=(0, 2000)))

    # Inter-arrival Time Analysis
    inter_arrival_times = [packet['time'] - packets[i-1]['time'] for i, packet in enumerate(packets[1:], start=1)]
    inter_arrival_lines.set_data(range(1, len(inter_arrival_times) + 1), inter_arrival_times)

    # Flow Duration Analysis
    flow_durations = []
    flow_start_time = packets[0]['time']
    for packet in packets[1:]:
        if packet['time'] - flow_start_time > 1:  # Threshold for flow duration
            flow_durations.append(packet['time'] - flow_start_time)
            flow_start_time = packet['time']
    flow_duration_lines.set_data(range(1, len(flow_durations) + 1), flow_durations)

    # Top Conversations
    src_dst_pairs = collections.Counter([(packet['src'], packet['dst']) for packet in packets if 'IP' in packet])
    top_pairs = src_dst_pairs.most_common(10)
    labels = [f"{pair[0]} -> {pair[1]}" for pair, _ in top_pairs]
    counts = [count for _, count in top_pairs]
    for i, bar in enumerate(top_conversations_bars):
        bar.set_height(counts[i])
    top_conversations_ax.set_xticks(range(len(labels)))
    top_conversations_ax.set_xticklabels(labels, rotation=45)

    # DNS Request Analysis
    dns_queries = collections.Counter([packet['DNS']['qd']['qname'].decode('utf-8') for packet in packets if 'DNS' in packet and packet['DNS']['qd']['qname']])
    top_queries = dns_queries.most_common(10)
    labels = [query for query, _ in top_queries]
    counts = [count for _, count in top_queries]
    for i, bar in enumerate(dns_bars):
        bar.set_height(counts[i])
    dns_ax.set_xticks(range(len(labels)))
    dns_ax.set_xticklabels(labels, rotation=45)

    # HTTP Request Analysis
    http_methods = [packet['method'] for packet in packets if 'method' in packet and packet['method']]
    http_counts = collections.Counter(http_methods)
    methods = list(http_counts.keys())
    counts = list(http_counts.values())
    for i, bar in enumerate(http_bars):
        bar.set_height(counts[i])
    http_ax.set_xticks(range(len(methods)))
    http_ax.set_xticklabels(methods, rotation=45)

    # Geolocation Visualization
    src_ips = [packet['src'] for packet in packets if 'IP' in packet]
    dst_ips = [packet['dst'] for packet in packets if 'IP' in packet]
    # Dummy scatter plot, replace with actual geolocation data
    if src_ips or dst_ips:
        if geo_scatter:
            geo_scatter.remove()
        geo_scatter = geo_ax.scatter([], [], c='blue', label='Source IP')
        geo_ax.scatter([], [], c='red', label='Destination IP')
        geo_ax.legend()

    # Anomaly Detection
    inter_arrival_times = [packet['time'] - packets[i-1]['time'] for i, packet in enumerate(packets[1:], start=1)]
    anomaly_lines.set_data(range(1, len(inter_arrival_times) + 1), inter_arrival_times)

    # Bandwidth Utilization
    timestamps = [packet['time'] for packet in packets]
    packet_sizes = [packet['size'] for packet in packets]
    bandwidth_over_time = [sum(packet_sizes[:i+1]) for i in range(len(packet_sizes))]
    bandwidth_line.set_data(timestamps, bandwidth_over_time)


def generate_live_data():
    # Generate example live data
    example_data = {
        'IP': {'proto': random.choice([1, 6, 17])},
        'DNS': {'qd': {'qname': b'example.com'}},
        'method': random.choice(['GET', 'POST', 'PUT']),
        'time': random.uniform(0, 1000),
        'src': f'192.168.{random.randint(0, 255)}.{random.randint(0, 255)}',
        'dst': f'192.168.{random.randint(0, 255)}.{random.randint(0, 255)}',
        'size': random.randint(100, 1500)
    }
    return [example_data] * 100  # Return a list of 100 example packets


# def live_packet_visualization(packets):
#     update_plot(packets)
#     plt.draw()
#     plt.pause(0.01)


def live_packet_visualization(packets):
    print("Received packets:", packets)  # Print received packets for inspection
    update_plot(packets)
    plt.draw()
    plt.pause(0.01)


if __name__ == "__main__":
    # Example usage
    print("This script is intended to be imported and used for live visualization.")
    print("To use, import live_features.py and call the live_packet_visualization function with captured packets.")
    live_packet_visualization(generate_live_data())
