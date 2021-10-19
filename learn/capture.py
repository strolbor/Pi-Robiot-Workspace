# TestFile zur Videoaufnahme mit OpenCV

import cv2

video_capture = cv2.VideoCapture(0)
# Check success
if not video_capture.isOpened():
    raise Exception("Could not open video device")
# Read picture. ret === True on success
ret, frame = video_capture.read()
print(ret)
print("---")
print(frame)
cv2.imwrite("/root/cap.jpg",frame)
# Close device
video_capture.release()