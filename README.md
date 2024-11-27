# Web-Face-Detection
## What is it
Web-Face-Detection uses your browser to access your camera stream and detect faces to see if anyone is watching your computer behind your back.


# How to install Web-Face-Detection
## Create a Github Account
If you don't have a GitHub account, then you need to make one. Go to https://github.com/ and sign up
## Create Codespace
To run this, you need to make a codespace. Go to https://github.com/avacado-a/Web-Face-Detection. Click the green code button. Go to the codedspaces tab and click the plus.
## Run the program
After you do this, a codespace should open. When it fully loads, go to Terminal and run these lines.
1. It may take a long time. Let it finish completely (It may take 10 minutes!)
2. If the message *High codespace CPU (100%) utilization detected. Consider stopping some processes for the best experience.* appears, ignore it.
```bash
pip install dlib -vvv
pip install flask Pillow face_recognition opencv-python-headless
```
Go to the *Extensions* tab on the side of the codespace.
Search Python and click the green install button next to the first option.
Click on the *Explorer* side tab. Click on web.py. Click the run button in the top right (triangle)
When you do that, you should see a notification that says *Your application running on port 5000 is available.  [See all forwarded ports](command:~remote.forwardedPorts.focus)*
Click on the green *Open in Browser* button
It will open a new tab that will ask to use your camera. Press allow.
### Now the program will detect how many faces are in the webcam. If there are more than 1 face detected, it will open a new tab.
## Restart program
If the program stops working all of a sudden, report the issue at [Github](https://github.com/avacado-a/Web-Face-Detection/issues)
Then, try restarting the program by:
1. Going to the bottom right corner and hovering over the python tab.
2. Click on the trash can that appears.
3. Then, click the run button agian in the top right corner of the codespace (triangle)
4. When you do that, you should see a notification that says *Your application running on port 5000 is available.  [See all forwarded ports](command:~remote.forwardedPorts.focus)*
5. Click on the green *Open in Browser* button
6. It will open a new tab that may ask to use your camera again. Press allow.
