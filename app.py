import datetime
import time
from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

def is_recording_time():
    now = datetime.datetime.now()
    if now.weekday() >= 5: # Saturday or Sunday
        return False, None

    current_time = now.hour * 60 + now.minute
    am_session_start = 16 * 60 + 25
    am_session_end = 18 * 60
    pm_session_start = 20 * 60 + 25
    pm_session_end = 22 * 60

    if am_session_start <= current_time <= am_session_end:
        return True, "AM"
    elif pm_session_start <= current_time <= pm_session_end:
        return True, "PM"
    return False, None

def create_video_writer():
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = f'{time_stamp}.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' and .avi if issues
    return cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

current_session = None
captured_video = None

try:
    while True:
        should_record, session = is_recording_time()

        if should_record and session != current_session:
            if captured_video is not None:
                captured_video.release()
            current_session = session
            captured_video = create_video_writer()

        elif not should_record and captured_video is not None:
            captured_video.release()
            current_session = None
            captured_video = None

        if not should_record:
            cv2.waitKey(60000)
            continue

        img = ImageGrab.grab(bbox=(0, 0, width, height))
        img_np = np.array(img)
        img_final = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        cv2.imshow('ScreenRecorder', img_final)

        if captured_video is not None:
            captured_video.write(img_final)

        if cv2.waitKey(1) == ord('q'):
            break

        time.sleep(1 / 20)  # Control FPS
except KeyboardInterrupt:
    print("Recording stopped manually.")

finally:
    if captured_video is not None:
        captured_video.release()
    cv2.destroyAllWindows()
