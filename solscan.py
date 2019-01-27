import sys
from mainwindow import *
from PyQt5 import QtCore, QtGui, QtWidgets
# Импортируем модуль threading для работы с потоками
import threading
from subprocess import Popen, PIPE, STDOUT

listen=''
outputtext=''

# Функции для сигналов между потоками
def signal_handler(signal, frame):
    global interrupted
    interrupted = True    
def interrupt_callback():
    global interrupted
    return interrupted

# Отдельная функция-заготовка для вынесения 
# последующих функций в отдельный поток
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

def undotIPv4 (dotted):
    return sum (int (octet) << ( (3 - i) << 3) for i, octet in enumerate (dotted.split ('.') ) )

def dotIPv4 (addr):
    return '.'.join (str (addr >> off & 0xff) for off in (24, 16, 8, 0) )

def rangeIPv4 (start, stop):
    for addr in range (undotIPv4 (start), undotIPv4 (stop) ):
        yield dotIPv4 (addr)

      

class MyWin(QtWidgets.QMainWindow):
    my_listen = QtCore.pyqtSignal(list, name='my_listen')
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        qss_file = open('style_file.qss').read()
        self.setStyleSheet(qss_file)
        self.ui.lineEdit.setText('37.151.22.0 - 37.151.22.255')
        # Здесь прописываем событие нажатия на кнопку Scan                   
        self.ui.pushButton.clicked.connect(self.scanips)
        global listen
        listen=self.my_listen
        self.my_listen.connect(self.mylisten, QtCore.Qt.QueuedConnection)

    @thread
    def gocommand(self):
        global listen
        p = Popen('masscan -p80,21 -iL masin.txt --rate=300 -oL masout.txt', stdout = PIPE, stderr = STDOUT, shell = True)
        while p.poll() is None:
            line = p.stdout.readline()
            listen.emit([line])
        p = Popen('awk \'{ print $4 }\' masout.txt > nmapin.txt', stdout = PIPE, stderr = STDOUT, shell = True)
        while p.poll() is None:
            line = p.stdout.readline()
            listen.emit([line])
        p = Popen('nmap -p 80,21 --script "http-title","ftp-anon" -iL nmapin.txt -oN output.txt', stdout = PIPE, stderr = STDOUT, shell = True)
        while p.poll() is None:
            line = p.stdout.readline()
            listen.emit([line])
        p = Popen('python3 nparse.py', stdout = PIPE, stderr = STDOUT, shell = True)
        while p.poll() is None:
            line = p.stdout.readline()
            listen.emit([line])

    # Функция которая выполняется при нажатии на кнопку Scan                 
    def scanips(self):
        # Получаем значения из строки ввода IP диапазона
        ips = self.ui.lineEdit.text()
        # Удаляем из строки с диапазоном пробелы
        ips=ips.replace(' ', '')
        # Делим строку по разделителю тире на начальный и конечный IP адреса
        ip = ips.split('-')
        # Объявляем массив в который поместим все IP из указанного диапазона
        ipmas=[]
        # В цикле помещаем в массив все IP из диапазона
        for x in rangeIPv4 (ip[0], ip[1]):
            ipmas.append(x)
        # Добавляем в массив последний IP с диапазона
        ipmas.append(ip[1])
        # Сохраняем список айпишек в файл
        f=open(u'masin.txt', 'w')
        for s in ipmas:
            f.write(s+'\n')
        f.close()
        self.gocommand()
    
    def mylisten(self, data):
        global outputtext
        t=str(data[0])
        t=t.replace('b\'\'','')
        t=t.replace('b\'','')
        t=t.replace('\\n\'','')
        t=t.replace('\\r','<br>')
        outputtext+='<br>'+t
        self.ui.textEdit.setText(outputtext)
        self.ui.textEdit.update()
        self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit.ensureCursorVisible()
       
        

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
