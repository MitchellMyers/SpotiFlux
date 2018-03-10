import cv2
import numpy as np
import math


class PersonDetector:

    # Malisiewicz et al.
    def non_max_suppression(self, boxes, overlapThresh):
        # if there are no boxes, return an empty list
        if len(boxes) == 0:
            return []

        # if the bounding boxes integers, convert them to floats --
        # this is important since we'll be doing a bunch of divisions
        if boxes.dtype.kind == "i":
            boxes = boxes.astype("float")

        # initialize the list of picked indexes
        pick = []

        # grab the coordinates of the bounding boxes
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        # compute the area of the bounding boxes and sort the bounding
        # boxes by the bottom-right y-coordinate of the bounding box
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)

        # keep looping while some indexes still remain in the indexes
        # list
        while len(idxs) > 0:
            # grab the last index in the indexes list and add the
            # index value to the list of picked indexes
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)

            # find the largest (x, y) coordinates for the start of
            # the bounding box and the smallest (x, y) coordinates
            # for the end of the bounding box
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])

            # compute the width and height of the bounding box
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            # compute the ratio of overlap
            overlap = (w * h) / area[idxs[:last]]

            # delete all indexes from the index list that have
            idxs = np.delete(idxs, np.concatenate(([last],
                                                   np.where(overlap > overlapThresh)[0])))

        # return only the bounding boxes that were picked using the
        # integer data type
        return boxes[pick].astype("int")



    def GetNumberOfPersons(self):
        cap = cv2.VideoCapture(0)
        hogDescriptor = cv2.HOGDescriptor()
        hogDescriptor.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        count = 0
        personCount = []
        while (True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            (rects, weights) = hogDescriptor.detectMultiScale(frame,
                                                    winStride = (4, 4),
                                                    padding = (8, 8),
                                                    scale=1.05)

            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
            pick = self.non_max_suppression(rects, overlapThresh=0.65)

            personCount.append(len(rects))
            if count % 1000 == 0:
                avgCount = np.average(personCount)
                avgCount = math.floor(avgCount)
                print("Person Count: {}".format(avgCount))
                count = 0
                personCount = []


            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

