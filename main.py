import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer

def play_video(path):
    window_name = "Video"
    cap = cv2.VideoCapture(path)
    player = MediaPlayer(path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    fps = cap.get(cv2.CAP_PROP_FPS)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    video_frame_length = 1.0/fps
    interframe_wait_ms = round(video_frame_length*1000)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    video_time = 0
    cap_ret = True
    while (cap_ret):
        audio_frame, val = player.get_frame()
        if val != 'eof' and audio_frame is not None:
            img, audio_time = audio_frame
            frame = None
            while(video_time <= audio_time):
                cap_ret, frame = cap.read()
                if not cap_ret:
                    print("Reached end of video, exiting.")
                    break
                video_time = video_time + video_frame_length
            if frame is not None:
                # frame = cv2.resize(frame, (w, h))
                cv2.imshow(window_name, frame)
                if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
                    print("Exit requested.")
                    break

    cap.release()
    cv2.destroyAllWindows()
