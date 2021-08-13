import time, cv2
from threading import Thread
from djitellopy import Tello


# connect to tello and start video stream
tello = Tello()
tello.connect()
keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()


# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video
recorder = Thread(target=videoRecorder)


# begin flight, then recording
tello.takeoff()
recorder.start()


# fly two squares at different elevations around a center object
flySquare(100)
tello.move_up(20)
flySquare(100)


# end recording
keepRecording = False
recorder.join()


tello.land()




def videoRecorder():
    # create a VideoWrite object, .mp4 codec
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 30, (width, height))


    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()


# fly in a square, facing the center at all times
def flySquare(width):
    for(int i = 0; i < 4; i++){
        tello.move_right(width)
        tello.rotate_counter_clockwise(90)
    }