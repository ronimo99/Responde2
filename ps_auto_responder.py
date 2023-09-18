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
        

    def responde1(self): # manera 1, una mierda
        input_busqueda = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div[2]/label/input")
        input_busqueda.send_keys("42020") # hay que pasarle parametro luego
        ticket = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/table/tbody/tr/td[1]/a")
        url_ticket = ticket.get_attribute("href")
        # basta

    # prerequisitos: necesita un numero de ticket que exista de la plataforma de tickets y un tipo que puede no estar especificado, para respuestas automáticas de tickets habituales
    def responde2(self, numero_ticket, tipo=None):
        # inicializamos variables
        print("Limpiamos la solicitud anterior.")
        self.solicitud = ""

        # cambiamos de pestaña a la del ticket
        print("Se cambia a la pestaña a la del ticket.")
        self.driver.switch_to.new_window("tab")
        self.driver.get("https://soporteproservice.nexe.com/tickets/" + str(numero_ticket))
        print("Cambiando a la pestaña del ticket.")

        # asunto del correo de respuesta
        print("Se copia el asunto del ticket.")
        asunto = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[1]/h1")
        self.asunto = asunto.text
        print("Copiado el asunto.")

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

        # volvemos a gmail
        self.driver.switch_to.window(self.gmail_tab)
        # boton redactar
        self.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div").click()
        sleep(1)
        # boton redactar(x2), es necesario para que funcione no se porqué
        #self.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div/div[2]/div[2]/div[1]/div[1]/div/div").click()

        # esperamos hasta que todos los elementos del correo hayan cargado (gmail de mierda)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR , ".agP.aFw")))
        except:
            print("Algo ha salido mal en la espera del correo en blanco.")

        # redacta respuesta al correo
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
        if dt.datetime.today().hour < 13:
            solicitud_input.send_keys("Buenos días,\n")
        else:
            solicitud_input.send_keys("Buenas tardes,\n")

        solicitud_input.send_keys("Según solicitud:\n")
        solicitud_input.send_keys(self.solicitud + "\n")

        # templates de correo automáticas, según parámetro especificado en el comando
        if tipo:
            print("entramos en el switch de tipo: " + tipo)
            match tipo:
                case "Documentos":
                    solicitud_input.send_keys("Se ha desbloqueado el documento. \n")
                case "Stock":
                    solicitud_input.send_keys("Hay stock en: \n")
                case "Devoluciones":
                    solicitud_input.send_keys("No Supera el importe mínimo, con menos de X movimientos. \n")
                case "Entradas":
                    solicitud_input.send_keys("Se ha dado entrada, (X) líneas en total. \n")
                case "No Hay Ficheros":
                    solicitud_input.send_keys("Buenos días,\nNos podría indicar la situación actual y actuar según indicaciones:\n1. ¿Le han entrado los ficheros en este momento?\nSI. Infórmenos de la hora estimada de entrada del fichero\nNO. ¿Lo tiene facturado en ET2000?\nSI. Envíenos una captura de pantalla de ET2000 en la que se vea, el número de\npedido, la fecha, el estado y algunas referencias. Necesitaría también una\nimagen del albarán que trae el transportista con el material, en el que se vea\nel  número de boleto y las referencias de las piezas.\nNO. Contacte con su operador logístico y confirme si ha sido facturado. \n")
                case "Caso Qsac":
                    solicitud_input.send_keys("Se ha abierto incidente con Quiter")
                case "Caso Generix":
                    solicitud_input.send_keys("Se ha abierto incidente con SGA")
                case _:
                    print("Doesen't match any cases, skipping tipo.")
            print("Entramos en el if de tipo \"" + tipo + "\" y el switch ha funcionado.")

        # funciona, no lo cambiaré
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.DOWN)
        solicitud_input.send_keys(Keys.LEFT)
        solicitud_input.send_keys(Keys.LEFT)
        solicitud_input.send_keys(usuario_ps)

#bot = web_bot()
#bot.login_gmail()
#bot.login_ps()

"""
Desbloquear documentos:
bot.responde2(42135, "doc")
Consultas devoluciones:
bot.responde2(42146, "dev")
Consultas stock:
bot.responde2(42300, "stock")
Petición dar entradas:
bot.responde2(42135, "ent")

bot.responde2(42300)
"""