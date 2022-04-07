from math import sqrt, ceil, log
import cv2 as cv
from PyQt6 import QtWidgets
from matplotlib import pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, \
    QGraphicsPixmapItem,QVBoxLayout, QProgressBar, \
        QPushButton, QFileDialog , QLabel, QTextEdit, QMessageBox, QDialog
import sys
import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.image = None
        self.file_name = ''

        self.dst = None
        self.setWindowTitle('DIP')
        self.setGeometry(600, 250, 500, 500)

        self.button = QtWidgets.QPushButton(self)
        self.button.move(20, 20)
        self.button.setText("Sobel")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.Sobel)

        self.button = QtWidgets.QPushButton(self)
        self.button.move(20, 50)
        self.button.setText("Yolles")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.Yolles)

        self.button = QtWidgets.QPushButton(self)
        self.button.move(20, 80)
        self.button.setText("Prevvit")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.Prevvit)

        self.button = QtWidgets.QPushButton(self)
        self.button.move(20, 110)
        self.button.setText("Kirsh")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.Kirsh)

        self.button = QtWidgets.QPushButton(self)
        self.button.move(20, 180)
        self.button.setText("Histogram")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.GetHistogramm)

        self.button = QtWidgets.QPushButton(self)
        self.button.move(380, 0)
        self.button.setText("Close all windows")
        self.button.setFixedWidth(120)
        self.button.clicked.connect(self.CloseAllWindows)


        self.button = QtWidgets.QPushButton(self)
        self.button.move(380, 450)
        self.button.setText("Close app")
        self.button.setFixedWidth(120)
        self.button.clicked.connect(self.Exit)


        self.button = QtWidgets.QPushButton(self)
        self.button.move(200, 60)
        self.button.setText("Save image")
        self.button.setFixedWidth(120)
        self.button.clicked.connect(self.SaveImage)


        self.button = QtWidgets.QPushButton(self)
        self.button.move(200, 20)
        self.button.setText("Open Image")
        self.button.setFixedWidth(120)
        self.button.clicked.connect(self.getImage)


        self.progress = QProgressBar(self)
        self.progress.setGeometry(130, 440, 250, 20)

    def GetHistogramm(self):
        plt.close()
        fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2)


        ax1.hist(self.dst.ravel(), 256, [0, 256])
        # show the plotting graph of an image


        ax0.hist(self.image.ravel(), 256, [0, 256])
        # show the plotting graph of an image
        plt.show()

    def showDialog(self):
        QMessageBox.about(self, "Error", "Load image first")

    def SaveImage(self):

        if self.dst is None:
            self.showDialog()
            return

        self.file_name = QFileDialog.getSaveFileName(self, "Save image (*.png *.jpg)")
        if self.file_name[0] == '':
            return
        cv.imwrite(self.file_name[0], self.dst)
        QMessageBox.about(self, "Saving", "Success")

    def Exit(self):
        self.close()

    def getImage(self):
        self.file_name = QFileDialog.getOpenFileName(self, "Chose an image", None, "Image (*.png *.jpg)")[0]
        self.progress.setValue(0)
        if not self.file_name:
            return
        self.image = cv.imread(self.file_name)
        cv.namedWindow('Initial image', cv.WINDOW_AUTOSIZE)
        cv.moveWindow("Initial image", 30, 370)
        cv.imshow("Initial image", self.image)

        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)


    def CloseAllWindows(self):
        plt.close()
        self.progress.setValue(0)
        cv.destroyAllWindows()

    def Sobel(self):
        if self.image is None:
            self.showDialog()
            return
        self.progress.setValue(0)
        copy = self.image.copy()
        rows, cols = self.image.shape
        sobel_x = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]])

        sobel_y = np.array([[-1, -2, -1],
                            [0, 0, 0],
                            [1, 2, 1]])

        for x in range(1, rows - 1):
            self.progress.setValue(ceil((x + 1) * 100 / self.image.shape[0]))
            for y in range(1, cols - 2):
                pixel_x = abs((sobel_x[0][0] * self.image[x - 1, y - 1]) +
                              (sobel_x[0][2] * self.image[x - 1, y + 1]) +
                              (sobel_x[1][0] * self.image[x, y - 1]) +
                              (sobel_x[1][2] * self.image[x, y + 1]) +
                              (sobel_x[2][0] * self.image[x + 1, y - 1]) +
                              (sobel_x[2][2] * self.image[x + 1, y + 1]))

                pixel_y = abs((sobel_y[0][0] * self.image[x - 1, y - 1]) +
                              (sobel_y[0][1] * self.image[x - 1, y]) +
                              (sobel_y[0][2] * self.image[x, y + 1]) +
                              (sobel_y[2][0] * self.image[x + 1, y - 1]) +
                              (sobel_y[2][1] * self.image[x + 1, y]) +
                              (sobel_y[2][2] * self.image[x + 1, y + 1]))
                val = pixel_x + pixel_y
                if val > 255:
                    val = 255

                copy[x, y] = val
                self.dst = copy
        cv.namedWindow('Sobel', cv.WINDOW_AUTOSIZE)
        cv.moveWindow("Sobel", 1260, 370)
        cv.imshow("Sobel", copy)



    def Prevvit(self):
        if self.image is None:
            self.showDialog()
            return
        self.progress.setValue(0)
        copy = self.image.copy()
        rows, cols = self.image.shape
        prevvit_x = np.array([[-1, 0, 1],
                              [-1, 0, 1],
                              [-1, 0, 1]])

        prevvit_y = np.array([[-1, -1, -1],
                              [0, 0, 0],
                              [1, 1, 1]])

        for x in range(1, rows - 1):
            self.progress.setValue(ceil((x + 1) * 100 / self.image.shape[0]))
            for y in range(1, cols - 2):
                pixel_x = abs((prevvit_x[0][0] * self.image[x - 1, y - 1]) +
                              (prevvit_x[0][2] * self.image[x - 1, y + 1]) +
                              (prevvit_x[1][0] * self.image[x, y - 1]) +
                              (prevvit_x[1][2] * self.image[x, y + 1]) +
                              (prevvit_x[2][0] * self.image[x + 1, y - 1]) +
                              (prevvit_x[2][2] * self.image[x + 1, y + 1]))

                pixel_y = abs((prevvit_y[0][0] * self.image[x - 1, y - 1]) +
                              (prevvit_y[0][1] * self.image[x - 1, y]) +
                              (prevvit_y[0][2] * self.image[x, y + 1]) +
                              (prevvit_y[2][0] * self.image[x + 1, y - 1]) +
                              (prevvit_y[2][1] * self.image[x + 1, y]) +
                              (prevvit_y[2][2] * self.image[x + 1, y + 1]))

                val = pixel_x + pixel_y
                if val > 255:
                    val = 255
                copy[x, y] = val

        self.dst = copy


        cv.namedWindow('Prevvit', cv.WINDOW_AUTOSIZE)
        cv.moveWindow("Prevvit", 1260, 370)
        cv.imshow("Prevvit", copy)

    def KirshHelper(self, kirsh, x, y):
        pixel = abs((kirsh[0][0] * self.image[x - 1, y - 1]) +
                    (kirsh[0][1] * self.image[x - 1, y + 1]) +
                    (kirsh[0][2] * self.image[x - 1, y + 1]) +
                    (kirsh[1][0] * self.image[x, y - 1]) +
                    (kirsh[1][2] * self.image[x, y + 1]) +
                    (kirsh[2][0] * self.image[x + 1, y - 1]) +
                    (kirsh[2][1] * self.image[x + 1, y]) +
                    (kirsh[2][2] * self.image[x + 1, y + 1]))
        return pixel

    def Kirsh(self):
        if self.image is None:
            self.showDialog()
            return
        self.progress.setValue(0)
        copy = self.image.copy()
        rows, cols = self.image.shape

        img1 = copy
        img2 = copy
        img3 = copy
        img4 = copy
        img5 = copy
        img6 = copy
        img7 = copy
        img8 = copy

        for x in range(1, rows - 1):
            self.progress.setValue(ceil((x + 1) * 100 / self.image.shape[0]))
            for y in range(1, cols - 2):

                r = list()

                kirsh = np.array([[5, 5, 5],
                                  [-3, 0, -3],
                                  [-3, -3, -3]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img1[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[-3, 5, 5],
                                  [-3, 0, 5],
                                  [-3, -3, -3]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img2[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[-3, -3, 5],
                                  [-3, 0, 5],
                                  [-3, -3, 5]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img3[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[-3, -3, -3],
                                  [-3, 0, 5],
                                  [-3, 5, 5]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img4[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[-3, -3, -3],
                                  [-3, 0, -3],
                                  [5, 5, 5]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img5[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[-3, -3, -3],
                                  [5, 0, -3],
                                  [5, 5, -3]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img6[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[5, -3, -3],
                                  [5, 0, -3],
                                  [5, -3, -3]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255
                img7[x, y] = pixel
                r.append(pixel)


                kirsh = np.array([[5, 5, -3],
                                  [5, 0, -3],
                                  [-3, -3, -3]])
                pixel = self.KirshHelper(kirsh, x, y)
                if pixel > 255:
                    pixel = 255

                img8[x, y] = pixel
                r.append(pixel)
                if __name__ == '__main__':
                    pixel = max(r)
                if pixel > 255:
                    pixel = 255
                if pixel == 255:
                    pixel = 0
                copy[x,y] = pixel




        self.dst = img1
        cv.namedWindow('Kirsh', cv.WINDOW_AUTOSIZE)
        cv.moveWindow("Kirsh", 1260, 370)
        cv.imshow("Kirsh", img1)
        cv.imshow("Kirsh2", img2)
        cv.imshow("Kirsh3", img3)
        cv.imshow("Kirsh4", img4)
        cv.imshow("Kirsh5", img5)
        cv.imshow("Kirsh6", img6)
        cv.imshow("Kirsh7", img7)
        cv.imshow("Kirsh8", img8)
        cv.imshow("Kirsh9", copy)

    def Yolles(self):
        if self.image is None:
            self.showDialog()
            return
        self.progress.setValue(0)
        copy = self.image.copy()
        rows, cols = self.image.shape
        C_Norm = 112
        for x in range(1, rows - 1):
            self.progress.setValue(ceil((x + 1) * 100 / self.image.shape[0]))
            for y in range(1, cols - 2):
                if int(self.image[x, y]) == 0 or int(self.image[x - 1, y]) == 0 or int(self.image[x + 1, y]) == 0 or int(
                        self.image[x, y - 1]) == 0 or int(self.image[x, y + 1]) == 0:
                    continue
                val = C_Norm * abs(log(
                    abs(pow(self.image[x, y], 4) / self.image[x - 1, y] / self.image[x, y - 1] / self.image[x + 1, y] / self.image[x, y + 1])))

                if val > 255:
                    val = 255
                copy[x, y] = val
        self.dst = copy
        cv.namedWindow('Yolles', cv.WINDOW_AUTOSIZE)
        cv.moveWindow("Yolles", 1260, 370)
        cv.imshow("Yolles", copy)



def init():
    applicaton = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(applicaton.exec())

if __name__ == '__main__':
    init()
