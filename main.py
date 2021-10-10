import sys

import requests
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QStackedWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QPen, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt

from utilities import DBConnection
from utilities.firatDao import FiratDao
from utilities import mailSender

from view.main_parsingPage import Ui_MainWindowParsing
from view.main_personWho import Ui_MainWindowPersonWho

from utilities.publishNumber import predict


class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("view/main_welcomPage.ui", self)

        self.img_firat = QLabel(self)
        self.img_firat.setGeometry(650, 10, 200, 100)
        pixmap = QPixmap('view/firat_logo.png')
        self.img_firat.setPixmap(pixmap)
        self.img_firat.resize(pixmap.width(), pixmap.height())
        self.ph_loginPage.clicked.connect(self.gotoLogin)
        self.ph_createAccountPage.clicked.connect(self.gotoCreateAccount)
        self.ph_who.clicked.connect(self.gotoWhoPage)


    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCreateAccount(self):
        createAccount = CreateAccountScreen()
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoWhoPage(self):
        whoPage = PublishScreen()
        widget.addWidget(whoPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("view/main_loginPage.ui", self)
        self.ph_login.clicked.connect(self.loginScreen)
        self.ln_passwd.setEchoMode(QLineEdit.Password)
        self.createAccount.clicked.connect(self.gotoCreateAccount)
        self.ph_back.clicked.connect(self.gotoWelcome)

    def loginScreen(self):
        db = DBConnection.DBConnection()
        check = db.login(email=self.ln_email.text(), passwd=self.ln_passwd.text())
        if (check):
            self.gotoParse()
        else:
            self.mesaj.setText("Kullanıcı Oluşturulmadı !!!")

    def gotoParse(self):
        parse = ParsingScreen()
        widget.addWidget(parse)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCreateAccount(self):
        createAccount = CreateAccountScreen()
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoWelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAccountScreen(QMainWindow):
    def __init__(self):
        super(CreateAccountScreen, self).__init__()
        loadUi("view/main_createAccountPage.ui", self)
        self.ph_create.clicked.connect(self.gotoVerificationCodeScreen)

        self.ln_passwd.setEchoMode(QLineEdit.Password)
        self.loginPage.clicked.connect(self.gotoLogin)
        self.ph_back.clicked.connect(self.gotoWelcome)

    def gotoVerificationCodeScreen(self):
        codeResult = mailSender.sendMail(self.ln_email.text())
        if (codeResult[0]):
            print("Mail Gönderildi")
            verificationCode = VerificationCodeScreen(firstname=self.ln_firstname.text(),
                                                      lastname=self.ln_lastname.text(),
                                                      email=self.ln_email.text(), passwd=self.ln_passwd.text(),
                                                      code=codeResult[1])
            widget.addWidget(verificationCode)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        else:
            print("Mail Gönderilemedi!!!")

    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoWelcome(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class VerificationCodeScreen(QMainWindow):
    def __init__(self, firstname, lastname, email, passwd, code):
        super(VerificationCodeScreen, self).__init__()
        loadUi("view/main_verificationPage.ui", self)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.passwd = passwd
        self.code = code
        print(code)
        self.ph_send.clicked.connect(self.verification)

    def verification(self):
        if (str(self.code) == str(self.ln_verificationCode.text())):
            db = DBConnection.DBConnection()
            db.createAccount(firstname=self.firstname, lastname=self.lastname, email=self.email, passwd=self.passwd)
            self.gotoLogin()
        else:
            self.mesaj.setText("Dogrulama Kodu Hatalı !!!")

    def gotoLogin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ParsingScreen(QMainWindow):
    def __init__(self):
        super(ParsingScreen, self).__init__()
        self.firatDao = FiratDao()
        self.domain = "https://abs.firat.edu.tr/"
        self.ui = Ui_MainWindowParsing()
        self.ui.setupUi(self)

        # self.ui.ph_difference =  QAction(QIcon("r3.png"), "Search", self) #*Butona ican ekleme
        # self.ui.ph_display.setIcon(QIcon("r3.png"))
        header = self.ui.tableAbs.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)

        header2 = self.ui.tableStaff.horizontalHeader()
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.ph_display.clicked.connect(self.display)
        self.comboboxBirimUpdate()

        self.ui.ph_errors.clicked.connect(self.errors)

        self.ui.cb_birim.currentIndexChanged.connect(self.updateBolum)
        self.updateBolum(self.ui.cb_birim.currentIndex())

        self.ui.ph_difference.clicked.connect(self.difference)

    def comboboxBirimUpdate(self):
        listDao = sorted(self.firatDao.getAbsAll())

        birimler = []
        for ls in listDao:
            tmp = ls[1]
            birimler.append(tmp)

        birimler = sorted(set(birimler))
        print(birimler)
        for br in birimler:
            bolumler = []
            for i in listDao:
                if i[1] == br:
                    tmp = i[0]
                    bolumler.append(tmp)
            self.ui.cb_birim.addItem(br, bolumler)

    def updateBolum(self, index):
        self.ui.cb_bolum.clear()
        bolumler = self.ui.cb_birim.itemData(index)
        if bolumler:
            self.ui.cb_bolum.addItems(bolumler)

    def display(self):
        self.ui.tableAbs.clear()
        self.ui.tableStaff.clear()
        self.ui.tableAbs.setRowCount(0)
        self.ui.tableStaff.setRowCount(0)

        birimName = str(self.ui.cb_birim.currentText())
        bolumName = str(self.ui.cb_bolum.currentText())

        if birimName == "Tıp Fakültesi" \
                or birimName == "Veteriner Fakültesi" \
                or birimName == "Diş Hekimliği Fakütesi" \
                or birimName == "Devlet Konservatuvarı" \
                or birimName == "Yabancı Diller Yüksekokulu":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Seçtiğiniz {} birimine ait öğretim görevlileri staff web sitesinde bölümler altında değil,"
                        " hepsi bir arada olacak şekilde bulunmaktadır. Bu yüzden yapılacak karşılaştırmalar, abs'deki seçilen bölüme ait"
                        " hocalar ile staff'taki tüm hocalar arasında gerçekleşmektedir.".format(birimName))
            msg.setWindowTitle("Warning")
            msg.exec_()

        resultAbs = self.firatDao.getAbs(bolumName, birimName)
        resultStaff = self.firatDao.getStaff(bolumName, birimName)
        if (len(resultStaff) < 1):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Staff servisinde {} 'bölümü bulunmamaktadır".format(bolumName))
            msg.setWindowTitle("Warning")
            msg.exec_()

        # Abs verileri tablosuna ekleniyor
        for row_number, row_data, in enumerate(resultAbs):
            self.ui.tableAbs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):

                if column_number == 4:
                    r = requests.get(self.domain + column_data, stream=True)
                    assert r.status_code == 200
                    img = QImage()
                    assert img.loadFromData(r.content)
                    w = QLabel()

                    w.setScaledContents(True)
                    w.setGeometry(QtCore.QRect(0, 0, 50, 50))
                    w.setPixmap(QPixmap.fromImage(img))

                    item = w
                    self.ui.tableAbs.setRowHeight(row_number, 100)
                    self.ui.tableAbs.setCellWidget(row_number, column_number, item)
                    # self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))
                else:
                    item = str(column_data)
                    self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))

        # Staff verileri tablosuna ekleniyor
        for row_number, row_data, in enumerate(resultStaff):
            self.ui.tableStaff.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = str(column_data)
                self.ui.tableStaff.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))

    def difference(self):
        self.ui.tableAbs.clear()
        self.ui.tableStaff.clear()
        self.ui.tableAbs.setRowCount(0)
        self.ui.tableStaff.setRowCount(0)

        birimName = str(self.ui.cb_birim.currentText())
        bolumName = str(self.ui.cb_bolum.currentText())

        resultAbs = self.firatDao.getAbs(bolumName, birimName)
        resultStaff = self.firatDao.getStaff(bolumName, birimName)

        dataAbs = self.findDifferencies(resultAbs, resultStaff)
        dataStaff = self.findDifferencies(resultStaff, resultAbs)

        # Abs verileri tablosuna ekleniyor
        for row_number, row_data, in enumerate(dataAbs):
            self.ui.tableAbs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                if column_number == 4:
                    r = requests.get(self.domain + column_data, stream=True)
                    assert r.status_code == 200
                    img = QImage()
                    assert img.loadFromData(r.content)
                    w = QLabel()

                    w.setScaledContents(True)
                    w.setGeometry(QtCore.QRect(0, 0, 50, 50))
                    w.setPixmap(QPixmap.fromImage(img))

                    item = w
                    self.ui.tableAbs.setRowHeight(row_number, 100)
                    self.ui.tableAbs.setCellWidget(row_number, column_number, item)
                else:
                    item = str(column_data)
                    self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))

        # Staff verileri tablosuna ekleniyor
        for row_number, row_data, in enumerate(dataStaff):
            self.ui.tableStaff.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                item = str(column_data)
                self.ui.tableStaff.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))

        #
        # db = DBConnection.DBConnection()
        # personelAbs = db.readPersonelAbs(bolum, birim)
        # personelStaff = db.readPersonelStaff(bolum)

    def errors(self):
        self.ui.tableAbs.clear()
        self.ui.tableStaff.clear()
        self.ui.tableAbs.setRowCount(0)
        self.ui.tableStaff.setRowCount(0)

        birimName = str(self.ui.cb_birim.currentText())
        bolumName = str(self.ui.cb_bolum.currentText())

        resultAbs = self.firatDao.getAbs(bolumName, birimName)
        resultStaff = self.firatDao.getStaff(bolumName, birimName)

        dataAbs = self.findErrors(resultAbs, resultStaff)

        for i in dataAbs:
            print("eros : " ,i)

        # Abs verileri tablosuna ekleniyor
        for row_number, row_data, in enumerate(dataAbs):
            self.ui.tableAbs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                if column_number == 4:
                    r = requests.get(self.domain + column_data, stream=True)
                    assert r.status_code == 200
                    img = QImage()
                    assert img.loadFromData(r.content)
                    w = QLabel()

                    w.setScaledContents(True)
                    w.setGeometry(QtCore.QRect(0, 0, 50, 50))
                    w.setPixmap(QPixmap.fromImage(img))

                    item = w
                    self.ui.tableAbs.setRowHeight(row_number, 100)
                    self.ui.tableAbs.setCellWidget(row_number, column_number, item)
                else:
                    item = str(column_data)
                    self.ui.tableAbs.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(item))



    def getItem(self, name, secondList):
        for i in secondList:
            if (i[2] == name):
                return i
        return None

    def isExist(self, x, name):
        return True if (x[2] == name) else False

    def findDifferencies(self, firstLilst, secondList):
        # verilen sıraya göre 1. listede olup ikincide olmayanları getirir
        responseList = []
        for i in firstLilst:
            sonuc = any(self.isExist(j, i[2]) for j in secondList)
            if (sonuc == False):
                responseList.append(i)
        return responseList

    def findErrors(self, firstList, secondList):
        result = []
        for i in firstList:
            errors = ""
            temp = self.getItem(i[2], secondList)
            if (temp != None):
                if (temp[0] != i[0]):
                    errors += "bölüm bilgisi uyuşmamaktadır; {} - {} ".format(i[0], temp[0])
                if (str(i[1]).__contains__(temp[1]) == False):
                    errors += "unvan bilgileri uyuşmamaktadır; {} - {}".format(i[1], temp[1])
                if (errors != ""):
                    tempList = list(i)
                    tempList[3] = errors
                    i = tuple(tempList)
                    print("find error : ",i)
                    result.append(i)
        return result


class PublishScreen(QMainWindow):
    def __init__(self):
        super(PublishScreen, self).__init__()
        self.ui = Ui_MainWindowPersonWho()
        self.ui.setupUi(self)
        self.ui.ph_who.clicked.connect(self.create_piechart)

    def create_piechart(self):
        a = self.ui.ln_uluslararasiMakale.text
        b = self.ui.ln_ulusalMakale.text
        c = self.ui.ln_bildiri.text
        d = self.ui.ln_kitap.text

        series = QPieSeries()
        who, skorfloat = predict(a, b, c, d)

        skor = int(str(skorfloat)[2:4])

        print("Who : -----------", who[0], skor)

        series.append(who[0], skor)
        series.append("", 100 - skor)

        # adding slice
        slice = QPieSlice()
        slice = series.slices()[0]
        slice.setExploded(True)
        slice.setLabelVisible(True)
        slice.setPen(QPen(Qt.darkGreen, 0))
        slice.setBrush(Qt.green)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Personel Ünvan Tahmin Oranı")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)
        # self.setCentralWidget(chartview)


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.setWindowTitle("Bilgi İşlem Daire Başkanlığı")
widget.addWidget(welcome)
widget.setFixedHeight(850)
widget.setFixedWidth(1550)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
