import socket
from PyQt5 import QtWidgets
from clientGui import Ui_MainWindow
import sys
import socket
import game
from PyQt5.Qt import QMessageBox
from game import Send
import threading
BUFFER_SIZE = 2 ** 10
import json

class MainClientWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainClientWindow, self).__init__()
        self.port = 9095
        self.host = socket.gethostbyname(socket.gethostname())
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.send = Send()
        try:
            self.ui.pushButton.clicked.connect(self.pressButton)
        except Exception:
            print("Ошибка")

    def connectServer(self):
        try:
            self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientsocket.connect((self.host, self.port))
            self.clientsocket.sendall(self.send.marshal())
        except Exception:
            print("No connect")
        self.receive_worker = threading.Thread(target=self.receive)
        self.receive_worker.start()

    def receive(self):
        while True:
            try:
                self.inputSend = Send(**json.loads(self.receive_all()))
                self.ui.resultLabel.clear()
                self.ui.inputLabel.setText("Введите город")
                self.send.start = self.inputSend.start
                self.send.answer = self.inputSend.answer
                self.send.move = self.inputSend.move
                if self.inputSend.answer != None:
                    self.ui.resultLabel.setText(self.inputSend.getAnswer())
                    self.exit()
                    return
                if not self.inputSend.start:
                    self.ui.resultLabel.setText(self.inputSend.getStart())
                else:
                    if self.inputSend.move:
                        str = self.inputSend.getStart() + self.inputSend.getMove() + self.inputSend.getCity()
                    else:
                        str = self.inputSend.getMove()
                    self.ui.resultLabel.setText(str)
            except Exception:
                print("Не робит")
                return

    def receive_all(self):
        buffer = ""
        while not buffer.endswith(game.END_CHARACTER):
            buffer += self.clientsocket.recv(BUFFER_SIZE).decode(game.TARGET_ENCODING)
        print(buffer)
        return buffer[:-1]

    def sendSity(self):
        if not self.inputSend.start or not self.inputSend.move:
            return
        try:
            self.send.city = self.ui.lineEdit.text()
            self.clientsocket.sendall(self.send.marshal())
        except Exception:
            print("disconnect")
            self.exit()


    def pressButton(self):
        if self.ui.inputLabel.text() == "Username: " and self.ui.lineEdit.text() != "":
            self.username = self.ui.lineEdit.text()
            self.ui.resultLabel.setText("Имя пользователя " + str(self.username))
            self.send.username = self.username
            self.connectServer()
        elif self.ui.lineEdit.text() == "":
            self.ui.resultLabel.clear()
            self.ui.resultLabel.setText("Вы ничего не ввели")
            return
        else:
            self.sendSity()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Выход", "Вы действительно хотите выйти?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.send.answer != None:
                event.accept()
            else:
                self.send.q = False
                self.clientsocket.sendall(self.send.marshal())
                event.accept()
                self.exit()
        else:
            event.ignore()

    def exit(self):
        self.clientsocket.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainClientWindow()
    application.show()
    sys.exit(app.exec())
