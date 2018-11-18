from __future__ import absolute_import, division, print_function

from java import constructor, method, static_proxy, jint, jarray, jdouble, jboolean, jclass

from java.lang import String

from scipy.signal import butter, lfilter
from sklearn.decomposition import FastICA
import numpy as np

import scipy
import cv2
import imutils
class Butter(static_proxy()):
    @constructor([])
    def __init__(self):
        super(Butter, self).__init__()

    '''In PulseRateAlgorithm: 
                y = butter_bandpass_filter(
                    detrend, lowcut, highcut, fs, order=4)'''

    @method(jarray(jarray(jdouble)), [jarray(jarray(jdouble)), jdouble, jdouble, jdouble, jint])
    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

class NpScipy(static_proxy()):
    @constructor([])
    def __init__(self):
        super(NpScipy, self).__init__()


    '''In PulseRateAlgorithm: 
                ica = FastICA(whiten=False)
                window = (window - np.mean(window, axis=0)) / \
                    np.std(window, axis=0)  # signal normalization
                # S = np.c_[array[cutlow:], array_1[cutlow:], array_2[cutlow:]]
                # S /= S.std(axis=0)
                # ica = FastICA(n_components=3)
                # print(np.isnan(window).any())
                # print(np.isinf(window).any())
                # ica = FastICA()
                window = np.reshape(window, (150, 1))
                S = ica.fit_transform(window)  # ICA Part
                ...
                ...
                detrend = scipy.signal.detrend(S)'''
    @method(jarray(jarray(jdouble)), [jarray(jdouble), jboolean])
    def get_detrend(self, window, dummyBoolean):
        ica = FastICA(whiten=False)

        window = (window - np.mean(window, axis=0)) / \
                 np.std(window, axis=0)  # signal normalization
        window = np.reshape(window, (9, 1))#NOTE: it was (150, 1)

        S = ica.fit_transform(window)  # ICA Part
        detrend = scipy.signal.detrend(S)
        return detrend.tolist()


    '''In PulseRateAlgorithm: 
                powerSpec = np.abs(np.fft.fft(y, axis=0)) ** 2'''
    @method(jarray(jarray(jdouble)), [jarray(jarray(jdouble)), jboolean])
    def get_powerSpec(self, y, dummyBoolean):
        return (np.abs(np.fft.fft(y, axis=0)) ** 2).tolist()


    '''In PulseRateAlgorithm: 
                freqs = np.fft.fftfreq(150, 1.0 / 30)'''
    @method(jarray(jdouble), [jint, jdouble])
    def fftfreq(self,a, b):
        return np.fft.fftfreq(a, b).tolist()
    '''
    @method(jdouble,[])
    def CCW(self):
        #Point = jclass("main/java/com/kevintkuo/datasciencelibrary/Coordinate")
        A = self.Point(0.0,10.0)
        return A.x
    '''



