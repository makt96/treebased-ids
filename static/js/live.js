const socket = io();

const charts = {};
const gaugeCharts = {}; // Store gauge charts here

function createLineChart(ctx, label, borderColor) {
  console.log(`Initializing chart: ${label}`);
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: label,
          data: [],
          borderColor: borderColor,
          borderWidth: 1,
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        xAxes: [
          {
            type: "time",
            time: {
              unit: "minute",
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });
}

function createPieChart(ctx, labels, backgroundColor) {
  console.log(`Initializing chart: Protocol Distribution`);
  return new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          data: [0, 0, 0],
          backgroundColor: backgroundColor,
        },
      ],
    },
  });
}

function createBarChart(ctx, label, backgroundColor) {
  console.log(`Initializing chart: ${label}`);
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: [],
      datasets: [
        {
          label: label,
          data: [],
          backgroundColor: backgroundColor,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });
}

function createGaugeChart(ctx, value, target) {
  return new Chart(ctx, {
    type: "doughnut",
    data: {
      datasets: [
        {
          value: value,
          data: [value, target - value],
          backgroundColor: ["#ffab00", "#00e676"],
        },
      ],
    },
    options: {
      circumference: Math.PI,
      rotation: Math.PI,
      cutoutPercentage: 80,
      responsive: true,
      tooltips: {
        enabled: false,
      },
      plugins: {
        datalabels: {
          display: true,
          formatter: (value, context) => {
            return context.chart.data.datasets[0].value + "%";
          },
          color: "black",
          backgroundColor: null,
          borderWidth: 0,
        },
      },
      needle: {
        radiusPercentage: 2,
        widthPercentage: 3.2,
        lengthPercentage: 80,
        color: "rgba(0, 0, 0, 1)",
      },
      valueLabel: {
        display: true,
        formatter: (value) => {
          return Math.round(value) + "%";
        },
      },
    },
  });
}

charts.packetLengthChart = createLineChart(
  document.getElementById("packetLengthChart").getContext("2d"),
  "Packet Length",
  "blue"
);
charts.sourcePacketFreqChart = createLineChart(
  document.getElementById("sourcePacketFreqChart").getContext("2d"),
  "Source Packet Frequency",
  "green"
);
charts.destinationPacketFreqChart = createLineChart(
  document.getElementById("destinationPacketFreqChart").getContext("2d"),
  "Destination Packet Frequency",
  "red"
);
charts.trafficVolumeChart = createLineChart(
  document.getElementById("trafficVolumeChart").getContext("2d"),
  "Traffic Volume",
  "purple"
);
charts.protocolDistributionChart = createPieChart(
  document.getElementById("protocolDistributionChart").getContext("2d"),
  ["TCP", "UDP", "ICMP"],
  ["red", "blue", "green"]
);
charts.topTalkersChart = createBarChart(
  document.getElementById("topTalkersChart").getContext("2d"),
  "Top Talkers",
  "orange"
);
charts.topDestinationsChart = createBarChart(
  document.getElementById("topDestinationsChart").getContext("2d"),
  "Top Destinations",
  "pink"
);

// Create the gauge charts only once
gaugeCharts.avgPacketLengthGauge = createGaugeChart(
  document.getElementById("avgPacketLengthGauge").getContext("2d"),
  0,
  100 // Using percentage values
);
gaugeCharts.avgSourcePacketFreqGauge = createGaugeChart(
  document.getElementById("avgSourcePacketFreqGauge").getContext("2d"),
  0,
  100 // Using percentage values
);
gaugeCharts.avgDestPacketFreqGauge = createGaugeChart(
  document.getElementById("avgDestPacketFreqGauge").getContext("2d"),
  0,
  100 // Using percentage values
);
gaugeCharts.totalTrafficVolumeGauge = createGaugeChart(
  document.getElementById("totalTrafficVolumeGauge").getContext("2d"),
  0,
  100 // Using percentage values
);

socket.on("connect", () => {
  console.log("Connected to server");
  requestNotificationPermission();
});

socket.on("disconnect", () => {
  console.log("Disconnected from server");
});

