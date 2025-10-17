from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

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
    
    time.sleep(8)
    
    # Obtener TODAS las tarjetas de productos
    productos = driver.find_elements(By.CSS_SELECTOR, 'ml-card-product')
    
    if len(productos) > 1:
        # Seleccionar el SEGUNDO producto (índice 1)
        producto = productos[1]
        
        # Obtener nombre del segundo producto
        nombre = producto.find_element(By.CSS_SELECTOR, 'a[class*="font-open"] span.ng-star-inserted').text
        
        # Obtener precio del segundo producto
        precio = producto.find_element(By.CSS_SELECTOR, 'span.font-bold.text-prices').text
        
        print(f"\n Producto: {nombre}")
        print(f" Precio: {precio}")
    else:
        print(f"\n Solo se encontró {len(productos)} producto(s)")
        
except Exception as e:
    print(f"\n Error: {e}")

driver.quit()