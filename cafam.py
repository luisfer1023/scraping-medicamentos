from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def configurar_navegador(headless=False):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extraer_producto(driver, url):
    """
    Mete directamente a la URL del producto y extrae nombre y precio.
    """
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Esperar nombre visible – depende del selector real
        nombre = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1, .product-title, .dfd-product-title, .dfd-card-title")
        )).text.strip()

        # Esperar precio – depende del selector real
        precio = None
        try:
            # selector común del precio
            precio = driver.find_element(By.CSS_SELECTOR, "span[data-dfd-attribute='price'], .price, .product-price").text.strip()
        except:
            pass

        if not precio:
            # como respaldo, buscar el primer texto con “$” en los spans
            spans = driver.find_elements(By.TAG_NAME, "span")
            for sp in spans:
                txt = sp.text.strip()
                if txt and "$" in txt:
                    precio = txt
                    break

        return {
            "nombre": nombre,
            "precio": precio
        }

    except Exception as e:
        print("Error al extraer producto:", e)
        return None

if __name__ == "__main__":
    url = "https://www.drogueriascafam.com.co/medicamentos/13853-comprar-en-cafam-amoxidal-500-mg-caja-con-30-capsulas-precio-7703281002741.html"
    driver = configurar_navegador(headless=False)
    try:
        resultado = extraer_producto(driver, url)
        if resultado:
            print("Nombre:", resultado["nombre"])
            print("Precio:", resultado["precio"])
        else:
            print("No se pudo extraer el producto.")
    finally:
        time.sleep(2)
        driver.quit()


