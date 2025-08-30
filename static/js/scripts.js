document.addEventListener("DOMContentLoaded", function(){

    timeText=this.getElementById("timeDisplay");
    tempText = this.getElementById("temperatureDisplay")
    humidityText = this.getElementById("humidityDisplay");

    function displayCurrentTime(){
        const currentTime = new Date();
        const formattedTime = currentTime.toLocaleTimeString();
        timeText.textContent = formattedTime;
    };

    function displaySensorData(){
        fetch('/get_current_data')
        .then(response => response.json)
        .then(data => {
            console.log(`Received Data: ${data}`);
            tempText =  "Temparature: " + data.temperature;
            humidityText = "Humidity: " + data.humidity;

        })
        .catch(error=> console.log("Error fetching data: ", error));
    };

    setInterval(displayCurrentTime, 1000);
    setInterval(displaySensorData, 5000);
});
