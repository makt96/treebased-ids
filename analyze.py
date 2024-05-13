# import features
# import joblib
# import collections
# import sys

# # Load the pre-trained machine learning model
# model = joblib.load('stk_model.pkl')

# def preprocess(packet_data):
#     # Ensure all features needed for prediction are present
#     processed_features = [
#         packet_data['packet_size'],
#         packet_data['src_packet_freq'],
#         packet_data['dst_packet_freq'],
#         packet_data['traffic_volume']
#     ]
#     print(f"Preprocessed features: {processed_features}")  # Debugging statement
#     return processed_features

# def make_prediction(packets):
#     predictions = []
#     packet_freqs = collections.defaultdict(int)
#     total_traffic = 0

#     for packet in packets:
#         try:
#             packet_size = len(packet)
#             src_ip = packet.get('IP', {}).get('src', '')
#             dst_ip = packet.get('IP', {}).get('dst', '')
#             packet_freqs[src_ip] += 1
#             packet_freqs[dst_ip] += 1
#             total_traffic += packet_size

#             packet_data = {
#                 "packet_size": packet_size,
#                 "src_packet_freq": packet_freqs[src_ip],
#                 "dst_packet_freq": packet_freqs[dst_ip],
#                 "traffic_volume": total_traffic
#             }

#             features_for_model = preprocess(packet_data)
#             prediction = model.predict([features_for_model])
#             predictions.append(prediction[0])
#             print(f"Prediction for IP {src_ip} to {dst_ip}: {prediction[0]}")  # Debugging statement
#         except Exception as e:
#             print(f"Error processing packet: {e}")

#     return predictions

# def main(pcap_file):
#     print("Analyzing traffic from:", pcap_file)
#     try:
#         packets = features.load_packets(pcap_file)
#         print("Starting traffic analysis...")
#         predictions = make_prediction(packets)
#         print("Predictions:", predictions)
#         print("Traffic analysis complete")
#     except Exception as e:
#         print(f"An error occurred during analysis: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python analyze.py <pcap_file>")
#         sys.exit(1)
    
#     pcap_file = sys.argv[1]
#     main(pcap_file)


import features
import joblib
import collections
import sys
import logging
from scapy.all import rdpcap, IP, TCP, UDP

# Setup basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the pre-trained machine learning model
model = joblib.load('stk_model.pkl')

def preprocess(packet_data):
    # Ensure all features needed for prediction are present
    processed_features = [
        packet_data['packet_size'],
        packet_data['src_packet_freq'],
        packet_data['dst_packet_freq'],
        packet_data['traffic_volume']
    ]
    logging.debug(f"Preprocessed features: {processed_features}")
    return processed_features

def make_prediction(packets):
    predictions = []
    packet_freqs = collections.defaultdict(int)
    total_traffic = 0

    for packet in packets:
        if IP in packet:
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            packet_size = len(packet)
            packet_freqs[src_ip] += 1
            packet_freqs[dst_ip] += 1
            total_traffic += packet_size

            packet_data = {
                "packet_size": packet_size,
                "src_packet_freq": packet_freqs[src_ip],
                "dst_packet_freq": packet_freqs[dst_ip],
                "traffic_volume": total_traffic
            }

            features_for_model = preprocess(packet_data)
            prediction = model.predict([features_for_model])
            predictions.append(prediction[0])
        else:
            logging.error("Packet does not contain an IP layer.")

    return predictions

def main(pcap_file):
    logging.info(f"Analyzing traffic from: {pcap_file}")
    try:
        packets = rdpcap(pcap_file)
        logging.info("Starting traffic analysis...")
        predictions = make_prediction(packets)
        logging.info(f"Predictions: {predictions}")
        logging.info("Traffic analysis complete")
    except Exception as e:
        logging.error(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python analyze.py <pcap_file>")
        sys.exit(1)
    
    pcap_file = sys.argv[1]
    main(pcap_file)
