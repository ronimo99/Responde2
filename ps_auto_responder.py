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

import re # regex to parse mail

from time import sleep # self evident

import datetime as dt # to check time for the greetings in the mail

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# credentials, in a separate file for privacy and security reasons
from credenciales import usuario_ps
from credenciales import password_ps
from credenciales import usuario_gmail
from credenciales import password_gmail


class web_bot():

    # window handlers para cambiar el cliente de pestaña
    gmail_tab = ""
    ps_tab = ""
    ticket_tab = ""

    # info para la respuesta
    correo = ""
    asunto = ""
    solicitud = ""
    tipo_ticket = ""
    estado_ticket = ""

    def __init__(self):  # función de inicialización del bot
        # inicializamos el crawler
        self.driver = webdriver.Firefox()
        print("Web Driver inicializado.")
        self.driver.maximize_window()
        print("Pantalla maximizada.")
        
    def login_gmail(self): 
        self.driver.get("https://gmail.com")
        print("Entrando a https://gmail.com.")
        #  introduce el usuario
        input_usuario = self.driver.find_element(By.NAME, "identifier")
        input_usuario.send_keys(usuario_gmail)
        print("Usuario escrito en input.")
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
        print("Esperando 60 segundos para que se resuelva el captcha.")

        # entre user y password tienes 30 segundos para demostrar que no eres un bot rellenando el captcha
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.NAME, "Passwd")))
        sleep(1)

        # introduce la contraseña y entra en el correo
        input_password = self.driver.find_element(By.NAME, "Passwd")
        input_password.send_keys(password_gmail)
        print("Contraseña escrita en input.")
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
        self.gmail_tab = self.driver.current_window_handle
        print("Guardando el Window Handle de la pestaña.")
        
    def login_ps(self, user=None, password=None): 
        # loguea en la web de ticketing de soporte proservice
        global usuario_ps
        global password_ps
        if user: usuario_ps = user
        if password: password_ps = password
        self.driver.switch_to.new_window("tab")
        print("Abriendo pestaña nueva en https://soporteproservice.nexe.com/login.")
        self.driver.get("https://soporteproservice.nexe.com/login")
        input_usuario = self.driver.find_element(By.NAME, "usuario")
        input_usuario.send_keys(usuario_ps)
        print("Usuario escrito en input.")
        input_password = self.driver.find_element(By.NAME, "password")
        input_password.send_keys(password_ps)
        print("Contraseña escrita en input.")
        self.driver.find_element(By.NAME, "Enviar").click()

        # guarda el window_handle de la tab para poder cambiar de pestañas
        self.ps_tab = self.driver.current_window_handle
        print("Guardando el Window Handle de la pestaña.")

        # pulsa la opción para ver los tickets de todos los usuarios
        #resulta que la ventana de responder tickets interfiere con éste seleccionable así que fuera
        """
        usuarios = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/table/thead/tr[2]/th[5]/select")
        select = Select(usuarios)
        select.select_by_visible_text("")
        print("Cambiambiada la vista a \"todos los tickets\".")
        """

    # prerequisitos: necesita un numero de ticket que exista de la plataforma de tickets y un tipo que puede no estar especificado, para respuestas automáticas de tickets habituales
    def responde2(self, numero_ticket, tipo=None):
        # inicializamos variables
        print("Se limpian las variables.")
        self.solicitud = ""
        self.tipo_ticket = ""
        self.estado_ticket = ""

        if tipo:
            print("Se entra en el switch de variable tipo: " + tipo)
            match tipo:
                case "Documentos":
                    self.tipo_ticket = "Se ha desbloqueado el documento."
                    self.estado_ticket = "Resolt"
                case "Stock":
                    self.tipo_ticket = "Hay stock en:\n"
                    self.estado_ticket = "Resolt"
                case "Devoluciones":
                    self.tipo_ticket = "No Supera el importe mínimo, con menos de X movimientos."
                    self.estado_ticket = "Resolt"
                case "Entradas":
                    self.tipo_ticket = "Se ha dado entrada, (X) líneas en total."
                    self.estado_ticket = "Resolt"
                case "Caso Qsac":
                    self.tipo_ticket = "Se ha abierto incidente con Quiter"
                    self.estado_ticket = "En Curs"
                case "Caso Generix":
                    self.tipo_ticket = "Se ha abierto incidente con SGA"
                    self.estado_ticket = "En Curs"
                case "Contacto Telefonico":
                    self.tipo_ticket = "Pueden darnos un número de contacto directo para darselo"
                    self.estado_ticket = "En Curs"
                case "Creacion referencia":
                    self.tipo_ticket = "Se ha creado la referencia."
                    self.estado_ticket = "Resolt"
                case "Reseteo contraseñas":
                    self.tipo_ticket = "Hemos pedido que la reseteen, por favor no prueben de entrar con la antigua para no bloquear la nueva antes de tenerla, nos pondremos en contacto en cuanto la tengamos."
                    self.estado_ticket = "En Curs"
                case "No Hay Ficheros":
                    self.tipo_ticket = "Buenos días,\nNos podría indicar la situación actual y actuar según indicaciones:\n1. ¿Le han entrado los ficheros en este momento?\nSI. Infórmenos de la hora estimada de entrada del fichero\nNO. ¿Lo tiene facturado en ET2000?\nSI. Envíenos una captura de pantalla de ET2000 en la que se vea, el número de\npedido, la fecha, el estado y algunas referencias. Necesitaría también una\nimagen del albarán que trae el transportista con el material, en el que se vea\nel  número de boleto y las referencias de las piezas.\nNO. Contacte con su operador logístico y confirme si ha sido facturado.\n"
                    self.estado_ticket = "En Curs"
                case _:
                    print("No hay matches, saltando tipo.")

        # cambiamos de pestaña a la del ticket
        print("Se cambia a la pestaña a la del ticket.")
        self.driver.switch_to.new_window("tab")
        self.driver.get("https://soporteproservice.nexe.com/tickets/" + str(numero_ticket))

        # asunto del correo de respuesta
        print("Se copia el asunto del ticket.")
        asunto = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[1]/h1")
        self.asunto = asunto.text

        # solicitud, hay que buscar todas las líneas <p>
        print("Se copia la solicitud.")
        for n in range(1, 20):
            try:
                solicitud = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[1]/p[" + str(n) + "]")
                if solicitud.text != " ":
                    self.solicitud += solicitud.text
                    self.solicitud += "\n"
            except:
                break
        
        # correo
        correo = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[1]/div[4]/div[4]/b[9]")
        # regex para parsear el correo de la string con el contacto
        aux = re.search("((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])", correo.text)
        self.correo = aux.group()
        
        if tipo:
            print("Existe tipo, se escribe la actualización del ticket predeterminada")
            print("Se rellena la info en actualización del ticket")
            self.driver.find_element(By.ID, "botonactualizarticekt").click() # "ticekt" el typo es de Jero
        
            print("Se añaden las horas")
            campo_horas = self.driver.find_element(By.ID, "ticketminhores")
            campo_horas.send_keys("15")

            print("Se añade la info de actualización")
            campo_titol = self.driver.find_element(By.ID, "subtitolticket")
            campo_titol.send_keys(tipo)

            print("Se añade la info de actualización")
            campo_titol = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[2]/form/div/div[2]/div[2]/div[5]/div[2]")
            campo_titol.send_keys(self.tipo_ticket)
            
            print("Se selecciona el estado")
            campo_estado = self.driver.find_element(By.ID, "estadosactualizar")
            select = Select(campo_estado)
            select.select_by_visible_text(self.estado_ticket)
            
            print("Se selecciona el tipo de actuación")
            campo_actuacio = self.driver.find_element(By.ID, "ticketactuacio" )
            select = Select(campo_actuacio)
            select.select_by_visible_text("Email")
            
            try:
                print("Se asigna el ticket al usuario actual")
                campo_asignado = self.driver.find_element(By.ID, "ticketassignado")
                select = Select(campo_asignado)
                select.select_by_visible_text(usuario_ps)
            except:
                print("Ya estaba el usuario asignado.")

        # volvemos a gmail
        print("Se cambia a la pestaña de Gmail")
        self.driver.switch_to.window(self.gmail_tab)
        # boton redactar
        self.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div").click()
        sleep(1)
        # boton redactar(x2), es necesario para que funcione no se porqué
        # self.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div").click()

        # esperamos hasta que todos los elementos del correo hayan cargado (gmail de mierda)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR , ".agP.aFw")))
        except:
            print("Algo ha salido mal en la espera del correo en blanco.")

        # redacta respuesta al correo
        print("Se escribe la info en los campos del correo correspondientes.")
        self.driver.find_element(By.CSS_SELECTOR, ".agP.aFw").click()
        correo_input = self.driver.find_element(By.CSS_SELECTOR, ".agP.aFw")
        correo_input.send_keys(self.correo)
        asunto_input = self.driver.find_element(By.NAME, "subjectbox")
        asunto_input.send_keys(self.asunto)
        self.driver.find_element(By.CSS_SELECTOR, ".Am.Al.editable.LW-avf.tS-tW").click();
        solicitud_input = self.driver.find_element(By.CSS_SELECTOR, ".Am.Al.editable.LW-avf.tS-tW")

        # para volver a la cabeza del cuerpo del mensaje
        for n in range(20):
            solicitud_input.send_keys(Keys.UP)
        
        # antes de las 13:00h responde con "buenos días", después responde "buenas tardes"
        print("Se escribe el buenos días/tardes.")
        if dt.datetime.today().hour < 13:
            solicitud_input.send_keys("Buenos días,\n")
        else:
            solicitud_input.send_keys("Buenas tardes,\n")

        solicitud_input.send_keys("Según solicitud:\n")
        solicitud_input.send_keys(self.solicitud + "\n")
        print("Se escribe la respuesta predeterminada al ticket.")
        solicitud_input.send_keys(self.tipo_ticket)        

        # funciona, no lo cambiaré lmao
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.LEFT)
        solicitud_input.send_keys(Keys.LEFT)
        solicitud_input.send_keys(usuario_ps)