# Web-Based-Camera
## What is it
Run a python script that uses the camera on a computer where Python is not allowed to be downloaded


# How to use Web-Based-Camera
## Create a Github Account
If you don't have a GitHub account, then you need to make one. Go to https://github.com/ and sign up
## Create Codespace
To run this, you need to make a codespace. Go to [https://github.com/avacado-a/Web-Face-Detection](https://github.com/avacado-a/Web-Based-Webcam). Click the green code button. Go to the codedspaces tab and click the plus.
## Run the program
After you do this, a codespace should open. When it fully loads, go to Terminal and run these lines.
```bash
pip install flask opencv-python-headless
```
Once it completes, go to the *Extensions* tab on the side of the codespace.
Search Python and click the green install button next to the first option.
Click on the *Explorer* side tab. Click on web.py. Click the run button in the top right (triangle)
When you do that, you should see a notification that says *Your application running on port 5000 is available.  [See all forwarded ports](command:~remote.forwardedPorts.focus)*
Click on the green *Open in Browser* button
It will open a new tab that will ask to use your camera. Press allow.
Your done!
## Restart program
If the program stops working all of a sudden, report the issue at [Github](https://github.com/avacado-a/Web-Face-Detection/issues)
Then, try restarting the program by:
1. Going to the bottom right corner and hovering over the python tab.
2. Click on the trash can that appears.
3. Then, click the run button agian in the top right corner of the codespace (triangle)
4. When you do that, you should see a notification that says *Your application running on port 5000 is available.  [See all forwarded ports](command:~remote.forwardedPorts.focus)*
5. Click on the green *Open in Browser* button
6. It will open a new tab that may ask to use your camera again. Press allow.
