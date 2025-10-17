from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def configurar_navegador():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

medicamento = input("¿Qué medicamento buscas?: ")
driver = configurar_navegador()

try:
    print("\nBuscando en Cruz Verde...")
    
    driver.get("https://www.cruzverde.com.co/")
    time.sleep(6)
    
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Buscar"]')
    search_box.send_keys(medicamento)
    search_box.send_keys(Keys.ENTER)
    
    time.sleep(10)  # Espera más tiempo para cargar
    
    # Buscar TODOS los elementos con texto
    todos_elementos = driver.find_elements(By.XPATH, "//*[contains(text(), '$')]")
    
    if len(todos_elementos) > 0:
        print(f"\n✓ Se encontraron {len(todos_elementos)} elementos con precios")
        
        # Mostrar los primeros 3 productos con precio
        for i, elemento in enumerate(todos_elementos[:3], 1):
            try:
                # Obtener el contenedor padre del producto
                producto_container = elemento.find_element(By.XPATH, "./ancestor::article | ./ancestor::div[contains(@class, 'product')]")
                
                # Extraer todo el texto
                texto_completo = producto_container.text
                lineas = texto_completo.split('\n')
                
                print(f"\n--- Producto {i} ---")
                for linea in lineas[:5]:  # Primeras 5 líneas
                    if linea.strip():
                        print(f"  {linea}")
            except:
                continue
    else:
        print("\n No se encontraron productos")
        
except Exception as e:
    print(f"\n Error: {e}")

driver.quit()
