# **<u>Proservice Auto Template</u>**
## Crawler que crea respuestas automáticamente para los tickets de [soporteproservice.nexe.com](https://soporteproservice.nexe.com) para no tener que hacerlo tu.

### Dependencias necesárias:
* [Python 3](https://www.python.org/downloads/)
* [Selenium](https://www.selenium.dev/)
* [GeckoDriver](https://github.com/mozilla/geckodriver/)
* [Firefox](https://www.mozilla.org/en-US/firefox/new/)
* [Terminal del sistema](https://es.wikipedia.org/wiki/Terminal_(inform%C3%A1tica))
* Windows actualizado

### Instalación
Se necesita:
 * [Python 3](https://www.python.org/downloads/) o una version mayor en el equipo. Se puede descargar directamente de su web. En la instalación aceptar checkbox añadir en el PATH y en el final de la instalación darle a la opción del PATH variable lenght.
 * [GeckoDriver](https://github.com/mozilla/geckodriver/), se puede descargar desde [su Github](https://github.com/mozilla/geckodriver/releases). Hace falta descargar la versión para el sistema operativo en uso y poner el driver en el PATH del sistema ([por ejemplo](https://stackoverflow.com/questions/42524114/how-to-install-geckodriver-on-a-windows-system)).
 * [Firefox](https://www.mozilla.org/en-US/firefox/new/) debe estar instalado en el equipo.
 * Selenium, para descargarlo hay que ejecutar el siguiente comando en la terminal:

        pip install -U selenium
 
 * Tener los permisos para poder ejecutar el programa desde una terminal.

### Uso
Hay que rellenar el archivo credenciales.py con las credenciales del usuario de [https://soporteproservice.nexe.com/login](https://soporteproservice.nexe.com/login) para que pueda acceder a la página.

2023 Robert Nieto Molina