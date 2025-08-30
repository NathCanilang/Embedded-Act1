document.addEventListener("DOMContentLoaded", function () {
    const timeText = document.getElementById("timeDisplay");
    const tempText = document.getElementById("temperatureDisplay");
    const humidityText = document.getElementById("humidityDisplay");

    function startBuzzer() {
    fetch('/start_buzzer', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.status))
        .catch(err => console.error("Error:", err));
    }

    function stopBuzzer() {
    fetch('/stop_buzzer', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.status))
        .catch(err => console.error("Error:", err));
    }

    function displayCurrentTime() {
        const currentTime = new Date();
        const formattedTime = currentTime.toLocaleTimeString();
        timeText.textContent = formattedTime;
    }

    function displaySensorData() {
        fetch('/get_current_data')
            .then(response => response.json())
            .then(data => {
                console.log("Received Data:", data);
                tempText.textContent = "Temperature: " + data.temperature + " °C";
                humidityText.textContent = "Humidity: " + data.humidity + "%";

                if(data.temperature >= 38.0){
                    startBuzzer();
                }
                else{
                    stopBuzzer();
                }
            })
            .catch(error => console.log("Error fetching data: ", error));
    }

    setInterval(displayCurrentTime, 1000);
    setInterval(displaySensorData, 5000);
});
