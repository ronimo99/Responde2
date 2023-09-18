#!/usr/bin/env python
"""
2023 Robert Nieto Molina

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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

ps_user = None
ps_pass = None

class DialogCredentialsPS(QDialog):
  def __init__(self):
    super().__init__()
    super(DialogCredentialsPS, self).__init__()
    loadUi("dialog_proservice_credentials.ui", self)

    self.input_usuario_ps.textChanged.connect(self.user_entrado)
    self.input_pass_ps.textChanged.connect(self.pass_entrado)

  def user_entrado(self, text):
    global ps_user
    ps_user = text

  def pass_entrado(self, text):
    global ps_pass
    ps_pass = text

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
    global bot
    if self.num_ticket != 0:
      # real shit
      try:
        bot.responde2(self.num_ticket, str(self.tipo))
      except: print("Algo salió mal, intenta hacerlo bien la siguiente vez.")
    else: print("Respuesta no procesada, el ticket no es valido.")

  def ticket_input_entrado(self, text):
    self.num_ticket = text

  def tipo_selected(self):
    print("tipo: " + self.list_respuestas_tipicas.currentText())
    self.tipo = self.list_respuestas_tipicas.currentText()

  #btn_responder
  #list_respuestas_tipicas
  #input_ticket

  #Dialog credenciales ps
  # input_usuario_ps
  # input_pass_ps

# me obligan a hacer ésto antes del dialog
app = QApplication(sys.argv)

# abrimos dialog contraseña PS
dialog_ps = DialogCredentialsPS()
dialog_ps.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "car--exclamation.png")))
dialog_ps.exec()

# inicializamos el crawler
bot = ps.web_bot()
bot.login_gmail()
bot.login_ps(ps_user, ps_pass)

# abrimos la interfaz grafica
window = MainUI()
window.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "car--plus.png")))
window.show()
app.exec()