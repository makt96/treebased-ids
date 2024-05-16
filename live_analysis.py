import subprocess
import json
import time
import joblib
import random

# Load the pre-trained machine learning model
model = joblib.load('stk_model.pkl')

# Global storage for packet frequency counts and total traffic
packet_freqs = {}
total_traffic = 0
live_results = []

def preprocess(packet_data):
    """ Prepare packet data for model prediction based on features similar to static analysis. """
    processed_features = [
        packet_data['len'],
        packet_data['src_packet_freq'],
        packet_data['dst_packet_freq'],
        packet_data['traffic_volume']
    ]
    print(f"Preprocessed features: {processed_features}")  # Debugging statement
    return processed_features

def process_packet(packet_json):
    """Process each packet captured by tshark, ignoring packets without necessary data."""
    try:
        packet_data = json.loads(packet_json)
        # Ensure all required fields are present
        if 'layers' in packet_data and all(k in packet_data['layers'] for k in ['ip_src', 'ip_dst', 'ip_len']):
            src_ip = packet_data['layers']['ip_src'][0]
            dst_ip = packet_data['layers']['ip_dst'][0]
            packet_len = int(packet_data['layers']['ip_len'][0])

            # Accumulate frequency and total traffic as done in static analysis
            global packet_freqs, total_traffic
            packet_freqs[src_ip] = packet_freqs.get(src_ip, 0) + 1
            packet_freqs[dst_ip] = packet_freqs.get(dst_ip, 0) + 1
            total_traffic += packet_len

            packet_info = {
                "len": packet_len,
                "src_packet_freq": packet_freqs[src_ip],
                "dst_packet_freq": packet_freqs[dst_ip],
                "traffic_volume": total_traffic
            }

            features = preprocess(packet_info)
            prediction = model.predict([features])
            
            live_results.append({
                "IP": {
                    "src": src_ip,
                    "dst": dst_ip,
                    "len": packet_len,
                    "prediction": prediction[0]
                },
                "time": time.time()
            })

            # Limit the size of live_results
            if len(live_results) > 100:
                live_results.pop(0)

            print(f"Processed packet: {packet_info}, Prediction: {prediction[0]}")
        else:
            print("Packet skipped due to incomplete data")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {str(e)}")
    except Exception as e:
        print(f"Error processing packet: {str(e)}")


def start_tshark(interface):
    """ Start the tshark process to capture packets using provided interface. """
    command = ['tshark', '-i', interface, '-T', 'ek', '-e', 'ip.src', '-e', 'ip.dst', '-e', 'ip.len', '-Y', 'ip', '-l']
    print(f"Starting tshark with command: {' '.join(command)}")  # Debugging statement
    with subprocess.Popen(command, stdout=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            process_packet(line.strip())

def get_live_results():
    """ Return a copy of the live results. """
    print(f"Returning live results: {live_results}")  # Debugging statement
    #return live_results.copy()
    example_data = {
        'len': random.randint(40, 1500),
        'src_packet_freq': random.randint(1, 1000),
        'dst_packet_freq': random.randint(1, 1000),
        'traffic_volume': random.randint(1, 1000000)
    }
    return example_data

if __name__ == "__main__":
    interface = "\\Device\\NPF_{3958AAE7-B2D7-4302-9F76-EA8AD698D618}"
    start_tshark(interface)
