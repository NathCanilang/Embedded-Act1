document.addEventListener("DOMContentLoaded", function () {
  const timeText = document.getElementById("timeDisplay");
  const tempText = document.getElementById("temperatureDisplay");
  const humidityText = document.getElementById("humidityDisplay");

  function startBuzzer() {
    fetch("/start_buzzer", { method: "POST" })
      .then((response) => response.json())
      .then((data) => console.log(data.status))
      .catch((err) => console.error("Error:", err));
  }

  function stopBuzzer() {
    fetch("/stop_buzzer", { method: "POST" })
      .then((response) => response.json())
      .then((data) => console.log(data.status))
      .catch((err) => console.error("Error:", err));
  }

  function displayCurrentTime() {
    const currentTime = new Date();
    const formattedTime = currentTime.toLocaleTimeString();
    timeText.textContent = formattedTime;
  }

  function displaySensorData() {
    fetch("/get_current_data")
      .then((response) => response.json())
      .then((data) => {
        console.log("Received Data:", data);
        tempText.textContent = "Temperature: " + data.temperature + " °C";
        humidityText.textContent = "Humidity: " + data.humidity + "%";

        if (data.temperature >= 38.0) {
          startBuzzer();
        } else {
          stopBuzzer();
        }
      })
      .catch((error) => console.log("Error fetching data: ", error));
  }

  //for chart
  const canvas = document.getElementById("dht11Chart").getContext("2d");
  const sensorChart = new Chart(canvas, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Humidity (%)",
          data: [],
          borderColor: "blue",
          fill: false,
          tension: 0.1,
          yAxisID: "yLeft",
        },
        {
          label: "Temperature (°C)",
          data: [],
          borderColor: "red",
          fill: false,
          tension: 0.1,
          yAxisID: "yRight",
        },
      ],
    },
    options: {
      responsive: false,
      scales: {
        x: {
          title: { display: true, text: "Date Time" },
        },
        yLeft: {
          type: "linear",
          position: "left",
          title: { display: true, text: "Humidity (%)" },
          beginAtZero: true,
        },
        yRight: {
          type: "linear",
          position: "right",
          title: { display: true, text: "Temperature (°C)" },
          beginAtZero: true,
          grid: {
            drawOnChartArea: false,
          },
        },
      },
    },
  });

  function displayChartDataFromDB() {
    fetch("/get_data_from_db")
      .then((response) => response.json())
      .then((data) => {
        if (!data) return;

        //insert data to chart
        sensorChart.data.labels.push(data.timestamp);
        sensorChart.data.datasets[0].data.push(data.humidity);
        sensorChart.data.datasets[1].data.push(data.temperature);

        //max 8 base doon sa pic
        if (sensorChart.data.labels.length > 8) {
          sensorChart.data.labels.shift();
          sensorChart.data.datasets[0].data.shift();
          sensorChart.data.datasets[1].data.shift();
        }

        sensorChart.update();
      })
      .catch((err) =>
        console.error("Error fetching sensor readings history:", err)
      );
  }

  setInterval(displayCurrentTime, 1000);
  setInterval(displaySensorData, 5000);
  setInterval(displayChartDataFromDB, 5000);
});
