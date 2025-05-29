import datetime
import time
from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

time_stamp = datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
file_name = f'{time_stamp}.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # or use 'XVID' and .avi if issues
captured_video = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

try:
    while True:
        img = ImageGrab.grab(bbox=(0, 0, width, height))
        img_np = np.array(img)
        img_final = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        cv2.imshow('ScreenRecorder', img_final)

        captured_video.write(img_final)
        if cv2.waitKey(1) == ord('q'):
            break

        time.sleep(1 / 20)  # Control FPS

except KeyboardInterrupt:
    print("Recording stopped manually.")

finally:
    captured_video.release()
    cv2.destroyAllWindows()
