from flask import Flask, request, jsonify
#from PIL import Image
#import time
#import face_recognition
import numpy as np
import cv2
import itertools
import dlib

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
    detector = dlib.get_frontal_face_detector()
    image_data = request.files['image'].read()
    image_rgb = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_rgb = cv2.resize(image_rgb, (800, int(800 * image_rgb.shape[:2][0] / image_rgb.shape[:2][1])))
    dets, scores, idx = detector.run(image_rgb, 1)
    # if len(face_locations) > 1:
    #     for d,e in list(itertools.combinations(face_locations, 2)):
    #         left1, top1, right1, bottom1, left2, top2, right2, bottom2 = d.left(), d.top(), d.right(), d.bottom(), e.left(), e.top(), e.right(), e.bottom() 
    #         if check_overlap([bottom1,left1,top1,right1],[bottom2,left2,top2,right2]):
    #             face_locations.remove(d)
    faces = []
    for i in range(len(dets)):
        if scores[i] > 0.7:
            print(dets[i],scores[i])
            faces.append(dets[i])
    for d in dets:
        cv2.rectangle(image_rgb, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)
    cv2.imwrite("static/letsgo.png",image_rgb)
    if len(list(dets)) > 1:
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
    <img id="bounded" src="/static/letsgo.png" />
    <canvas id="canvas" width="640" height="480"></canvas>

    <script>
        let video = document.getElementById('video');
        let canvas = document.getElementById('canvas');
        let bounded = document.getElementById('bounded');
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
        var t=setInterval(checkFaces,1000*1);
        var t=setInterval(loadImage,1000);
    </script>
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True)