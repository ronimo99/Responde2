import sys,  os
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout, QLineEdit, 
    QWidget, QPushButton, QListWidget, QComboBox,
    QDialog, 
)
from PyQt6.uic import loadUi
from PyQt6 import QtGui
from PyQt6.QtCore import QSize, Qt
import ps_auto_responder as ps
import ps_auto_responder as ps

basedir = os.path.dirname(__file__)

class MainUI(QMainWindow):
  
  num_ticket = 0
  tipo = ""

  def __init__(self):
    super(MainUI, self).__init__()
    loadUi("responde2.ui", self)

    self.btn_responder.clicked.connect(self.responde2)
    self.input_ticket.textChanged.connect(self.ticket_input_entrado)

    self.list_respuestas_tipicas.currentIndexChanged.connect(self.tipo_selected)

  def responde2(self):
    if self.num_ticket != 0:
      # real shit
      try:
        bot.responde2(self.num_ticket, str(self.tipo))
      except: print("Algo salió mal, intenta hacerlo bien la siguiente vez.")
    else: print("Respuesta no procesada, el ticket no es valido.")

  def ticket_input_entrado(self, s):
    self.num_ticket = s

  def tipo_selected(self):
    print("tipo: " + self.list_respuestas_tipicas.currentText())
    self.tipo = self.list_respuestas_tipicas.currentText()

  #btn_responder
  #list_respuestas_tipicas
  #input_ticket

  #Dialog credenciales ps
  # input_usuario_ps
  # input_pass_ps

# inicializamos el crawler
bot = ps.web_bot()
bot.login_gmail()
bot.login_ps()

# abrimos la interfaz grafica
app = QApplication(sys.argv)
window = MainUI()
window.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "car--plus.png")))
window.show()
app.exec()