socket.on("live_data", (data) => {
  console.log("Received live data:", data);
  updateCharts(data);
  checkForSuspiciousActivity(data); // Check for suspicious activity
});

function updateCharts(data) {
  const timestamp = new Date().toLocaleTimeString();

  // Packet Length Distribution
  if (charts.packetLengthChart.data.labels.length > 100) {
    charts.packetLengthChart.data.labels.shift();
    charts.packetLengthChart.data.datasets[0].data.shift();
  }
  charts.packetLengthChart.data.labels.push(timestamp);
  charts.packetLengthChart.data.datasets[0].data.push(data.len);
  charts.packetLengthChart.update();
  console.log("Updated Packet Length Chart");

  // Source Packet Frequency
  if (charts.sourcePacketFreqChart.data.labels.length > 100) {
    charts.sourcePacketFreqChart.data.labels.shift();
    charts.sourcePacketFreqChart.data.datasets[0].data.shift();
  }
  charts.sourcePacketFreqChart.data.labels.push(timestamp);
  charts.sourcePacketFreqChart.data.datasets[0].data.push(data.src_packet_freq);
  charts.sourcePacketFreqChart.update();
  console.log("Updated Source Packet Frequency Chart");

  // Destination Packet Frequency
  if (charts.destinationPacketFreqChart.data.labels.length > 100) {
    charts.destinationPacketFreqChart.data.labels.shift();
    charts.destinationPacketFreqChart.data.datasets[0].data.shift();
  }
  charts.destinationPacketFreqChart.data.labels.push(timestamp);
  charts.destinationPacketFreqChart.data.datasets[0].data.push(
    data.dst_packet_freq
  );
  charts.destinationPacketFreqChart.update();
  console.log("Updated Destination Packet Frequency Chart");

  // Traffic Volume
  if (charts.trafficVolumeChart.data.labels.length > 100) {
    charts.trafficVolumeChart.data.labels.shift();
    charts.trafficVolumeChart.data.datasets[0].data.shift();
  }
  charts.trafficVolumeChart.data.labels.push(timestamp);
  charts.trafficVolumeChart.data.datasets[0].data.push(data.traffic_volume);
  charts.trafficVolumeChart.update();
  console.log("Updated Traffic Volume Chart");

  // Protocol Distribution
  if (data.protocol === "TCP") {
    charts.protocolDistributionChart.data.datasets[0].data[0] += 1;
  } else if (data.protocol === "UDP") {
    charts.protocolDistributionChart.data.datasets[0].data[1] += 1;
  } else if (data.protocol === "ICMP") {
    charts.protocolDistributionChart.data.datasets[0].data[2] += 1;
  }
  charts.protocolDistributionChart.update();
  console.log("Updated Protocol Distribution Chart");

  // Top Talkers
  const topTalkers = charts.topTalkersChart.data;
  const srcIndex = topTalkers.labels.indexOf(data.src_ip);
  if (srcIndex === -1) {
    topTalkers.labels.push(data.src_ip);
    topTalkers.datasets[0].data.push(1);
  } else {
    topTalkers.datasets[0].data[srcIndex] += 1;
  }
  charts.topTalkersChart.update();
  console.log("Updated Top Talkers Chart");

  // Top Destinations
  const topDestinations = charts.topDestinationsChart.data;
  const dstIndex = topDestinations.labels.indexOf(data.dst_ip);
  if (dstIndex === -1) {
    topDestinations.labels.push(data.dst_ip);
    topDestinations.datasets[0].data.push(1);
  } else {
    topDestinations.datasets[0].data[dstIndex] += 1;
  }
  charts.topDestinationsChart.update();
  console.log("Updated Top Destinations Chart");

  // Alerts and Anomalies
  const alertsTableBody = document.querySelector("#alertsTable tbody");
  const alertRow = `
    <tr>
      <td>${timestamp}</td>
      <td>
        <strong>Packet Length:</strong> ${data.len}, 
        <strong>Source IP:</strong> ${data.src_ip}, 
        <strong>Source Packet Freq:</strong> ${data.src_packet_freq}, 
        <strong>Destination IP:</strong> ${data.dst_ip}, 
        <strong>Dest Packet Freq:</strong> ${data.dst_packet_freq}, 
        <strong>Traffic Volume:</strong> ${data.traffic_volume},
        <strong>Protocol:</strong> ${data.protocol}
      </td>
    </tr>`;
  alertsTableBody.innerHTML += alertRow;

  // Summary Statistics
  const avgPacketLength = (
    charts.packetLengthChart.data.datasets[0].data.reduce((a, b) => a + b, 0) /
    charts.packetLengthChart.data.datasets[0].data.length
  ).toFixed(2);
  const avgSourcePacketFreq = (
    charts.sourcePacketFreqChart.data.datasets[0].data.reduce(
      (a, b) => a + b,
      0
    ) / charts.sourcePacketFreqChart.data.datasets[0].data.length
  ).toFixed(2);
  const avgDestPacketFreq = (
    charts.destinationPacketFreqChart.data.datasets[0].data.reduce(
      (a, b) => a + b,
      0
    ) / charts.destinationPacketFreqChart.data.datasets[0].data.length
  ).toFixed(2);
  const totalTrafficVolume =
    charts.trafficVolumeChart.data.datasets[0].data.reduce((a, b) => a + b, 0);

  // Update gauges
  gaugeCharts.avgPacketLengthGauge.data.datasets[0].data[0] =
    (avgPacketLength / 1500) * 100;
  gaugeCharts.avgPacketLengthGauge.data.datasets[0].data[1] =
    100 - gaugeCharts.avgPacketLengthGauge.data.datasets[0].data[0];
  gaugeCharts.avgPacketLengthGauge.update();

  gaugeCharts.avgSourcePacketFreqGauge.data.datasets[0].data[0] =
    (avgSourcePacketFreq / 1000) * 100;
  gaugeCharts.avgSourcePacketFreqGauge.data.datasets[0].data[1] =
    100 - gaugeCharts.avgSourcePacketFreqGauge.data.datasets[0].data[0];
  gaugeCharts.avgSourcePacketFreqGauge.update();

  gaugeCharts.avgDestPacketFreqGauge.data.datasets[0].data[0] =
    (avgDestPacketFreq / 1000) * 100;
  gaugeCharts.avgDestPacketFreqGauge.data.datasets[0].data[1] =
    100 - gaugeCharts.avgDestPacketFreqGauge.data.datasets[0].data[0];
  gaugeCharts.avgDestPacketFreqGauge.update();

  gaugeCharts.totalTrafficVolumeGauge.data.datasets[0].data[0] =
    (totalTrafficVolume / 5000) * 100;
  gaugeCharts.totalTrafficVolumeGauge.data.datasets[0].data[1] =
    100 - gaugeCharts.totalTrafficVolumeGauge.data.datasets[0].data[0];
  gaugeCharts.totalTrafficVolumeGauge.update();
}

function requestNotificationPermission() {
  if (Notification.permission === "granted") {
    return Promise.resolve();
  } else if (Notification.permission !== "denied") {
    return Notification.requestPermission();
  } else {
    return Promise.reject("Notification permission denied");
  }
}

function sendNotification(title, body) {
  if (Notification.permission === "granted") {
    new Notification(title, { body });
  }
}

function checkForSuspiciousActivity(data) {
  // Example condition: Packet length exceeds 1500 bytes
  if (data.len > 1500) {
    sendNotification(
      "Suspicious Activity Detected",
      `High packet length: ${data.len}`
    );
  }

  // Example condition: Source packet frequency exceeds threshold
  if (data.src_packet_freq > 1000) {
    sendNotification(
      "Suspicious Activity Detected",
      `High source packet frequency: ${data.src_packet_freq}`
    );
  }

  // Add more conditions as needed
}

document.addEventListener("DOMContentLoaded", () => {
  requestNotificationPermission()
    .then(() => console.log("Notification permission granted"))
    .catch((err) => console.error("Notification permission denied", err));
});
