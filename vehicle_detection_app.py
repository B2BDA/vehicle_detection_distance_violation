from detections.vehicle_detect import detectVehicle
import cv2
import numpy as np
from scipy.spatial import distance as dist
import imutils
import argparse

class DetectVehicle:
    
    def __init__(self):
        
        self.argparser = argparse.ArgumentParser()

        # self.argparser.add_argument('--input', '-i', type=str, default=r"C:\Users\bishw\Videos\vlc-record-2021-01-30-20h24m49s-MUMBAI TRAFFIC - INDIA.mp4-.mp4", help="Path of a input file" )

        self.argparser.add_argument('--output', '-o', type=str, default=r"C:\Users\bishw\Videos\output.avi", help="Path of a output file" )

        self.argparser.add_argument('--display', '-d', type=int, default=0, help="output of the frame will diplayed" )

        self.args = vars(self.argparser.parse_args())


        self.labels_path = r"D:\B2B_Git_Instance\vehicle_detection_distance_violation\coco.names"

        self.labels = open(self.labels_path).read().strip().split("\n")

        # load YOLO
        self.net = cv2.dnn.readNet(r"D:\B2B_Git_Instance\vehicle_detection_distance_violation\yolov3.cfg", r"D:\B2B_Git_Instance\vehicle_detection_distance_violation\yolov3.weights")

        # getting the layers form network
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0]-1] for i in self.net.getUnconnectedOutLayers()]

    def process_video(self, file_name):
        # loading video
        cap = cv2.VideoCapture(file_name)
        out = None

        while True:
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=800)
            results = detectVehicle(frame, self.net, self.ln,)
            unsafe_vehicle = set()
            if len(results) >= 2:
                # extract the centroids and find the euclidian distance between 2
                centroids = np.array([r[2] for r in results])
                D = dist.cdist(centroids, centroids, metric="euclidean")

                for i in range(0, D.shape[0]):
                    for j in range(i+1, D.shape[1]):
                        if D[i, j] < 160:
                            unsafe_vehicle.add(i)
                            unsafe_vehicle.add(j)
            for (i, (prob, box, centroid)) in enumerate(results):
                (sX, sY, eX, eY) = box
                (cX, cY) = centroid
                color = (0,255,0)
                if i in unsafe_vehicle:
                    color = (0,0,255)
                # draw rectangle
                cv2.rectangle(frame, (sX, sY), (eX, eY), color, 2)
                cv2.circle(frame, (cX, cY), 2, (0,0,255), 2)
                text = "Vehicle Distancing Violations: {}".format(len(unsafe_vehicle))
                cv2.putText(frame, text, (10,30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 0, 0), 3)

            if self.args["display"] > 0:
                cv2.imshow('frame', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

            if self.args["output"] != "" and out is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                out = cv2.VideoWriter(self.args["output"], fourcc, 25,
                                        (frame.shape[1], frame.shape[0]), True)

            if out is not None:
                out.write(frame)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    a = DetectVehicle()
    a.process_video()
    print("Done")