import os

try:
    os.system("python -m PyQt5.uic.pyuic -x MainWindow.ui -o ui_MainWindow.py")
    #☻os.system("pyrcc5 icons.qrc -o icons_rc.py")
except Exception as e:
    print(e)
    pass


#Siyah Beyaz resmi arayüzde gösterme

"""_, step = current_image.shape

            qImgResult = QtGui.QImage(current_image, current_image.shape[1], current_image.shape[0], step,
                                      QtGui.QImage.Format_Grayscale8)
            self.anapencere.labelImageSonuc.setPixmap(QPixmap.fromImage(qImgResult))"""