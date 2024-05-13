import argparse
import logging
import analyze
import features
import live_analysis
import live_features

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(filename=None, live=False):
    """ Main function to handle both live and static packet analysis """
    try:
        if live:
            # Perform live packet analysis
            live_results = live_analysis.live_packet_analysis()
            return live_features.live_packet_visualization(live_results)
        elif filename:
            # Perform static analysis using the provided pcap file
            analysis_results = analyze.main(filename)
            feature_results = features.main(filename)
            if analysis_results and feature_results:
                return visualize_static_results(analysis_results, feature_results)
            else:
                logging.error("Failed to obtain valid results from analysis or feature extraction.")
                return {"error": "Analysis or feature extraction failed"}
        else:
            logging.error("No valid input provided. Please provide a filename or use --live for live analysis.")
            return {"error": "No valid input provided"}
    except Exception as e:
        logging.exception("An error occurred during processing: {}".format(str(e)))
        return {"error": str(e)}

def visualize_static_results(analysis_results, feature_results):
    """ Function to visualize static results from packet analysis """
    try:
        # Assume these functions are from features.py and they return visualization data or success indicators
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
        return {"success": "Visualizations created successfully"}
    except Exception as e:
        logging.exception("Error in visualizing static results: {}".format(str(e)))
        return {"error": "Error visualizing results"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run network packet analysis.")
    parser.add_argument('--filename', type=str, help='The file path of the packet capture file for static analysis.')
    parser.add_argument('--live', action='store_true', help='Flag to run live packet analysis instead of static.')
    args = parser.parse_args()

    result = main(filename=args.filename, live=args.live)
    if 'error' in result:
        logging.error(result['error'])
    else:
        logging.info("Operation completed successfully.")
