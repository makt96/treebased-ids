# # live_analysis.py
# from scapy.all import sniff, IP
# import joblib
# import collections
# import platform

# # Load the pre-trained machine learning model
# model = joblib.load('stk_model.pkl')

# # Global variables to track packet statistics
# packet_freqs = collections.defaultdict(int)
# total_traffic_volume = 0

# def preprocess(packet):
#     global total_traffic_volume
#     packet_size = len(packet)
#     src_ip = packet[IP].src if IP in packet else ''
#     dst_ip = packet[IP].dst if IP in packet else ''
#     packet_freqs[src_ip] += 1
#     packet_freqs[dst_ip] += 1
#     total_traffic_volume += packet_size
#     return [packet_size, packet_freqs[src_ip], packet_freqs[dst_ip], total_traffic_volume]

# def process_packet(packet):
#     if IP not in packet:
#         return
#     features = preprocess(packet)
#     prediction = model.predict([features])
#     print(f"Prediction: {prediction[0]}")

# def get_available_interfaces():
#     system = platform.system()
#     if system == 'Windows':
#         from scapy.arch.windows import get_windows_if_list
#         interfaces = get_windows_if_list()
#         print("Available interfaces:", interfaces)
#         return [(interface['name'], interface['description']) for interface in interfaces]
#     else:
#         print("Interface discovery is not supported on this platform.")
#         return []

# def live_packet_analysis(interface):
#     if not interface:
#         print("No interface selected.")
#         return

#     print(f"Starting live packet analysis on interface: {interface}")
#     sniff(iface=interface, prn=process_packet, store=False, filter="ip")

# if __name__ == "__main__":
#     # Run live packet analysis
#     live_packet_analysis()


# import platform
# from scapy.all import sniff, IP
# import joblib
# import collections

# # Load the pre-trained machine learning model
# model = joblib.load('stk_model.pkl')

# # Global variables to track packet statistics
# packet_freqs = collections.defaultdict(int)
# total_traffic_volume = 0

# def preprocess(packet):
#     global total_traffic_volume
#     packet_size = len(packet)
#     src_ip = packet[IP].src if IP in packet else ''
#     dst_ip = packet[IP].dst if IP in packet else ''
#     packet_freqs[src_ip] += 1
#     packet_freqs[dst_ip] += 1
#     total_traffic_volume += packet_size
#     return [packet_size, packet_freqs[src_ip], packet_freqs[dst_ip], total_traffic_volume]

# def process_packet(packet):
#     if IP not in packet:
#         return
#     features = preprocess(packet)
#     prediction = model.predict([features])
#     print(f"Prediction: {prediction[0]}")

# def get_available_interfaces():
#     system = platform.system()
#     if system == 'Windows':
#         from scapy.arch.windows import get_windows_if_list
#         return get_windows_if_list()
#     else:
#         print("Interface discovery is not supported on this platform.")
#         return []

# def interface_selection_menu(interfaces):
#     print("Available Interfaces:")
#     for index, interface in enumerate(interfaces):
#         print(f"{index + 1}: {interface['name']} - {interface['description']}")
#     selection = int(input("Select the interface number you want to use: ")) - 1
#     if 0 <= selection < len(interfaces):
#         return interfaces[selection]['name']
#     else:
#         print("Invalid interface selection.")
#         return None

# def live_packet_analysis(interface):
#     if not interface:
#         print("No interface selected.")
#         return

#     print(f"Starting live packet analysis on interface: {interface}")
#     try:
#         sniff(iface=interface, prn=process_packet, store=False, filter="ip")
#     except Exception as e:
#         print(f"Failed to start packet sniffing on {interface}: {str(e)}")

# if __name__ == "__main__":
#     interfaces = get_available_interfaces()
#     if interfaces:
#         selected_interface = interface_selection_menu(interfaces)
#         if selected_interface:
#             live_packet_analysis(selected_interface)
#     else:
#         print("No interfaces available for selection.")



import subprocess
import platform
from scapy.all import sniff, IP
import joblib
import collections

# Load the pre-trained machine learning model
model = joblib.load('stk_model.pkl')

# Global variables to track packet statistics
packet_freqs = collections.defaultdict(int)
total_traffic_volume = 0