'''
    @method(jdouble, [jarray(jarray(jint)),jarray(jarray(jdouble)), jboolean])
    def getHeartRate(self, shape, frame, dummyBoolean):
        shape = face_utils.shape_to_np(shape)
        counter = 0
        initframecounter = 0

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image

        for (x, y) in shape:

            cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
            cv2.putText(frame, str(counter), (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            # setting face as found
            foundlandmark = True

            # saving particular face landmarks for the ROI box
            if counter == 21:
                a1x = x
                a1y = y / 1.3
            if counter == 22:
                a2x = x
                a2y = y
            if counter == 27:
                a3x = x
                a3y = y
            if counter == 8:
                a4x = x
                a4y = y
            if counter == 23:
                a5x = x
                a5y = y

            if counter == 17:
                b1x = x
                b1y = y * 1.2
            if counter == 31:
                b2x = x
                b2y = y
            if counter == 28:
                b3x = x
                b3y = y
            if counter == 39:
                b4x = x
                b4y = y
                ixc = (a1x + a2x) / 2.2
                iyc = (a4y + a3y)

            if counter == 26:
                c1x = x
                c1y = y / 1.2
            if counter == 35:
                c2x = x
                c2y = y
            if counter == 28:
                c3x = x
                c3y = y
            if counter == 42:
                c4x = x
                c4y = y

            if counter == 16:
                d1x = x * 1.1
                d1y = y

            if counter == 0:
                e1x = x / 1.15
                e1y = y

            counter = counter + 1

        firstframe = 0
        initframecounter = initframecounter + 1



        # co-ordinates for the rectangle
        listforehead = [int(a1x), int(a1y), a2x, a2y]
        listleftface = [int(b1x), int(b3y), b4x, b2y]
        listrightface = [int(c1x), int(c3y), c4x, c2y]

        cv2.rectangle(frame, (listforehead[0], listforehead[1]), (
            listforehead[2], listforehead[3]), (255, 0, 0), 2)
        cv2.rectangle(frame, (listleftface[0], listleftface[1]), (
            listleftface[2], listleftface[3]), (255, 0, 0), 2)
        cv2.rectangle(frame, (listrightface[0], listrightface[1]), (listrightface[2], listrightface[3]),
                      (255, 0, 0), 2)

        # converting the frame to HSV
        HSVframe = CoverttoHSV(HSVframe)

        # checkig if this is the first frame
        if firstframe == 0:
            if first == True:
                listtocheck = listforehead
                firstframe = 1
                first = False

        # setting up intital frames to measure the Bluriness value
        # setting up the blurriness threshold from the frist 6 seconds
        # checking the following frames and comparing it to the bluriness value
        # sharpen the frames if needed depending on the blurriness mean
        if (initframecounter / 2) < 6:
            if enterif == True:
                if countdowntime == 0:
                    HistoryList.append(gray)
                notmoving = checkpixeldiff(listtocheck, listforehead)
                if notmoving == False:
                    text = "You Moved. Starting countdown again"
                    resetloop = True
                    HistoryList = []
                    continue

        else:
            if enterif == True:
                initframecounter = 0
                if countdowntime == 0:
                    notmoving = checkpixeldiff(listtocheck, listforehead)
                    if notmoving == True:
                        enterif = False
                        continue
                    else:
                        resetloop = True
                        HistoryList = []

                        continue
                countdowntime = countdowntime - 1

        if enterif == False:

            threshold = findvarmean(HistoryList)
            if cv2.Laplacian(gray, cv2.CV_64F).var() < threshold:
                HSVframe = cv2.bilateralFilter(HSVframe, 9, 75, 75)
                gaussian = cv2.GaussianBlur(HSVframe, (9, 9), 10.0)
                HSVframe = cv2.addWeighted(
                    HSVframe, 1.5, gaussian, -0.5, 0, HSVframe)

            else:
                HistoryList.pop(listcounter)
                HistoryList.append(gray)
                threshold = findvarmean(HistoryList)
                listcounter = listcounter + 1
                if listcounter == len(HistoryList):
                    listcounter = 0

        if enterif == True:
            currentcount = countdowntime
            if foundlandmark == False:
                ctd = "Searching For Face"
            else:
                ctd = "Face Found"

            ctd2 = ctd
            cv2.putText(frame, ctd, (30, 30),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255))

        # setting the previous ROI to cerrent ROI
        prevROI1 = currROI1
        prevROI2 = currROI2
        prevROI3 = currROI3

        # setting the current ROI to next ROI
        currROI1 = gray[listforehead[1]:listforehead[1] +
                                        10, listforehead[0]:listforehead[0] + 10]
        currROI2 = gray[listleftface[1]:listleftface[1] +
                                        10, listleftface[0]:listleftface[0] + 10]
        currROI3 = gray[listrightface[1]:listrightface[1] +
                                         10, listrightface[0]:listrightface[0] + 10]

        pointsListRoi1, pointsListRoi2, pointsListRoi3, avelist1, avearray2, Normalizedlist = [], [], [], [], [], [
            8]

        # finding the middle points of the region of interest for Kalman Filter Calculation
        for x1 in range(1):
            a1 = int((listforehead[0] + listforehead[2]) / 2) + x1
            b1 = int((listleftface[0] + listleftface[2]) / 2) + x1
            c1 = int((listrightface[0] + listrightface[2]) / 2) + x1
            for y1 in range(5):
                a2 = int((listforehead[1] + listforehead[3]) / 2) + y1
                b2 = int((listleftface[1] + listleftface[3]) / 2) + y1
                c2 = int((listrightface[1] + listrightface[3]) / 2) + y1

                tup1 = (a1, a2)
                tup2 = (b1, b2)
                tup3 = (c1, c2)

                pointsListRoi1.append(tup1)
                pointsListRoi2.append(tup2)
                pointsListRoi3.append(tup3)
                allPoints = pointsListRoi1 + pointsListRoi2 + pointsListRoi3
            d = 0

        # if face is found
        if foundlandmark == True:
            # seeting the previous to current
            prevlistforehead = listforehead
            prevlistleftface = listleftface
            prevlistrightface = listrightface
            prevallpoints = allPoints
            topright = (pts[0][0], pts[0][1])
            bottomright = (pts[1][0], pts[1][1])
            topleft = (pts[3][0], pts[3][1])
            bottomleft = (pts[2][0], pts[2][1])

            # Passing the points to the Kalman filter
            ptsss = kalman_filter(
                topleft, bottomleft, topright, bottomright, allPoints, foundlandmark)

            # finding the length of the ROI
            a11 = int(abs(listforehead[0] - listforehead[2]) / 4)
            b11 = int(abs(listleftface[0] - listleftface[2]) / 4)
            c11 = int(abs(listrightface[0] - listrightface[2]) / 4)

            a22 = int(abs(listforehead[1] - listforehead[3]) / 4)
            b22 = int(abs(listleftface[1] - listleftface[3]) / 4)
            c22 = int(abs(listrightface[1] - listrightface[3]) / 4)

            ptsss2 = [ptsss[0], ptsss[5], ptsss[10]]

            # Finding the HSV value of the points of the ROI and storing it
            for xaxis in range(ptsss[0][0] - a11, ptsss[0][0] + a11):
                for yaxis in range(ptsss[0][1] - a22, ptsss[0][1] + a22):
                    Normalizedlist.append(HSVframe[yaxis][xaxis][0])
            cv2.circle(
                frame, (ptsss[0][0], ptsss[0][1]), 8, (0, 0, 255), -1)

            for xaxis in range(ptsss[5][0] - b11, ptsss[5][0] + b11):
                for yaxis in range(ptsss[5][1] - b22, ptsss[5][1] + b22):
                    Normalizedlist.append(HSVframe[yaxis][xaxis][0])
            cv2.circle(
                frame, (ptsss[5][0], ptsss[5][1]), 8, (0, 0, 255), -1)

            for xaxis in range(ptsss[10][0] - c11, ptsss[10][0] + c11):
                for yaxis in range(ptsss[5][1] - c22, ptsss[5][1] + c22):
                    Normalizedlist.append(HSVframe[yaxis][xaxis][0])
            cv2.circle(
                frame, (ptsss[10][0], ptsss[10][1]), 8, (0, 0, 255), -1)

            avearray2 = np.asarray(Normalizedlist)
            # taking the mean of the ROi
            totalmean = int(np.mean(avearray2))

        else:

            # When face not found work with previous values
            # Passing the points to the Kalman filter
            ptsss = kalman_filter(
                topleft, bottomleft, topright, bottomright, ptsss, foundlandmark)
            ptsss2 = [ptsss[0], ptsss[5], ptsss[10]]

            # Finding the HSV value of the points of the ROI and storing it
            for xaxis in range(ptsss[0][0] - a11, ptsss[0][0] + a11):
                for yaxis in range(ptsss[0][1] - a22, ptsss[0][1] + a22):
                    Normalizedlist.append(HSVframe[yaxis][xaxis][0])

            # cv2.circle(frame, (ptsss[0][0], ptsss[0][1]), 8, (0, 0, 255), -1)

            for xaxis in range(ptsss[5][0] - b11, ptsss[5][0] + b11):
                for yaxis in range(ptsss[5][1] - b22, ptsss[5][1] + b22):
                    Normalizedlist.append(HSVframe[yaxis][xaxis][0])

            # cv2.circle(frame, (ptsss[5][0], ptsss[5][1]), 8, (0, 0, 255), -1)

            for xaxis in range(ptsss[10][0] - c11, ptsss[10][0] + c11):
                for yaxis in range(ptsss[5][1] - c22, ptsss[5][1] + c22):
                    Normalizedlist.append(HSVframe[yaxis][xaxis][0])
            # cv2.circle(frame, (ptsss[10][0], ptsss[10][1]), 8, (0, 0, 255), -1)

            avearray2 = np.asarray(Normalizedlist)
            # Taking the mean of the ROI
            totalmean = int(np.mean(avearray2))
'''


