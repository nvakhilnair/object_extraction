from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PIL
from PIL import Image
import os
import cv2
import numpy as np


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ObjectDetection(QWidget):
    def setupUi(self, ObjectDetection):
        ObjectDetection.setObjectName(_fromUtf8("ObjectDetection"))
        ObjectDetection.resize(768, 522)
        ObjectDetection.setAutoFillBackground(False)
        ObjectDetection.setStyleSheet(
            "QWidget#ObjectDetection {background-image: url('data/logo.png');background-repeat: no-repeat; background-position: top right;}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("data\icon.ico")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ObjectDetection.setWindowIcon(icon)
        self.Image1 = QtGui.QPushButton(ObjectDetection)
        self.Image1.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.Image1.setObjectName(_fromUtf8("Image1"))
        self.Image1.clicked.connect(self.open_image1)
        self.image2 = QtGui.QPushButton(ObjectDetection)
        self.image2.setGeometry(QtCore.QRect(20, 280, 75, 23))
        self.image2.setObjectName(_fromUtf8("image2"))
        self.image2.clicked.connect(self.open_image2) 
        self.graphicsView = QtGui.QGraphicsView(ObjectDetection)
        self.graphicsView.setGeometry(QtCore.QRect(130, 10, 321, 171))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView")) 
        self.graphicsView_2 = QtGui.QGraphicsView(ObjectDetection)
        self.graphicsView_2.setGeometry(QtCore.QRect(130, 270, 321, 192))
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.detect = QtGui.QPushButton(ObjectDetection)
        self.detect.setGeometry(QtCore.QRect(600, 200, 75, 23))
        self.detect.setObjectName(_fromUtf8("detect"))
        self.detect.clicked.connect(self.detection)
        self.saveoutput = QtGui.QPushButton(ObjectDetection)
        self.saveoutput.setGeometry(QtCore.QRect(580, 250, 111, 23))
        self.saveoutput.setObjectName(_fromUtf8("saveoutput"))
        self.saveoutput.clicked.connect(self.save_output)
        self.exit = QtGui.QPushButton(ObjectDetection)
        self.exit.setGeometry(QtCore.QRect(610, 440, 75, 23))
        self.exit.setObjectName(_fromUtf8("exit"))
        self.exit.clicked.connect(self.close_application)
        self.horizontalSlider = QtGui.QSlider(ObjectDetection)
        self.horizontalSlider.setGeometry(QtCore.QRect(220, 220, 160, 22))
        self.horizontalSlider.setMinimum(50)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setValue(70)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalSlider.valueChanged.connect(self.threshold_value)
        self.label = QtGui.QLabel(ObjectDetection)
        self.label.setGeometry(QtCore.QRect(20, 220, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.threshold_value = QtGui.QLabel(ObjectDetection)
        self.threshold_value.setGeometry(QtCore.QRect(280, 240, 46, 13))
        self.threshold_value.setObjectName(_fromUtf8("threshold_value"))

        self.retranslateUi(ObjectDetection)
        QtCore.QMetaObject.connectSlotsByName(ObjectDetection)

    def close_application(self):
        choice=QtGui.QMessageBox.question(self,'Exit',"Do You want to exit",
                                          QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice==QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def open_image1(self):
        global img_rgb, img_gray,path
        mname=QFileDialog.getOpenFileName(self, 'Open file', 
   'c:\\',"Image files (*.jpg *.png)")
        image12 = Image.open(mname)
        image12 = image12.resize((200, 200), Image.ANTIALIAS)
        image12.save("temp.png", "png")
        mscene = QGraphicsScene()
        mscene.addPixmap(QPixmap('temp.png'))
        self.graphicsView.setScene(mscene)
        os.remove("temp.png")
        img_rgb = cv2.imread(mname)
        path=mname
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    def open_image2(self):
        global template
        oname=QFileDialog.getOpenFileName(self, 'Open file', 
   'c:\\',"Image files (*.jpg *.png)")
        image12_ = Image.open(oname)
        image12_ = image12_.resize((100, 100), Image.ANTIALIAS)
        image12_.save("temp.png", "png")
        oscene = QGraphicsScene()
        oscene.addPixmap(QPixmap('temp.png'))
        self.graphicsView_2.setScene(oscene)
        os.remove("temp.png")
        template = cv2.imread(oname, 0)
        
        
    def detection(self):
        try:
            global template,img_gray,path,image13
            cv2.destroyAllWindows()
            img_rgb=cv2.imread(path)
            threshold =(self.horizontalSlider.value())*0.01
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(
                    img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
            image13 = Image.fromarray(img_rgb, mode='RGB')
            cv2.imshow('Detected', img_rgb)
        except:
            error=QtGui.QMessageBox.critical(self,'Error',"Please select the images properly")

    def save_output(self):
        try:
            global image13
            sname=QFileDialog.getSaveFileName(self, 'Save File', 
       'c:\\',"Image files (*.jpg *.png)")
            abs_path = os.path.abspath(sname)
            image13.save(abs_path)
        except:
            error=QtGui.QMessageBox.critical(self,'Error',"Please detect the image and click this")

    def threshold_value(self):
        text=str(self.horizontalSlider.value())
        self.threshold_value.setText(text)        


    def retranslateUi(self, ObjectDetection):
        ObjectDetection.setWindowTitle(_translate("ObjectDetection", "Object Detection", None))
        self.Image1.setText(_translate("ObjectDetection", "Select Image", None))
        self.image2.setText(_translate("ObjectDetection", "Select Image", None))
        self.detect.setText(_translate("ObjectDetection", "Detect", None))
        self.saveoutput.setText(_translate("ObjectDetection", "Save Output Image", None))
        self.exit.setText(_translate("ObjectDetection", "Exit", None))
        self.label.setText(_translate("ObjectDetection", "Select the threshold value", None))
        self.threshold_value.setText(_translate("ObjectDetection", "70", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ObjectDetection = QtGui.QDialog()
    ui = Ui_ObjectDetection()
    ui.setupUi(ObjectDetection)
    ObjectDetection.show()
    sys.exit(app.exec_())

