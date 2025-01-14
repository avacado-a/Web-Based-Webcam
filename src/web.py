from flask import Flask, request, jsonify, send_file
from PIL import Image
import time
#import face_recognition
import numpy as np
import cv2
import os

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.files['image'].read()
    cv2_image = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite("static/letsgo.png",cv2_image)
    return jsonify({'success': True})

@app.route('/show', methods=['POST'])
def capture():
    return send_file("letsgo.png")



@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html>
<head>
    <link rel="icon" type="image/png" href="/static/lgo.png"> 
</head>
<body>
    <video id="video" autoplay></video>
    <canvas id="canvas" width="640" height="480"></canvas>
    <script>
        let video = document.getElementById('video');
        let canvas = document.getElementById('canvas');
        let bounded = document.getElementById('bounded');
        let detection = document.getElementById('detection');
        var width = 640;
        var height = 480;
        navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 4000 },//{ ideal: 1920 },
                        height: { ideal: 4000 },//{ ideal: 1080 }
                        facingMode: { exact: "user" }
                    }
                })
                .then(function(stream) {
                video.srcObject = stream;
                video.onloadedmetadata = () => {
                    width = video.videoWidth;
                    height = video.videoHeight;
                    video.width = width.toString();
                    video.height = height.toString();
                    canvas.width = width.toString();
                    canvas.height = height.toString();
                    console.log(`Webcam image size: ${width} x ${height}`);
                };
            })
            .catch(function(error) {
                console.error('Error accessing media devices.', error);
            });
        function check() {
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(function(blob) {
                const formData = new FormData();
                formData.append('image', blob, 'letsgo.png'); // Adjust filename as needed
                fetch('/capture', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        console.log('Image saved successfully!');
                    } else {
                        console.log('Error saving image');
                    }
                })
                .catch(error => {
                    console.error('Error sending image:', error);
                });
            });
        }
        var t=setInterval(check,1000*0.05);
    </script>
</body>
</html>"""

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)