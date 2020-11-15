'''
Object detection ("Ball tracking") with OpenCV
    Adapted from the original code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018
'''

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

def spiral(b, tmax, nb, xc=0, yc=0, phi=0):

    t = np.linspace(0,tmax,nb)

    x_sp = ( (b*t)*np.cos(t+phi) + xc )#*np.cos(phi)
    y_sp = ( (b*t)*np.sin(t+phi) + yc )#*np.sin(phi)

    return x_sp, y_sp

def dist( x, p ):

    return np.sqrt( (x[0]-p[0])**2 + (x[1]-p[1])**2 )

def closest (num, arr):
    curr = arr[0]
    for val in arr:
        if abs (num - val) < abs (num - curr):
            curr = val
    return curr

def main():

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "yellow object"
    # (or "ball") in the HSV color space, then initialize the
    # list of tracked points
    colorLower = (0, 0, 180)
    colorUpper = (33, 80, 255)
    pts = deque(maxlen=args["buffer"])

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)

        # otherwise, grab a reference to the video file
    else:
        camera = cv2.VideoCapture(args["video"])

    WIN_SRC = "Source"
    cv2.namedWindow(WIN_SRC, cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow(WIN_SRC, 0, 0) #750,  2 (bernat =0)

    framenum = 0

    srcS = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    testname = 'test_tracking.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'MP4V') #lossless codec
    out_video = cv2.VideoWriter( testname, fourcc, 30, (srcS[0],srcS[1]) )

        # keep looping
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        framenum += 1

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if args.get("video") and not grabbed:
                out_video.release()
                break
        if args.get("video") and framenum > 430:
                out_video.release()
                break

        # resize the frame, inverted ("vertical flip" w/ 180degrees),
        # blur it, and convert it to the HSV color space
        # frame = imutils.resize(frame, width=600)
        # frame = imutils.rotate(frame, angle=180)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                # c = max(cnts, key=cv2.contourArea)
                x, y, radius, c, n = None, None, None, None, 0
                # cv2.circle(frame, (450,480), 50, (255, 0, 0), 2)
                # cv2.circle(frame, (1500,480), 50, (255, 0, 0), 2)
                x_ref, y_ref, r_ref = 1000, 480, 450
                for c in cnts:
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    if (x - x_ref)**2 + (y - y_ref)**2 < r_ref**2:
                        if radius < 35 and radius > 20:
                            M = cv2.moments(c)
                            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                            cv2.circle(frame, (int(x), int(y)), int(radius),
                                       (0, 255, 255), 2)
                            cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    # __draw_label(frame, str(n), center, (0,255,255))
                    # n += 1

                # only proceed if the radius meets a minimum size
                # if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                # cv2.circle(frame, (int(x), int(y)), int(radius),
                #            (0, 255, 255), 2)
                # cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)

        if center is not None:
            b_sp= 20
            tmax = 100

            teta = np.arctan( (center[1]-y_ref)/(center[0]-x_ref) )
            op = dist( center, (x_ref,y_ref) )
            # print(op)
            # print(b_sp)
            t_target = op/b_sp

            x_sp_1, y_sp_1 = spiral(b_sp, tmax, 1000, xc=x_ref, yc=y_ref, phi = -(t_target-teta) )
            x_sp_2, y_sp_2 = spiral(b_sp, tmax, 1000, xc=x_ref, yc=y_ref, phi = -(t_target-teta+np.pi) )

            dist_1 = np.zeros(len(x_sp_1)-1)
            dist_2 = np.zeros(len(x_sp_2)-1)
            for j in range(len(x_sp_1)-1):
                dist_1[j] = dist( (x_sp_1[j], y_sp_1[j]), center )
                dist_2[j] = dist( (x_sp_2[j], y_sp_2[j]), center )

            if np.min(abs(dist_1)) < np.min(abs(dist_2)):
                x_sp, y_sp = x_sp_1, y_sp_1
            else:
                x_sp, y_sp = x_sp_2, y_sp_2

            # pos_1 = np.where( dist_1 == closest( 0, dist_1 ) )
            # pos_2 = np.where( dist_2 == closest( 0, dist_2 ) )

            for j in range(1, len(x_sp)):
                if x_sp[j - 1] is None or x_sp[j] is None or framenum < 60:
                    continue

                sp_jm1 = ( np.rint(x_sp[j-1]).astype(np.int), np.rint(y_sp[j-1]).astype(np.int) )
                sp_j =   ( np.rint(x_sp[j]).astype(np.int), np.rint(y_sp[j]).astype(np.int) )

                if (sp_jm1[0] - x_ref)**2 + (sp_jm1[1] - y_ref)**2 > r_ref**2: continue

            # if center is not None:
                r_int = np.sqrt( (x_ref - center[0])**2 + (y_ref - center[1])**2 )
                if (sp_jm1[0] - x_ref)**2 + (sp_jm1[1] - y_ref)**2 < r_int**2: continue

                #thickness = 3
                thickness = int(np.sqrt(args["buffer"] / float(j/50 + 1)) * 2.5)
                # cv2.line(frame, sp_jm1, sp_j, (152, 152, 48), thickness)
                color_sp =  (0, 159, 255)
                cv2.line(frame, sp_jm1, sp_j, color_sp, thickness)
            #     r_int_old = r_int
            # else:
            #     if (sp_jm1[0] - x_ref)**2 + (sp_jm1[1] - y_ref)**2 < r_int_old**2: continue

            # print(sp_jm1)
            # print(sp_j)
            # print('ciao')

            # thickness = int(np.sqrt(args["buffer"] / float(j/10 + 1)) * 2.5)
            # if thickness == 0: thickness += 1


                # loop over the set of tracked points
        for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
            if pts[i - 1] is None or pts[i] is None:
                continue

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
            color_track = (255, 110, 26)
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], color_track, thickness)

        # show the frame to our screen
        cv2.imshow(WIN_SRC, frame)
        out_video.write(frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
                break

#######################################################################
if __name__ == "__main__":
    main()
