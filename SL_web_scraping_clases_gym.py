# Codigo para hacer web scapring en gym https://maisqueauga.com/

# Importamos librerias
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import schedule

# Esto es para evitar conflictos del navegador
def get_driver():
    options=webdriver.ChromeOptions()
    options.add_argument("disable-inforbars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

# Definimos el driver de la web a la que haremos scraping (maisqueauga en mi caso).   
    driver=webdriver.Chrome(options=options)
    driver.get("https://maisqueauga.deporsite.net/login")
    return driver

# Criterios de reserva. En este caso entro con los criterios de la cosa que quiero ejecutar a una hora en específico. Si lo que se quiere es simplemente 
# extraer información, o ejecutar algo anytime, no es necesario definir la función ni entrar con estos criterios.
nombre_clase="Invicto"
dias_clase="Jueves"
xpath_clase="/html/body/div[5]/div[3]/div/div/div/div[3]/div/table[1]/tbody/tr[8]/td[5]/div"

def reserva_clase(nombre_clase, dias_clase, xpath_clase):
    
    # Nos autenticamos en la página
    driver=get_driver()
    driver.find_element(by="id", value="email").send_keys("email@gmail.com")
    driver.find_element(by="id", value="password").send_keys("Password" + Keys.RETURN)

    # Los siguientes pasos toca indicar al código en donde ir clickando, literal como si fuera un humano. ¿Çómo?. Con los xpath. Por ejemplo, le digo que 
    # entre a mi sede del gym, indicandole el path en donde tiene que hacer click. Los paths se miran directamente en el navegador. OJO, que pueden cambiar si actualizan la web. 
    driver.find_element(by="xpath", value="/html/body/div[4]/div[3]/div/div/div/div/div[3]/div[1]/a[3]").click()
    
    # Doy tiempo de espera y accedo a la clase - Tabla. (Caso especifico de esta web que tenía las clases en una clase tipo tabla).
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-clases")))
    
    # Seleccionar la clase con los parámetros de entrada en la función y doy click en "Reservar"
    driver.find_element(by="xpath", value=xpath_clase).click()
    time.sleep(2)

    #confirmo y doy tiempo de espera
    driver.find_element(by="xpath", value="/html/body/div[3]/div/div[2]/div[2]/a").click()
    time.sleep(2)

    # Espera larga para obtener la confirmación de la reserva y continúo el proceso de reserva, es todo igual, acá dejo de comentar esto.
    time.sleep(5)
    container_div = driver.find_element(by="class name", value="container")
    container_div.find_element(by="xpath", value="/html/body/div[4]/div[3]/div/div/div/section/div[3]/div[7]/div[4]/div/div[4]/div[1]/div[4]/div[2]").click()
    time.sleep(20)
    
    confirmacion_div = driver.find_element(by="class name", value="confirmacion-pago")
    confirmacion_fecha_reserva = confirmacion_div.find_element(by="xpath", value="/html/body/div[4]/div[3]/div/div/div/div[1]/div/div/div[6]/div[2]").text
    confirmacion_hora_reserva = confirmacion_div.find_element(by="xpath", value="/html/body/div[4]/div[3]/div/div/div/div[1]/div/div/div[7]/div[2]").text
    
    # Le digo que me imprima lo que he reservado.
    print("RESERVA HECHA:")
    print(nombre_clase)
    print(dias_clase)
    print("Fecha:", confirmacion_fecha_reserva)
    print("Hora:", confirmacion_hora_reserva)

# Programar la reserva para todos los días a las 20:00:05
schedule.every().day.at("22:00:05").do(reserva_clase, nombre_clase, dias_clase, xpath_clase)

# Ejecutar el programa de forma continua y dar espera.
while True:
    schedule.run_pending()
    time.sleep(5)
    
  
  