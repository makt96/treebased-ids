from scapy.all import rdpcap
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import networkx as nx
from scapy.layers.http import HTTP
from scapy.layers.dns import DNS
from scapy.layers.inet import IP
from scapy.all import TCP, UDP, ICMP, ARP
import os


# Use Agg backend to avoid GUI-related warnings
import matplotlib
matplotlib.use('Agg')

# Get the absolute path to the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory where the images will be saved
image_dir = os.path.join(script_dir, 'static', 'images')


# Function for Protocol Distribution Over Time
def protocol_distribution_over_time(packets):
    if not packets:
        print("Error: No packets data found.")
        return

    protocols = Counter()
    timestamps = []

    # Collect timestamps and protocol counts separately
    for packet in packets:
        if packet.haslayer('IP'):
            protocol = packet['IP'].proto
            protocols[protocol] += 1
            timestamps.append(packet.time)

    # Align timestamps and protocol counts
    timestamps = timestamps[:len(protocols)]

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, list(protocols.values()), marker='o', linestyle='-')
    plt.title('Protocol Distribution Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Packet Count')
    plt.grid(True)
    # plt.savefig('static/images/protocol_distribution_over_time.png')  # Save the plot as a PNG image
    plt.savefig(os.path.join(image_dir, 'protocol_distribution_over_time.png'))
    plt.close()


