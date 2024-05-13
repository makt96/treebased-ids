// // Initialize any type of chart with base configuration
// function initChart(chartId, type, label, backgroundColor, borderColor) {
//   var ctx = document.getElementById(chartId).getContext("2d");
//   return new Chart(ctx, {
//     type: type,
//     data: {
//       labels: [],
//       datasets: [
//         {
//           label: label,
//           backgroundColor: backgroundColor,
//           borderColor: borderColor,
//           data: [],
//           fill: false,
//         },
//       ],
//     },
//     options: {
//       scales: {
//         x: { display: true },
//         y: { display: true, beginAtZero: true },
//       },
//       animation: {
//         duration: 0, // Reduce animation time to improve responsiveness for live data
//       },
//       maintainAspectRatio: false,
//     },
//   });
// }

// // Initialize all charts
// var charts = {
//   protocolChart: initChart(
//     "protocolChart",
//     "line",
//     "Protocol Usage",
//     "rgba(255, 99, 132, 0.2)",
//     "rgba(255, 99, 132, 1)"
//   ),
//   packetSizeChart: initChart(
//     "packetSizeChart",
//     "bar",
//     "Packet Size Distribution",
//     "rgba(54, 162, 235, 0.2)",
//     "rgba(54, 162, 235, 1)"
//   ),
//   interArrivalTimeChart: initChart(
//     "interArrivalTimeChart",
//     "line",
//     "Inter-Arrival Times",
//     "rgba(75, 192, 192, 0.2)",
//     "rgba(75, 192, 192, 1)"
//   ),
//   flowDurationChart: initChart(
//     "flowDurationChart",
//     "line",
//     "Flow Durations",
//     "rgba(153, 102, 255, 0.2)",
//     "rgba(153, 102, 255, 1)"
//   ),
//   topConversationsChart: initChart(
//     "topConversationsChart",
//     "bar",
//     "Top Conversations",
//     "rgba(255, 159, 64, 0.2)",
//     "rgba(255, 159, 64, 1)"
//   ),
//   dnsRequestChart: initChart(
//     "dnsRequestChart",
//     "bar",
//     "DNS Requests",
//     "rgba(255, 206, 86, 0.2)",
//     "rgba(255, 206, 86, 1)"
//   ),
//   httpRequestChart: initChart(
//     "httpRequestChart",
//     "bar",
//     "HTTP Methods",
//     "rgba(54, 162, 235, 0.2)",
//     "rgba(54, 162, 235, 1)"
//   ),
//   geolocationChart: initChart(
//     "geolocationChart",
//     "scatter",
//     "Geolocations",
//     "rgba(255, 99, 132, 0.2)",
//     "rgba(255, 99, 132, 1)"
//   ),
//   anomalyDetectionChart: initChart(
//     "anomalyDetectionChart",
//     "line",
//     "Anomalies Detected",
//     "rgba(255, 99, 132, 0.2)",
//     "rgba(255, 99, 132, 1)"
//   ),
//   bandwidthUtilizationChart: initChart(
//     "bandwidthUtilizationChart",
//     "line",
//     "Bandwidth Utilization",
//     "rgba(75, 192, 192, 0.2)",
//     "rgba(75, 192, 192, 1)"
//   ),
//   networkTopologyChart: initChart(
//     "networkTopologyChart",
//     "radar",
//     "Network Topology",
//     "rgba(153, 102, 255, 0.2)",
//     "rgba(153, 102, 255, 1)"
//   ),
//   correlationAnalysisChart: initChart(
//     "correlationAnalysisChart",
//     "line",
//     "Correlation Analysis",
//     "rgba(255, 159, 64, 0.2)",
//     "rgba(255, 159, 64, 1)"
//   ),
// };

// function updateChart(chart, newData) {
//   if (newData) {
//     // Check if new labels and data arrays are provided
//     if (newData.labels && newData.data) {
//       // Append new data
//       chart.data.labels.push(...newData.labels);
//       chart.data.datasets.forEach((dataset, index) => {
//         dataset.data.push(...newData.data[index]);
//       });

//       // Remove old data if the chart gets too crowded
//       while (chart.data.labels.length > 50) {
//         // adjust 50 to your desired data window size
//         chart.data.labels.shift();
//         chart.data.datasets.forEach((dataset) => {
//           dataset.data.shift();
//         });
//       }

//       chart.update();
//     }
//   }
// }

// // Fetch data from server and update charts
// function fetchDataAndUpdateCharts() {
//   fetch("/data-feed")
//     .then((response) => response.json())
//     .then((data) => {
//       console.log("Fetched data:", data);
//       Object.entries(data).forEach(([chartName, chartData]) => {
//         if (window[chartName] && chartData.data && chartData.labels) {
//           updateChart(window[chartName], chartData);
//         }
//       });
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//       alert(
//         "An error occurred while fetching chart data. Please check the console for more details."
//       );
//     });
// }

