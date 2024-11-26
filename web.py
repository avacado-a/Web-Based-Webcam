from flask import Flask, request, jsonify
from PIL import Image
import time
import face_recognition
import numpy as np
import cv2
import itertools

def check_overlap(rect1, rect2):
    """Checks if two rectangles overlap.

    Args:
        rect1 (tuple): (x1, y1, x2, y2) coordinates of the first rectangle.
        rect2 (tuple): (x1, y1, x2, y2) coordinates of the second rectangle.

    Returns:
        bool: True if rectangles overlap, False otherwise.
    """
    x1_1, y1_1, x2_1, y2_1 = rect1
    x1_2, y1_2, x2_2, y2_2 = rect2
    if x1_1 > x2_2 or x2_1 < x1_2:
        return False
    if y1_1 > y2_2 or y2_1 < y1_2:
        return False
    return True

app = Flask(__name__)

@app.route('/capture', methods=['POST'])
def capture():
    image_data = request.files['image'].read()
    image_rgb = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_rgb = cv2.resize(image_rgb, (1500, int(1500 * image_rgb.shape[:2][0] / image_rgb.shape[:2][1])))
    face_locations = list(set(face_recognition.face_locations(image_rgb,model="hog")))
    if len(face_locations) > 1:
        for i in list(itertools.combinations(face_locations, 2)):
            top1, right1, bottom1, left1, top2, right2, bottom2, left2 = i[0]+i[1]
            if check_overlap([bottom1,left1,top1,right1],[bottom2,left2,top2,right2]):
                face_locations.remove(i[1])
    # for top, right, bottom, left in face_locations:
    #     cv2.rectangle(image_rgb, (left, top), (right, bottom), (0, 0, 255), 2)
    # cv2.imwrite("letsgo.png",image_rgb)
    if len(face_locations) > 1:
        print(face_locations)
        cv2.imwrite("letsgoerror.png",image_rgb)
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
    <canvas id="canvas" width="640" height="480"></canvas>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const captureButton = document.getElementById('captureButton');
        var width = 640;
        var height = 480;
        navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 4000 },//{ ideal: 1920 },
                        height: { ideal: 4000 }//{ ideal: 1080 }
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
                        openNewTab();
                    }
                })
                .catch(error => {
                    console.error('Error sending image:', error);
                });
            });
        }
        var t=setInterval(checkFaces,1000*0.2);
    </script>
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True)