# Function for Packet Size Distribution by Protocol
def packet_size_distribution_by_protocol(packets):
    packet_sizes = {TCP: [], UDP: [], ICMP: [], ARP: [], "Unknown": []}

    for packet in packets:
        if packet.haslayer(IP):
            protocol = packet['IP'].proto
            if protocol in packet_sizes:
                packet_sizes[protocol].append(len(packet))
            else:
                packet_sizes["Unknown"].append(len(packet))

    plt.figure(figsize=(10, 6))
    for protocol, sizes in packet_sizes.items():
        sns.histplot(sizes, bins=30, kde=True, label=str(protocol))
    plt.title('Packet Size Distribution by Protocol')
    plt.xlabel('Packet Size (bytes)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig('static/images/packet_size_distribution_by_protocol.png')  # Save the plot as a PNG image
    plt.close()

# Function for Inter-arrival Time Analysis
def inter_arrival_time_analysis(packets):
    inter_arrival_times = []

    prev_time = packets[0].time
    for packet in packets[1:]:
        inter_arrival_times.append(packet.time - prev_time)
        prev_time = packet.time

    plt.figure(figsize=(10, 6))
    sns.histplot(inter_arrival_times, bins=30, kde=True)
    plt.title('Inter-arrival Time Analysis')
    plt.xlabel('Inter-arrival Time')
    plt.ylabel('Frequency')
    plt.savefig('static/images/inter_arrival_time_analysis.png')  # Save the plot as a PNG image
    plt.close()

# Function for Flow Duration Analysis
def flow_duration_analysis(packets):
    flow_durations = []

    flow_start_time = packets[0].time
    for packet in packets[1:]:
        if packet.time - flow_start_time > 1:  # Threshold for flow duration
            flow_durations.append(packet.time - flow_start_time)
            flow_start_time = packet.time

    plt.figure(figsize=(10, 6))
    sns.histplot(flow_durations, bins=30, kde=True)
    plt.title('Flow Duration Analysis')
    plt.xlabel('Flow Duration')
    plt.ylabel('Frequency')
    plt.savefig('static/images/flow_duration_analysis.png')  # Save the plot as a PNG image
    plt.close()

# Function for Top Conversations
def top_conversations(packets):
    src_dst_pairs = Counter()

    for packet in packets:
        if packet.haslayer('IP'):
            src_ip = packet['IP'].src
            dst_ip = packet['IP'].dst
            src_dst_pairs[(src_ip, dst_ip)] += 1

    top_pairs = src_dst_pairs.most_common(10)
    labels = [f"{pair[0]} -> {pair[1]}" for pair, _ in top_pairs]
    counts = [count for _, count in top_pairs]

    plt.figure(figsize=(12, 6))
    sns.barplot(x=labels, y=counts)
    plt.title('Top Conversations')
    plt.xlabel('Source-Destination Pair')
    plt.ylabel('Packet Count')
    plt.xticks(rotation=45)
    plt.savefig('static/images/top_conversations.png')  # Save the plot as a PNG image
    plt.close()

def dns_request_analysis(packets):
    dns_queries = Counter()

    # Iterate through each packet
    for packet in packets:
        # Check if the packet has a DNS layer
        if packet.haslayer('DNS'):
            # Try to access the DNS query name
            try:
                query = packet['DNS'].qd.qname.decode('utf-8')
                dns_queries[query] += 1
            except AttributeError:
                # If there is an AttributeError, the DNS query name is not accessible
                print("Error: Unable to access DNS query name in packet.")
                continue

    # Get the top 10 DNS queries
    top_queries = dns_queries.most_common(10)
    labels = [query for query, _ in top_queries]
    counts = [count for _, count in top_queries]

    # Check if counts is empty
    if not counts:
        print("No DNS queries found for analysis.")
        return

    # Plot the top DNS queries
    plt.figure(figsize=(12, 6))
    sns.barplot(x=labels, y=counts)
    plt.title('Top DNS Queries')
    plt.xlabel('DNS Query')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.savefig('static/images/dns_request_analysis.png')  # Save the plot as a PNG image
    plt.close()


# Function for HTTP Request Analysis
def http_request_analysis(packets):
    try:
        methods = [packet['method'] for packet in packets if 'method' in packet and packet['method']]
        if not methods:
            print("No HTTP methods found for analysis.")
            return

        # Count the occurrences of each HTTP method
        method_counts = {}
        for method in methods:
            method_counts[method] = method_counts.get(method, 0) + 1

        methods, counts = zip(*method_counts.items()) if method_counts else ([], [])

        if not methods:
            print("No HTTP methods available to plot.")
            return

        # Plotting the barplot of HTTP methods
        sns.barplot(x=list(methods), y=list(counts))
        plt.xlabel('HTTP Methods')
        plt.ylabel('Count')
        plt.title('HTTP Request Analysis')
        plt.savefig('static/images/http_request_analysis.png')  # Save the plot as a PNG image
        plt.close()

    except Exception as e:
        print("An error occurred during HTTP request analysis:", str(e))


#Geolocation Analysis

def geolocation_visualization(packets):
    src_ips = [packet[IP].src for packet in packets if IP in packet]
    dst_ips = [packet[IP].dst for packet in packets if IP in packet]

    # Assuming you have a mapping of IP addresses to their geolocations
    # Replace this with your actual implementation
    src_geolocations = {}
    dst_geolocations = {}

    src_locations = [src_geolocations[ip] for ip in src_ips if ip in src_geolocations]
    dst_locations = [dst_geolocations[ip] for ip in dst_ips if ip in dst_geolocations]

    # Check if either src_locations or dst_locations is empty
    if not src_locations and not dst_locations:
        print("No geolocations found for source or destination IPs.")
        return

    # Plotting the source and destination IP locations
    if src_locations:
        plt.scatter(*zip(*src_locations), label='Source IP', color='blue')
    if dst_locations:
        plt.scatter(*zip(*dst_locations), label='Destination IP', color='red')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Geolocation Visualization')
    plt.legend()

    # Check if both src_locations and dst_locations are empty
    if not src_locations or not dst_locations:
        plt.text(0.5, 0.5, "No geolocations found", horizontalalignment='center', verticalalignment='center')
    
    plt.savefig('static/images/geolocation_visualization.png')  # Save the plot as a PNG image
    plt.close()


# Function for Anomaly Detection
def anomaly_detection(packets):
    try:
        # Calculate packet arrival times
        arrival_times = [packet.time for packet in packets]

        # Calculate inter-arrival times
        inter_arrival_times = [t2 - t1 for t1, t2 in zip(arrival_times[:-1], arrival_times[1:])]

        # Calculate the threshold
        threshold = 2 * np.std(inter_arrival_times, dtype=np.float64)

        # Identify anomalies (i.e., inter-arrival times greater than the threshold)
        anomalies = [time for time in inter_arrival_times if time > threshold]

        # Plot inter-arrival times
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(inter_arrival_times) + 1), inter_arrival_times, label='Inter-Arrival Times', color='blue')
        plt.xlabel('Packet Index')
        plt.ylabel('Inter-Arrival Time (seconds)')
        plt.title('Inter-Arrival Times with Anomalies')
        plt.grid(True)

        # Highlight anomalies on the plot
        if anomalies:
            anomaly_indices = [i+1 for i, time in enumerate(inter_arrival_times) if time in anomalies]
            anomaly_values = [time for time in inter_arrival_times if time in anomalies]
            plt.scatter(anomaly_indices, anomaly_values, color='red', label='Anomalies')

        plt.legend()
        plt.savefig('static/images/anomaly_detection.png')  # Save the plot as a PNG image
        plt.close()

        # Return or visualize the results as needed
        return anomalies

    except Exception as e:
        print("An error occurred during anomaly detection:", str(e))
        return []

