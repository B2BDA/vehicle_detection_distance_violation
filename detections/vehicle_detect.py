import cv2
import numpy as np


def detectVehicle(frame, net, ln):
    # extract the dimensions of the frame
    (h, w) = frame.shape[:2]
    results = []
    # create a blob frome the image
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1 / 255.0,
                                 size=(416,416),
                                 swapRB=True,
                                 crop=False)
    # forward pass for YOLO object detector, will give a boundig box
    net.setInput(blob)
    outputs = net.forward(ln)

    boxes = []
    centroids = []
    confidences = []

    # loop to each layer outputs
    for out in outputs:
        for detection in out:
            # extract class ID and confidences from detection
            scores = detection[5:]
            class_ID = np.argmax(scores)
            confidence = scores[class_ID]

            # filter out the car from detection
            # here in YOLO labels car index is 2
            if class_ID == 2 and confidence > 0.3:
                # YOLO detector returns a center(x, y) of a bounding box
                # followed with width and height
                box = detection[0:4] * np.array([w, h, w, h])
                (cX, cY, width, height) = box.astype('int')

                # calaculate top left (x, y) from centerX and Center Y
                x = int(cX - (width / 2))
                y = int(cY - (height / 2))

                # update a list
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                centroids.append((cX, cY))
    # apply NMS- non-max suppression for weak bounding boxes
    idx = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.3)

    # for one box
    if len(idx) > 0:
        for i in idx.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # update the result and return
            res = (confidences[i], (x, y, x+w, y+h), centroids[i])
            results.append(res)

    return results
