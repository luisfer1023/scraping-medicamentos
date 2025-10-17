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

# Solicitar medicamento
medicamento = input("¿Qué medicamento buscas?: ")

# Crear navegador
driver = configurar_navegador()

try:
    print("\nBuscando en La Rebaja Virtual...")
    
    driver.get("https://www.larebajavirtual.com/")
    time.sleep(5)
    
    # Buscar
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="buscando"]')
    search_box.send_keys(medicamento)
    search_box.send_keys(Keys.ENTER)
    
    time.sleep(7)
    
    # Extraer resultado
    productos = driver.find_elements(By.CSS_SELECTOR, 'div.vtex-search-result-3-x-galleryItem')
    
    if len(productos) > 0:
        producto = productos[0]
        nombre = producto.find_element(By.CSS_SELECTOR, 'span.vtex-product-summary-2-x-productBrand').text
        precio = producto.find_element(By.CSS_SELECTOR, 'span.vtex-product-price-1-x-sellingPriceValue').text
        
        print(f"\n Producto: {nombre}")
        print(f" Precio: {precio}")
    else:
        print("\n No se encontraron productos")
        
except Exception as e:
    print(f"\n Error: {e}")

driver.quit()