# Function for Bandwidth Utilization
def bandwidth_utilization(packets):
    try:
        # Extract timestamps and packet sizes
        timestamps = [packet.time for packet in packets]
        packet_sizes = [len(packet) for packet in packets]

        # Calculate the cumulative sum of packet sizes to represent bandwidth over time
        bandwidth_over_time = [sum(packet_sizes[:i+1]) for i in range(len(packet_sizes))]

        # Plot the bandwidth over time
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, bandwidth_over_time, color='blue')
        plt.title('Bandwidth Utilization Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Bandwidth Utilization (bytes)')
        plt.grid(True)
        plt.savefig('static/images/bandwidth_utilization.png')  # Save the plot as a PNG image
        plt.close()

        # Return the bandwidth over time data
        return timestamps, bandwidth_over_time

    except Exception as e:
        print("An error occurred during bandwidth utilization analysis:", str(e))
        return [], []

def network_topology_visualization(packets):
    try:
        # Create a directed graph for network topology visualization
        G = nx.DiGraph()

        # Extract source and destination IP addresses from packets
        src_ips = [packet['src_ip'] for packet in packets if 'src_ip' in packet and packet['src_ip']]
        dst_ips = [packet['dst_ip'] for packet in packets if 'dst_ip' in packet and packet['dst_ip']]

        # Check if either src_ips or dst_ips is empty
        if not src_ips or not dst_ips:
            print("No source or destination IP addresses found.")
            return

        # Add edges to the graph based on packet flows
        for src_ip, dst_ip in zip(src_ips, dst_ips):
            if src_ip and dst_ip:  # Ensure both source and destination IPs are not empty
                if G.has_edge(src_ip, dst_ip):
                    G[src_ip][dst_ip]['weight'] += 1
                else:
                    G.add_edge(src_ip, dst_ip, weight=1)

        # Check if the graph is empty
        if len(G.nodes()) == 0:
            print("No edges found to create the network topology.")
            return

        # Draw the network topology graph
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', edge_color='gray', width=2, alpha=0.8)
        plt.title('Network Topology Visualization')
        plt.savefig('static/images/network_topology_visualization.png')  # Save the plot as a PNG image
        plt.close()

    except Exception as e:
        print("An error occurred during network topology visualization:", str(e))

# Function for Correlation Analysis
def correlation_analysis(packets):
    try:
        # Extract relevant features for correlation analysis
        features = ['packet_size', 'src_packet_freq', 'dst_packet_freq', 'traffic_volume']

        # Extract feature values from packets
        feature_values = []
        for packet in packets:
            # Get the first layer of the packet
            first_layer = packet.getlayer(0)
            if first_layer:
                packet_features = []
                try:
                    # Attempt to retrieve all features
                    for feature in features:
                        value = first_layer.getfieldval(feature)
                        packet_features.append(value)
                    
                    # Check if packet_size is None
                    if packet_features[0] is not None:
                        feature_values.append(packet_features)
                    else:
                        print(f"AttributeError: packet_size is None in packet {packet.summary()}")
                except AttributeError as e:
                    # Handle missing attributes gracefully
                    print(f"AttributeError: {e} in packet {packet.summary()}")

        # Check if there are valid feature values for analysis
        if not feature_values:
            print("No valid feature values found for correlation analysis.")
            return

        # Calculate correlation matrix
        correlation_matrix = np.corrcoef(np.array(feature_values).T)

        # Plot the correlation matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', xticklabels=features, yticklabels=features)
        plt.title('Correlation Analysis')
        plt.savefig('static/images/correlation_analysis.png')  # Save the plot as a PNG image
        plt.close()

    except Exception as e:
        print("An error occurred during correlation analysis:", str(e))



def load_packets(pcap_file):
    print("Loading packets from:", pcap_file)
    packets = rdpcap(pcap_file)
    print("Loaded", len(packets), "packets")
    return packets




# Function for main feature extraction
def main(pcap_file=None):
    # Load packets from the pcap file
    packets = load_packets(pcap_file)

    # Check if packets are loaded successfully
    if not packets:
        print("Error: Failed to load packets.")
        return None  # Return None to indicate failure

    # Perform feature extraction
    protocol_distribution_over_time(packets)
    packet_size_distribution_by_protocol(packets)
    inter_arrival_time_analysis(packets)
    flow_duration_analysis(packets)
    top_conversations(packets)
    dns_request_analysis(packets)
    http_request_analysis(packets)
    geolocation_visualization(packets)
    anomaly_detection(packets)
    bandwidth_utilization(packets)
    network_topology_visualization(packets)
    correlation_analysis(packets)

    print("Feature extraction completed.")

    # Return success indication
    return True




