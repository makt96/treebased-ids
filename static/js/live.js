var socket = io();

// Create charts for different visualizations
var protocolChart = createBarChart("protocolChart", "Protocol Distribution");
var packetSizeChart = createLineChart(
  "packetSizeChart",
  "Packet Size Distribution"
);
var interArrivalTimeChart = createLineChart(
  "interArrivalTimeChart",
  "Inter-arrival Time Analysis"
);
var flowDurationChart = createLineChart(
  "flowDurationChart",
  "Flow Duration Analysis"
);
var topConversationsChart = createBarChart(
  "topConversationsChart",
  "Top Conversations"
);
var dnsRequestChart = createBarChart("dnsRequestChart", "DNS Request Analysis");
var httpRequestChart = createBarChart(
  "httpRequestChart",
  "HTTP Request Analysis"
);
var geolocationChart = createScatterChart(
  "geolocationChart",
  "Geolocation Visualization"
);
var anomalyDetectionChart = createLineChart(
  "anomalyDetectionChart",
  "Anomaly Detection"
);
var bandwidthUtilizationChart = createLineChart(
  "bandwidthUtilizationChart",
  "Bandwidth Utilization"
);
var networkTopologyChart = createLineChart(
  "networkTopologyChart",
  "Network Topology Visualization"
); // Placeholder for topology visualization
var correlationAnalysisChart = createLineChart(
  "correlationAnalysisChart",
  "Correlation Analysis"
); // Placeholder for correlation analysis

socket.on("connect", function () {
  console.log("Connected to server");
});

socket.on("disconnect", function () {
  console.log("Disconnected from server");
});

socket.on("live_data", function (data) {
  console.log(data); // For debugging purposes
  updateBarChart(protocolChart, data.src_packet_freq);
  updateLineChart(packetSizeChart, data.len);
  updateLineChart(interArrivalTimeChart, data.traffic_volume);
  updateLineChart(flowDurationChart, data.traffic_volume);
  updateBarChart(topConversationsChart, data.src_packet_freq);
  updateBarChart(dnsRequestChart, data.traffic_volume);
  updateBarChart(httpRequestChart, data.traffic_volume);
  updateScatterChart(geolocationChart, data.traffic_volume);
  updateLineChart(anomalyDetectionChart, data.traffic_volume);
  updateLineChart(bandwidthUtilizationChart, data.traffic_volume);
  // Additional logic for networkTopologyChart and correlationAnalysisChart if needed
});

function createBarChart(elementId, label) {
  var ctx = document.getElementById(elementId).getContext("2d");
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: [],
      datasets: [
        {
          label: label,
          data: [],
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        x: { beginAtZero: true },
        y: { beginAtZero: true },
      },
    },
  });
}

function createLineChart(elementId, label) {
  var ctx = document.getElementById(elementId).getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: label,
          data: [],
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        x: { type: "time", time: { unit: "second" } },
        y: { beginAtZero: true },
      },
    },
  });
}

function createScatterChart(elementId, label) {
  var ctx = document.getElementById(elementId).getContext("2d");
  return new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [
        {
          label: label,
          data: [],
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        x: { beginAtZero: true },
        y: { beginAtZero: true },
      },
    },
  });
}

function updateBarChart(chart, value) {
  var now = new Date().toLocaleTimeString();
  chart.data.labels.push(now);
  chart.data.datasets[0].data.push(value);
  if (chart.data.labels.length > 50) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update();
}

function updateLineChart(chart, value) {
  var now = new Date();
  chart.data.labels.push(now);
  chart.data.datasets[0].data.push({ x: now, y: value });
  if (chart.data.labels.length > 50) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update();
}

function updateScatterChart(chart, value) {
  var now = new Date();
  chart.data.datasets[0].data.push({ x: now, y: value });
  if (chart.data.datasets[0].data.length > 50) {
    chart.data.datasets[0].data.shift();
  }
  chart.update();
}
