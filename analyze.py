import features
import joblib
import collections

# Load the pre-trained machine learning model
model = joblib.load('stk_model.pkl')

# Function to preprocess packet data for model input
def preprocess(packet_data):
    processed_features = [
        packet_data['packet_size'],
        packet_data['src_packet_freq'],
        packet_data['dst_packet_freq'],
        packet_data['traffic_volume']
    ]
    return processed_features

# Function to make prediction using the model
def make_prediction(packets):
    predictions = []
    packet_freqs = collections.defaultdict(int)
    total_traffic_volume = 0

    for packet in packets:
        packet_size = len(packet)
        src_ip = packet['IP'].src if 'IP' in packet else ''
        dst_ip = packet['IP'].dst if 'IP' in packet else ''
        packet_freqs[src_ip] += 1
        packet_freqs[dst_ip] += 1
        total_traffic_volume += packet_size

        packet_data = {
            "packet_size": packet_size,
            "src_packet_freq": packet_freqs[src_ip],
            "dst_packet_freq": packet_freqs[dst_ip],
            "traffic_volume": total_traffic_volume
        }
        
        # Preprocess features for model input
        features_for_model = preprocess(packet_data)
        
        # Make prediction using the model
        prediction = model.predict([features_for_model])
        predictions.append(prediction)

    return predictions

# Main function
def main(pcap_file):
    print("Analyzing traffic from:", pcap_file)
    packets = features.load_packets(pcap_file)

    print("Starting traffic analysis...")
    predictions = make_prediction(packets)
    
    # Print or visualize predictions as needed
    print("Predictions:", predictions)
    print("Traffic analysis complete")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <pcap_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    main(pcap_file)
