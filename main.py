# import argparse
# import analyze
# import features
# import live_analysis
# import live_features

# def main(filename=None, live=False):
#     if live:
#         live_analysis.live_packet_analysis()
#         # Add live packet visualization
#         live_features.live_packet_visualization()
#     elif filename:  # Check if filename is not None
#         analyze.main(filename)
#         features.main(filename)
#         return [
#             'static/images/protocol_distribution_over_time.png',
#             # Add more image paths as needed
#         ]
#     else:
#         print("Please provide a filename or use the --live flag for live packet analysis.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run network packet analysis.")
#     parser.add_argument('--filename', type=str, help='The file path of the packet capture file for static analysis.')
#     parser.add_argument('--live', action='store_true', help='Flag to run live packet analysis instead of static.')
#     args = parser.parse_args()

#     main(filename=args.filename, live=args.live)



import argparse
import analyze
import features
import live_analysis
import live_features

# Define a global variable to store live packet results
live_results = None

def main(filename=None, live=False):
    global live_results  # Access the global variable

    if live:
        # Run live packet analysis
        live_results = live_analysis.live_packet_analysis()
        # Call live packet visualization
        live_features.live_packet_visualization(live_results)
        
    elif filename:  # Check if filename is not None
        # Perform static analysis
        analysis_results = analyze.main(filename)
        feature_results = features.main(filename)
        if analysis_results and feature_results:
            # Call visualization functions for static analysis
            visualize_static_results(analysis_results, feature_results)
    else:
        print("Please provide a filename or use the --live flag for live packet analysis.")

def visualize_static_results(analysis_results, feature_results):
    if feature_results:
        # Call visualization functions from features.py
        features.protocol_distribution_over_time(analysis_results)
        features.packet_size_distribution_by_protocol(analysis_results)
        features.inter_arrival_time_analysis(analysis_results)
        features.flow_duration_analysis(analysis_results)
        features.top_conversations(analysis_results)
        features.dns_request_analysis(analysis_results)
        features.http_request_analysis(analysis_results)
        features.geolocation_visualization(analysis_results)
        features.anomaly_detection(analysis_results)
        features.bandwidth_utilization(analysis_results)
        features.network_topology_visualization(analysis_results)
        features.correlation_analysis(analysis_results)
    else:
        print("Error: No features results found.")

# Modify the if __name__ == "__main__": block to accept live_results as a parameter
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run network packet analysis.")
    parser.add_argument('--filename', type=str, help='The file path of the packet capture file for static analysis.')
    parser.add_argument('--live', action='store_true', help='Flag to run live packet analysis instead of static.')
    args = parser.parse_args()

    main(filename=args.filename, live=args.live)
