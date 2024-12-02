from flask import Flask, request, jsonify
#from PIL import Image
import time
#import face_recognition
import numpy as np
import cv2
import itertools
import dlib

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    a = time.perf_counter()
    detector = dlib.get_frontal_face_detector()
    image_data = request.files['image'].read()
    image_rgb = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_rgb = cv2.resize(image_rgb, (600, int(600 * image_rgb.shape[:2][0] / image_rgb.shape[:2][1])))
    dets, scores, idx = detector.run(image_rgb, 1)
    acd = 0
    for i in range(len(dets)):
        if scores[i] > 0.7:
            acd+=1
            print(dets[i],scores[i])
            d = dets[i]
            cv2.rectangle(image_rgb, (d.left(), d.top()), (d.right(), d.bottom()), (0, int(255*(scores[i]/2)), 0), 2)
            cv2.putText(image_rgb,"Score:"+str(scores[i]*50)+"% ",(d.right(), d.bottom()),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255))        
    cv2.imwrite("static/letsgo.png",image_rgb)
    if acd > 1:
        cv2.imwrite("static/letsgoerror.png",image_rgb)
        return jsonify({'success': False})
    else:
        return jsonify({'success': True})




@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html>
<head>
    <link rel="icon" type="image/png" href="/static/lgo.png"> 
    <title> Think Ahead! | Scholarship Applications</title>
</head>
<body>
    <video id="video" autoplay></video>
    <img id="bounded" src="/static/letsgo.png" />
    <img id="detection" src="/static/letsgo.png" />
    <canvas id="canvas" width="640" height="480"></canvas>

    <script>
        let video = document.getElementById('video');
        let canvas = document.getElementById('canvas');
        let bounded = document.getElementById('bounded');
        let detection = document.getElementById('detection');
        const captureButton = document.getElementById('captureButton');
        var width = 640;
        var height = 480;
        var lastValue = true;
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

        function openNewTab() {
            window.open("https://www.google.com", "_blank");
        }
        function loadImage() {
            bounded.src = "/static/letsgo.png?rand="+Math.random().toString();
        }
        function loadDetectImage() {
            detection.src = "/static/letsgoerror.png?rand="+Math.random().toString();
        }
        function checkFaces() {
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
                        if (lastValue) {
                            openNewTab();
                        }
                    }
                    lastValue = data.success;
                })
                .catch(error => {
                    console.error('Error sending image:', error);
                });
            });
        }
        var t=setInterval(checkFaces,1000*0.5);
        var t=setInterval(loadImage,1000);
        var t=setInterval(loadDetectImage,1000);
    </script>
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True)