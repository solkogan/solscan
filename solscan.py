import sys
import subprocess
# Импортируем наш интерфейс
from mainwindow import *
from PyQt5 import QtCore, QtGui, QtWidgets

def undotIPv4 (dotted):
    return sum (int (octet) << ( (3 - i) << 3) for i, octet in enumerate (dotted.split ('.') ) )

def dotIPv4 (addr):
    return '.'.join (str (addr >> off & 0xff) for off in (24, 16, 8, 0) )

def rangeIPv4 (start, stop):
    for addr in range (undotIPv4 (start), undotIPv4 (stop) ):
        yield dotIPv4 (addr)

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit.setText('37.151.22.0 - 37.151.22.255')
        self.ui.textEdit.setText('Этот ебучий сканер не уведомляет тебя о ходе процесса сканирования, поэтому просто укажи в поле ввода начальный и конечный IP диапазона через тире, а потом сиди и жди пока не откроется браузер :)')
        # Здесь прописываем событие нажатия на кнопку Scan                   
        self.ui.pushButton.clicked.connect(self.scanips)

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
        subprocess.call('masscan -p80,21 -iL masin.txt --rate=300 -oL masout.txt', shell=True)
        subprocess.call('awk \'{ print $4 }\' masout.txt > nmapin.txt', shell=True)
        subprocess.call('nmap -p 80,21 --script "http-title","ftp-anon" -iL nmapin.txt -oN output.txt', shell=True)
        self.ui.textEdit.setText('И наконец последний этап - парсинг результатов. Ждем...')
        subprocess.call('python3 nparse.py', shell=True)
        
        
        

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