// // Periodic data fetch and update
// setInterval(fetchDataAndUpdateCharts, 1000); // Update every second
document.addEventListener("DOMContentLoaded", function () {
  const ctx = {
    protocolDistribution: document
      .getElementById("protocolChart")
      .getContext("2d"),
    packetSizeDistribution: document
      .getElementById("packetSizeChart")
      .getContext("2d"),
    interArrivalTime: document
      .getElementById("interArrivalTimeChart")
      .getContext("2d"),
    flowDuration: document.getElementById("flowDurationChart").getContext("2d"),
    topConversations: document
      .getElementById("topConversationsChart")
      .getContext("2d"),
    dnsRequestAnalysis: document
      .getElementById("dnsRequestChart")
      .getContext("2d"),
    httpRequestAnalysis: document
      .getElementById("httpRequestChart")
      .getContext("2d"),
    geolocationVisualization: document
      .getElementById("geolocationChart")
      .getContext("2d"),
    anomalyDetection: document
      .getElementById("anomalyDetectionChart")
      .getContext("2d"),
    bandwidthUtilization: document
      .getElementById("bandwidthUtilizationChart")
      .getContext("2d"),
    networkTopologyVisualization: document
      .getElementById("networkTopologyChart")
      .getContext("2d"),
  };

  const charts = {
    protocolDistribution: new Chart(ctx.protocolDistribution, {
      type: "bar",
      data: {
        labels: [],
        datasets: [
          {
            label: "Protocol Usage",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    packetSizeDistribution: new Chart(ctx.packetSizeDistribution, {
      type: "bar",
      data: {
        labels: [],
        datasets: [
          {
            label: "Packet Size",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    interArrivalTime: new Chart(ctx.interArrivalTime, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Inter-Arrival Time",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    flowDuration: new Chart(ctx.flowDuration, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Flow Duration",
            backgroundColor: "rgba(153, 102, 255, 0.2)",
            borderColor: "rgba(153, 102, 255, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    topConversations: new Chart(ctx.topConversations, {
      type: "bar",
      data: {
        labels: [],
        datasets: [
          {
            label: "Top Conversations",
            backgroundColor: "rgba(255, 159, 64, 0.2)",
            borderColor: "rgba(255, 159, 64, 1)",
            data: [],
          },
        ],
      },
      options: { indexAxis: "y", scales: { x: { beginAtZero: true } } }, // Change to horizontal bar
    }),
    dnsRequestAnalysis: new Chart(ctx.dnsRequestAnalysis, {
      type: "bar",
      data: {
        labels: [],
        datasets: [
          {
            label: "DNS Requests",
            backgroundColor: "rgba(255, 206, 86, 0.2)",
            borderColor: "rgba(255, 206, 86, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    httpRequestAnalysis: new Chart(ctx.httpRequestAnalysis, {
      type: "bar",
      data: {
        labels: [],
        datasets: [
          {
            label: "HTTP Methods",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    geolocationVisualization: new Chart(ctx.geolocationVisualization, {
      type: "scatter",
      data: {
        datasets: [
          {
            label: "Geolocations",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    anomalyDetection: new Chart(ctx.anomalyDetection, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Anomalies Detected",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    bandwidthUtilization: new Chart(ctx.bandwidthUtilization, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Bandwidth Utilization",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
    networkTopologyVisualization: new Chart(ctx.networkTopologyVisualization, {
      type: "radar",
      data: {
        labels: [],
        datasets: [
          {
            label: "Network Topology",
            backgroundColor: "rgba(153, 102, 255, 0.2)",
            borderColor: "rgba(153, 102, 255, 1)",
            data: [],
          },
        ],
      },
      options: { scales: { y: { beginAtZero: true } } },
    }),
  };

  function fetchData() {
    fetch("/data-feed")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Assuming data is an object where keys match chart names
        Object.keys(charts).forEach((chartName) => {
          if (data && data[chartName]) {
            // Ensure data and data[chartName] are valid
            const chart = charts[chartName];
            if (data[chartName].labels && data[chartName].data) {
              chart.data.labels.push(...data[chartName].labels);
              chart.data.datasets.forEach((dataset, index) => {
                dataset.data.push(...data[chartName].data[index]);
              });
              chart.update();
            }
          }
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        // Optionally update the UI to indicate an error fetching data
      });
  }

  // Update charts every second
  setInterval(fetchData, 1000);
});
