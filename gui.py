import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox,
    QHBoxLayout, QVBoxLayout, QLineEdit, 
    QWidget, QPushButton, QListWidget, QComboBox
)
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Responde2")
    self.resize(QSize(600, 400))
    self.setWindowIcon(QIcon("icons\car--plus.png"))

    toolbar = QToolBar("Barra de tareas principal")
    toolbar.setIconSize(QSize(16, 16))
    self.addToolBar(toolbar)

    action_exit = QAction(QIcon("icons\cross.png"), "Salir", self)
    action_exit.setShortcut(QKeySequence("Ctrl+q"))
    action_exit.setStatusTip("Cerrar y salir del programa.")
    #action_exit.triggered.connect(self.exit)

    action_settings_button = QAction(QIcon("icons\cross.png"), "\"What you see is what you get.\"", self)
    action_settings_button.setStatusTip("No hay ajustes.")

    self.setStatusBar(QStatusBar(self))

    menu = self.menuBar()

    file_menu = menu.addMenu("Archivo")
    file_menu.addAction(action_exit)
    file_menu = menu.addMenu("Ajustes")
    file_menu.addAction(action_settings_button)

    layout_ticket_number = QHBoxLayout()
    layout_standard_tickets = QVBoxLayout()

    label_ticket_num = QLabel("Ticket a responder")

    input_ticket_num = QLineEdit()
    input_ticket_num.setMaxLength(10)
    input_ticket_num.setPlaceholderText("Número de ticket sin \"#\"")

    label_tipo = QLabel("Tipo de ticket standard:")

    list2_tipo = QComboBox()
    list2_tipo.addItems(["", "Documentos", "Devolución", "Stock", "Entradas incompletas"])

    list_tipo = QListWidget()
    list_tipo.addItems(["", "Documentos", "Devolución", "Stock", "Entradas incompletas"])


    button_ticket_num = QPushButton("Responder")

    #button_ticket_num.triggered.connect(self.llama_responde2)

    layout_standard_tickets.setContentsMargins(20, 20, 20, 20)
    layout_standard_tickets.setSpacing(5)

    layout_standard_tickets.addWidget(label_tipo)
    layout_standard_tickets.addWidget(list2_tipo)

    layout_ticket_number.setContentsMargins(50, 50, 50, 50)
    
    layout_ticket_number.addWidget(label_ticket_num)
    layout_ticket_number.addWidget(input_ticket_num)
    layout_ticket_number.addLayout(layout_standard_tickets)
    layout_ticket_number.addWidget(button_ticket_num)

    widget = QWidget()
    widget.setLayout(layout_ticket_number)
    self.setCentralWidget(widget)
  
  #def llama_responde2(self, numero_ticket, tipo):
    # aquí enlazas con la función de selenium

  def onMyToolBarButtonClick(self, s):
    print("click", s)

  #def exit():
    # aqui gestionaremos el cierre del webSocket y la gui

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()