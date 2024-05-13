// Initialize any type of chart with base configuration
function initChart(chartId, type, label, backgroundColor, borderColor) {
  var ctx = document.getElementById(chartId).getContext("2d");
  return new Chart(ctx, {
    type: type,
    data: {
      labels: [],
      datasets: [
        {
          label: label,
          backgroundColor: backgroundColor,
          borderColor: borderColor,
          data: [],
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        x: { display: true },
        y: { display: true, beginAtZero: true },
      },
      animation: {
        duration: 0, // Reduce animation time to improve responsiveness for live data
      },
      maintainAspectRatio: false,
    },
  });
}

// Initialize all charts
var charts = {
  protocolChart: initChart(
    "protocolChart",
    "line",
    "Protocol Usage",
    "rgba(255, 99, 132, 0.2)",
    "rgba(255, 99, 132, 1)"
  ),
  packetSizeChart: initChart(
    "packetSizeChart",
    "bar",
    "Packet Size Distribution",
    "rgba(54, 162, 235, 0.2)",
    "rgba(54, 162, 235, 1)"
  ),
  interArrivalTimeChart: initChart(
    "interArrivalTimeChart",
    "line",
    "Inter-Arrival Times",
    "rgba(75, 192, 192, 0.2)",
    "rgba(75, 192, 192, 1)"
  ),
  flowDurationChart: initChart(
    "flowDurationChart",
    "line",
    "Flow Durations",
    "rgba(153, 102, 255, 0.2)",
    "rgba(153, 102, 255, 1)"
  ),
  topConversationsChart: initChart(
    "topConversationsChart",
    "bar",
    "Top Conversations",
    "rgba(255, 159, 64, 0.2)",
    "rgba(255, 159, 64, 1)"
  ),
  dnsRequestChart: initChart(
    "dnsRequestChart",
    "bar",
    "DNS Requests",
    "rgba(255, 206, 86, 0.2)",
    "rgba(255, 206, 86, 1)"
  ),
  httpRequestChart: initChart(
    "httpRequestChart",
    "bar",
    "HTTP Methods",
    "rgba(54, 162, 235, 0.2)",
    "rgba(54, 162, 235, 1)"
  ),
  geolocationChart: initChart(
    "geolocationChart",
    "scatter",
    "Geolocations",
    "rgba(255, 99, 132, 0.2)",
    "rgba(255, 99, 132, 1)"
  ),
  anomalyDetectionChart: initChart(
    "anomalyDetectionChart",
    "line",
    "Anomalies Detected",
    "rgba(255, 99, 132, 0.2)",
    "rgba(255, 99, 132, 1)"
  ),
  bandwidthUtilizationChart: initChart(
    "bandwidthUtilizationChart",
    "line",
    "Bandwidth Utilization",
    "rgba(75, 192, 192, 0.2)",
    "rgba(75, 192, 192, 1)"
  ),
  networkTopologyChart: initChart(
    "networkTopologyChart",
    "radar",
    "Network Topology",
    "rgba(153, 102, 255, 0.2)",
    "rgba(153, 102, 255, 1)"
  ),
  correlationAnalysisChart: initChart(
    "correlationAnalysisChart",
    "line",
    "Correlation Analysis",
    "rgba(255, 159, 64, 0.2)",
    "rgba(255, 159, 64, 1)"
  ),
};

function updateChart(chart, newData) {
  if (newData) {
    // Check if new labels and data arrays are provided
    if (newData.labels && newData.data) {
      // Append new data
      chart.data.labels.push(...newData.labels);
      chart.data.datasets.forEach((dataset, index) => {
        dataset.data.push(...newData.data[index]);
      });

      // Remove old data if the chart gets too crowded
      while (chart.data.labels.length > 50) {
        // adjust 50 to your desired data window size
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
          dataset.data.shift();
        });
      }

      chart.update();
    }
  }
}

// Fetch data from server and update charts
function fetchDataAndUpdateCharts() {
  fetch("/data-feed")
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched data:", data);
      Object.entries(data).forEach(([chartName, chartData]) => {
        if (window[chartName] && chartData.data && chartData.labels) {
          updateChart(window[chartName], chartData);
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      alert(
        "An error occurred while fetching chart data. Please check the console for more details."
      );
    });
}

// Periodic data fetch and update
setInterval(fetchDataAndUpdateCharts, 1000); // Update every second
