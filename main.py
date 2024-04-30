# main.py
import analyze
import features

def main(filename):
    analyze.main(filename)
    # packets = features.load_packets(filename)
    # features.protocol_distribution_over_time(packets)
    # features.packet_size_distribution_by_protocol(packets)
    # features.inter_arrival_time_analysis(packets)
    # features.flow_duration_analysis(packets)
    # features.top_conversations(packets)
    # features.dns_request_analysis(packets)
    # features.http_request_analysis(packets)
    # features.geolocation_visualization(packets)
    # features.anomaly_detection(packets)
    # features.bandwidth_utilization(packets)
    # features.network_topology_visualization(packets)
    # features.correlation_analysis(packets)
    features.main(filename)
    return [
        'static/images/protocol_distribution_over_time.png',
        # 'static/images/packet_size_distribution_by_protocol.png',
        # 'static/images/inter_arrival_time_analysis.png',
        # Add more image paths here
    ]

if __name__ == "__main__":
    main()