def preprocess(packet):
    global total_traffic_volume
    packet_size = len(packet)
    src_ip = packet[IP].src if IP in packet else ''
    dst_ip = packet[IP].dst if IP in packet else ''
    packet_freqs[src_ip] += 1
    packet_freqs[dst_ip] += 1
    total_traffic_volume += packet_size
    print("Now Live Packets are preprocessed and going to process_packet function...")
    return [packet_size, packet_freqs[src_ip], packet_freqs[dst_ip], total_traffic_volume]

def process_packet(packet):
    if IP not in packet:
        return
    features = preprocess(packet)
    print("Prediction is now starting...")
    prediction = model.predict([features])
    print(f"Prediction: {prediction[0]}")

def get_available_interfaces():
    system = platform.system()
    if system == 'Windows':
        # Execute PowerShell command to get network adapter information
        cmd = 'powershell "Get-NetAdapter | Select Name, Status, LinkSpeed, MacAddress"'
        output = subprocess.check_output(cmd, shell=True, text=True)
        # Parse the output to extract interface information
        interfaces = []
        for line in output.strip().split('\n'):
            fields = line.strip().split()
            interface = {
                'name': fields[0],
                'status': fields[1],
                'link_speed': fields[2],
                'mac_address': fields[3]
            }
            interfaces.append(interface)
        return interfaces
    else:
        print("Interface discovery is not supported on this platform.")
        return []

# def interface_selection_menu(interfaces):
#     print("Available Interfaces:")
#     for index, interface in enumerate(interfaces):
#         print(f"{index + 1}: {interface['name']} - {interface['status']} - {interface['link_speed']} - {interface['mac_address']}")
#     selection = int(input("Select the interface number you want to use: ")) - 1
#     if 0 <= selection < len(interfaces):
#         return interfaces[selection]['name']
#     else:
#         print("Invalid interface selection.")
#         return None

def interface_selection_menu(interfaces):
    print("Available Interfaces:")
    for index, interface in enumerate(interfaces):
        print(f"{index + 1}: {interface['name']} - {interface['status']} - {interface['link_speed']} - {interface['mac_address']}")
    selection = int(input("Select the interface number you want to use: ")) - 1
    if 0 <= selection < len(interfaces):
        return interfaces[selection]['name']  # Return only the interface name
    else:
        print("Invalid interface selection.")
        return None


# def live_packet_analysis(interface):
#     if not interface:
#         print("No interface selected.")
#         return

#     print(f"Starting live packet analysis on interface: {interface}")
#     try:
#         sniff(iface=interface, prn=process_packet, store=False, filter="ip")
#     except Exception as e:
#         print(f"Failed to start packet sniffing on {interface}: {str(e)}")

# def live_packet_analysis(interface):
#     if not interface:
#         print("No interface selected.")
#         return

#     print(f"Starting live packet analysis on interface: {interface}")
#     live_results = []

#     try:
#         # sniff(iface=interface, prn=process_packet, store=False, filter="ip")
#         sniff(iface=interface, prn=lambda pkt: live_results.append(process_packet(pkt)), store=False, filter="ip")
#     except Exception as e:
#         print(f"Failed to start packet sniffing on {interface}: {str(e)}")
#     print("Here is Live Data that has to be sent to main.py and then app.py (data-feed function) -> live.html: ", live_results)
#     return live_results


def live_packet_analysis(interface):
    if not interface:
        print("No interface selected.")
        return []

    print(f"Starting live packet analysis on interface: {interface}")
    live_results = []

    try:
        # Define a callback function to process each packet and append the result to live_results
        def packet_callback(packet):
            result = process_packet(packet)
            live_results.append(result)

        # Print the selected interface for verification
        print("Selected Interface:", interface)

        # Call sniff with the packet_callback function
        sniff(iface=interface, prn=packet_callback, store=False, filter="ip")
    except Exception as e:
        print(f"Failed to start packet sniffing on {interface}: {str(e)}")
    
    print("Live Packet Analysis Complete. Live Results:", live_results)
    return live_results




if __name__ == "__main__":
    interfaces = get_available_interfaces()
    if interfaces:
        selected_interface = interface_selection_menu(interfaces)
        if selected_interface:
            live_packet_analysis(selected_interface)
    else:
        print("No interfaces available for selection.")
