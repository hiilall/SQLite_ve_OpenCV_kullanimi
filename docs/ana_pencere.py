# Hilal - 3.23.22

# import system module and os module
import sys
import os

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
# import Opencv module
import cv2
from ui_MainWindow import *

# import sqlite modul for database
import sqlite3

class AnaPencere(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):

        super(AnaPencere, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.baglanti_olustur()
        self.ui.setupUi(self)            

        #start page
        self.ui.stackedWidget.setCurrentWidget(self.ui.pageAnaSayfa)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set pushButtonBaslat callback clicked  function
        self.ui.pushButtonBaslat.clicked.connect(self.controlTimer)



        self.ui.radioButtonGiris.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageKullaniciGirisi))
        self.ui.radioButtonEkle.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageEkleSil))
        
        self.ui.radioButtonKamera.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageKamera))

        self.ui.radioButtonAnaSayfaG.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageAnaSayfa))
        self.ui.radioButtonAnaSayfaE.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageAnaSayfa))
        self.ui.radioButtonAnaSayfaS.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageAnaSayfa))
        self.ui.radioButtonAnaSayfaK.clicked.connect(lambda : self.ui.stackedWidget.setCurrentWidget(self.ui.pageAnaSayfa))

        # save user info
        self.ui.pushButtonGiris.clicked.connect(self.login)
        self.ui.pushButtonTemizleG.clicked.connect(self.clear)
        self.ui.pushButtonKayit.clicked.connect(self.register)
        self.ui.pushButtonTemizleE.clicked.connect(self.clear)
        self.ui.pushButtonSil.clicked.connect(self.delete)
        self.ui.pushButtonTemizleS.clicked.connect(self.clear)

        # find to sehir_list in lineEditSehir
        self.ui.lineEditSehir.textChanged.connect(self.lineEditSehir_change)
        # selection by press enter
        self.ui.lineEditSehir.returnPressed.connect(self.lineEditSehir_choose)
        # comboBoxSehir içine şehirleri ekleyeceğiz
        self.ui.comboBoxSehir.addItem("Seçiniz..")
        self.sehir_list = ["ankara","antalya","istanbul","izmir", "kastamonu","kocaeli","konya"]
        self.ui.comboBoxSehir.addItems(self.sehir_list)
        # setting max number visible limit
        self.ui.comboBoxSehir.setMaxVisibleItems(5)
        self.ui.lineEditSehir.inputRejected.connect(self.ui.comboBoxSehir.showPopup)

        # print active index to lineEditSehir
        self.ui.comboBoxSehir.activated["int"].connect(self.sehir)

    def sehir(self,activated_index):
        self.ui.lineEditSehir.setText(self.ui.comboBoxSehir.itemText(activated_index))

    # find to sehir_list in lineEditSehir function
    def lineEditSehir_change(self):
        text = self.ui.lineEditSehir.text()
        self.ui.comboBoxSehir.showPopup()
        self.ui.comboBoxSehir.setMaxVisibleItems(5)
        self.matching = [s for s in self.sehir_list if text in s]
        self.ui.comboBoxSehir.clear()
        self.ui.comboBoxSehir.addItems(self.matching)

    # selection by press enter function
    def lineEditSehir_choose(self):
        secilen_sehir = self.matching[0]
        self.ui.lineEditSehir.setText(secilen_sehir)
    
    # camera information message - QMesaageBox
    def uyari(self):
        result = QMessageBox.critical(self,"Uyarı", "Kamera Yönlendirmesi ")
 
        if result == 1024: # click to Yes button
            myMessageBox = QMessageBox()    # define own message box from QMessageBox class 
            myMessageBox.setWindowTitle("Kamera Onay")
            myMessageBox.setText("Kamrea ile Doğrulama Yöntemine Yönlendiriliyorsunuz...")
            myMessageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            myMessageBox.setEscapeButton(QMessageBox.No)     

            buttonOnay = myMessageBox.button(QMessageBox.Yes)
            buttonOnay.setText("Onayla")
            buttonIptal = myMessageBox.button(QMessageBox.No)
            buttonIptal.setText("İptal Et")

            result_2 = myMessageBox.exec()      # run the myMessageBox 
            if result_2 ==  16384:              # result return and write QMessageBox.Yes value
                self.ui.pageAnaSayfa.close()
                self.ui.pageKamera.show()

            elif result_2 == QMessageBox.No:    # used QMessageBox.No instead of 65536 (QMessageBox.No value)
                self.ui.pageAnaSayfa.show()
    # connect to database
    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("database_kullanici.db")

        self.cursor = self.baglanti.cursor()
        self.cursor.execute("Create table If not exists Calisanlar (Kullanici Adi TEXT, Parola TEXT, Şube TEXT)")
        self.baglanti.commit()

    def login(self):
        secenek = self.ui.radioButtonGiris.isChecked()
        if secenek == True:
            adi = self.ui.lineEditKullaniciAd.text()
            parola = self.ui.lineEditKullaniciParola.text()
            # compare input values (kullanici adi and parola) ​​with info in database (database_kullanici)
            self.cursor.execute("Select * From Calisanlar where Kullanici = ? and Parola = ? ;", (adi, parola))
            # sorgudan dönen değeleri alma / getting the values returned from the query
            data = self.cursor.fetchall()          #liste dönüyor
            if len(data) == 0:
                self.ui.labelGiris.setText("Kullanıcı bilgileri eşleşmedi... \n Lütfen tekrar deneyin...")
         
            else:
                self.ui.labelGiris.setText("Hoşgeldiniz, eşleşme başarılı")
        else:
            self.ui.labelGiris.setWindowIcon(QIcon("icon/loupe.png"))
            self.ui.labelGiris.setText("Lütfen bir seçim yapınız")

    # register          
    def register(self):
        # confirmation for registration
        secenek = self.ui.radioButtonEkle.isChecked()
        if secenek == True:
            onay = self.ui.checkBoxKayitOnay.isChecked()
            if onay == True:
                yeni_ad = self.ui.lineEditKullaniciAdE.text()
                yeni_parola = self.ui.lineEditKullaniciParolaE.text()    
                sehir = self.ui.lineEditSehir.text()     
                if yeni_ad != "" and yeni_parola != "":

                    self.cursor.execute("Insert into Calisanlar Values (?,?,?)",(yeni_ad,yeni_parola,sehir))
                    self.baglanti.commit()
                    if self.cursor.rowcount:
                        self.ui.labelEkle.setText("Başarılı")
                else: 
                    self.ui.labelEkle.setText("Veri kaydedilemedi")

            else :
                self.ui.labelEkle.setText("Lütfen onaylama işlemini yapınız")
        else:
            self.ui.labelEkle.setText("Lütfen bir seçim yapınız")

    # kullanıcı Silme
    def delete(self):
        secenek = self.ui.radioButtonEkle.isChecked()
        if secenek == True:
            silinecek_ad = self.ui.lineEditKullaniciAdS.text()
            silinecek_parola = self.ui.lineEditKullaniciParolaS.text()
            self.cursor.execute("Delete from Calisanlar where Kullanici=? and Parola = ?",(silinecek_ad,silinecek_parola))
            self.baglanti.commit()
            if self.cursor.rowcount:
                self.ui.labelSil.setText("Silme işlemi başarılı")

    # clear
    def clear(self):
        self.ui.lineEditKullaniciAd.clear()
        self.ui.lineEditKullaniciParola.clear()
        self.ui.lineEditKullaniciAdE.clear()
        self.ui.lineEditKullaniciParolaE.clear()
        self.ui.lineEditSehir.clear()
        self.ui.lineEditKullaniciAdS.clear()
        self.ui.lineEditKullaniciParolaS.clear()

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #yuz tanima icin cascade ekleniyor
        self.frame_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.frame_rect = self.frame_cascade.detectMultiScale(image, minNeighbors = 7)

        for (x,y,w,h) in self.frame_rect:
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,150), 7)

        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_labelKamera.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(1)
            # update pushButtonBaslat text
            self.ui.pushButtonBaslat.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update pushButtonBaslat text
            self.ui.pushButtonBaslat.setText("Start")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow +icon

    mainWindow = AnaPencere()
    mainWindow.setWindowIcon(QIcon("icon/operating-system.png"))
    mainWindow.setWindowTitle("Kullanici Giris")
    mainWindow.show()

    sys.exit(app.exec_())