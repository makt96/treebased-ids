import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import numpy as np
import collections
import json
import networkx as nx
import socketio

# Setup figure and axes for the subplots
fig, axs = plt.subplots(5, 2, figsize=(15, 25))  # 5x2 grid for various charts
axs = axs.flatten()  # Flatten the array of axes for easier indexing

# Titles and labels for each subplot
titles = [
    'Packet Length Distribution', 'Source Packet Frequency',
    'Destination Packet Frequency', 'Traffic Volume',
    'Protocol Distribution', 'Top Talkers',
    'Top Destinations', 'Alerts and Anomalies',
    'Summary Statistics', 'Network Topology'
]
labels = [
    ('Packet Length', 'Frequency'), ('Time', 'Frequency'),
    ('Time', 'Frequency'), ('Time', 'Traffic Volume'),
    ('Protocol', 'Count'), ('IP Address', 'Count'),
    ('IP Address', 'Count'), ('Timestamp', 'Alert Details'),
    ('Metric', 'Value'), ('Node', 'Connections')
]

# Initialize each subplot with titles and labels
for ax, title, (xlabel, ylabel) in zip(axs, titles, labels):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

# Global storage for plotting data
data_store = collections.defaultdict(list)
data_store['network_topology'] = nx.Graph()

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.on('live_data')
def on_live_data(data):
    update(data)

def update(data):
    """ Update function for FuncAnimation to refresh plots with new data. """
    # Packet Length Distribution
    packet_lengths = data_store['packet_lengths']
    packet_lengths.append(data['len'])
    if len(packet_lengths) > 100:
        packet_lengths.pop(0)
    axs[0].clear()
    sns.histplot(packet_lengths, bins=30, ax=axs[0], kde=False, color='blue')
    
    # Source Packet Frequency
    src_freqs = data_store['src_freqs']
    src_freqs.append(data['src_packet_freq'])
    if len(src_freqs) > 100:
        src_freqs.pop(0)
    axs[1].clear()
    axs[1].plot(src_freqs, color='green')
    
    # Destination Packet Frequency
    dst_freqs = data_store['dst_freqs']
    dst_freqs.append(data['dst_packet_freq'])
    if len(dst_freqs) > 100:
        dst_freqs.pop(0)
    axs[2].clear()
    axs[2].plot(dst_freqs, color='red')
    
    # Traffic Volume
    traffic_volumes = data_store['traffic_volumes']
    traffic_volumes.append(data['traffic_volume'])
    if len(traffic_volumes) > 100:
        traffic_volumes.pop(0)
    axs[3].clear()
    axs[3].plot(traffic_volumes, color='purple')
    
    # Protocol Distribution
    protocols = data_store['protocols']
    protocols.append(data['protocol'])
    protocol_counts = collections.Counter(protocols)
    axs[4].clear()
    sns.barplot(x=list(protocol_counts.keys()), y=list(protocol_counts.values()), ax=axs[4], palette='viridis')
    
    # Top Talkers
    src_ips = data_store['src_ips']
    src_ips.append(data['src_ip'])
    src_ip_counts = collections.Counter(src_ips)
    top_src_ips = src_ip_counts.most_common(10)
    axs[5].clear()
    sns.barplot(x=[ip for ip, _ in top_src_ips], y=[count for _, count in top_src_ips], ax=axs[5], palette='hot')
    
    # Top Destinations
    dst_ips = data_store['dst_ips']
    dst_ips.append(data['dst_ip'])
    dst_ip_counts = collections.Counter(dst_ips)
    top_dst_ips = dst_ip_counts.most_common(10)
    axs[6].clear()
    sns.barplot(x=[ip for ip, _ in top_dst_ips], y=[count for _, count in top_dst_ips], ax=axs[6], palette='coolwarm')
    
    # Alerts and Anomalies
    alerts = data_store['alerts']
    alerts.append((data['len'], data['src_packet_freq'], data['dst_packet_freq'], data['traffic_volume']))
    if len(alerts) > 10:
        alerts.pop(0)
    axs[7].clear()
    axs[7].table(cellText=alerts, colLabels=['Packet Length', 'Source Freq', 'Dest Freq', 'Traffic Volume'], loc='center')
    axs[7].axis('off')
    
    # Summary Statistics
    summary_stats = [
        f"Average Packet Length: {np.mean(packet_lengths):.2f}",
        f"Average Source Packet Freq: {np.mean(src_freqs):.2f}",
        f"Average Dest Packet Freq: {np.mean(dst_freqs):.2f}",
        f"Total Traffic Volume: {sum(traffic_volumes)}"
    ]
    axs[8].clear()
    axs[8].text(0.5, 0.5, "\n".join(summary_stats), horizontalalignment='center', verticalalignment='center')
    axs[8].axis('off')

    # Network Topology Visualization
    G = data_store['network_topology']
    G.add_edge(data['src_ip'], data['dst_ip'])
    axs[9].clear()
    nx.draw(G, with_labels=True, ax=axs[9])
    
    plt.tight_layout()

# Connect to the Flask server
sio.connect('http://localhost:5000')

plt.show()
