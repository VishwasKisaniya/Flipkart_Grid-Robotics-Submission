// For Object Detection using RoboFlow API
function startObjectDetection() {
    document.getElementById("object-output").innerText = "Detecting objects...";
    
    // You can update this to trigger the actual POST request to Django endpoint /detect/object
    fetch('/detect/object', {
      method: 'POST',
      body: new FormData(document.querySelector('form[action="/detect/object"]'))
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("object-output").innerText = "Object Detected: " + data.output;
    })
    .catch(error => {
      document.getElementById("object-output").innerText = "Error in object detection.";
      console.error('Error:', error);
    });
  }
  
  // For Fruit/Vegetable Detection using local model
  function startFruitDetection() {
    document.getElementById("fruit-output").innerText = "Detecting fruit/vegetable...";
    
    // You can update this to trigger the actual POST request to Django endpoint /detect/fruit
    fetch('/detect/fruit', {
      method: 'POST',
      body: new FormData(document.querySelector('form[action="/detect/fruit"]'))
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("fruit-output").innerText = "Fruit Detected: " + data.prediction;
    })
    .catch(error => {
      document.getElementById("fruit-output").innerText = "Error in fruit/vegetable detection.";
      console.error('Error:', error);
    });
  }
  
  // For Text Detection from Camera Stream
  function startCameraDetection() {
    document.getElementById("text-output").innerText = "Starting camera detection...";
  
    fetch('/capture_from_camera', {
      method: 'POST',
      body: new FormData(document.querySelector('form[action="/capture_from_camera"]'))
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("text-output").innerText = "Extracted Text: " + data.text;
    })
    .catch(error => {
      document.getElementById("text-output").innerText = "Error in text detection.";
      console.error('Error:', error);
    });
  }
  