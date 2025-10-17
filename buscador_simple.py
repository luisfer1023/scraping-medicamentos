"""
Buscador Simple de Medicamentos
Importa y ejecuta cada script individual de farmacia
Ordena los resultados por precio de menor a mayor
"""

import importlib
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_navegador():
    """Configura y retorna el navegador"""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extraer_precio_numerico(texto_precio):
    """Convierte el texto del precio a número para ordenar"""
    if not texto_precio or texto_precio == "Sin precio":
        return float('inf')
    
    numeros = re.sub(r'[^\d,.]', '', texto_precio)
    numeros = numeros.replace('.', '').replace(',', '.')
    
    try:
        return float(numeros)
    except:
        return float('inf')

# ============================================
# PROGRAMA PRINCIPAL
# ============================================

print("\n" + "="*60)
print("       BUSCADOR DE PRECIOS DE MEDICAMENTOS")
print("="*60)

# Solicitar el medicamento
medicamento = input("\n¿Qué medicamento deseas buscar?: ")

# Configurar navegador (compartido para todas las farmacias)
print("\nConfigurando navegador...")
driver = configurar_navegador()

# Lista de módulos de farmacias
farmacias = [
    {'modulo': 'la_rebaja', 'funcion': 'buscar', 'nombre': 'La Rebaja Virtual'},
    {'modulo': 'pasteur', 'funcion': 'buscar', 'nombre': 'Pasteur'},
    {'modulo': 'cruz_verde', 'funcion': 'buscar', 'nombre': 'Cruz Verde'},
    {'modulo': 'cafam', 'funcion': 'buscar', 'nombre': 'Cafam'},
    {'modulo': 'farmatodo', 'funcion': 'buscar', 'nombre': 'Farmatodo'},
    {'modulo': 'colsubsidio', 'funcion': 'buscar', 'nombre': 'Colsubsidio'}
]

resultados = []

try:
    for farmacia in farmacias:
        print("\n" + "="*50)
        print(f"Buscando en {farmacia['nombre'].upper()}")
        print("="*50)
        
        try:
            # Importar el módulo dinámicamente
            modulo = importlib.import_module(farmacia['modulo'])
            
            # Ejecutar la función buscar() del módulo
            if hasattr(modulo, farmacia['funcion']):
                funcion_buscar = getattr(modulo, farmacia['funcion'])
                resultado = funcion_buscar(driver, medicamento)
                
                if resultado:
                    resultados.append(resultado)
                    print(f"✓ Encontrado: {resultado['nombre']}")
                    print(f"✓ Precio: {resultado['precio']}")
                else:
                    print(f"✗ No se encontró en {farmacia['nombre']}")
            else:
                print(f"⚠️ El módulo {farmacia['modulo']} no tiene función 'buscar()'")
                
        except ModuleNotFoundError:
            print(f"⚠️ Archivo {farmacia['modulo']}.py no encontrado")
        except Exception as e:
            print(f"✗ Error en {farmacia['nombre']}: {str(e)[:80]}")
        
        import time
        time.sleep(2)

finally:
    # Cerrar navegador
    print("\n" + "="*60)
    print("Cerrando navegador...")
    driver.quit()
    print("✓ Navegador cerrado")

# ============================================
# PROCESAR Y MOSTRAR RESULTADOS
# ============================================

# Agregar precio numérico para ordenar
for resultado in resultados:
    resultado['precio_numerico'] = extraer_precio_numerico(resultado['precio'])

# Ordenar de MENOR a MAYOR precio
resultados.sort(key=lambda x: x['precio_numerico'])

# Mostrar resultados
print("\n" + "="*60)
print("           RESULTADOS ORDENADOS POR PRECIO")
print("           (De menor a mayor)")
print("="*60)

if len(resultados) > 0:
    for i, r in enumerate(resultados, 1):
        print(f"\n{i}. {r['farmacia'].upper()}")
        print(f"   Producto: {r['nombre']}")
        print(f"   Precio: {r['precio']}")
        print("   " + "-"*55)
    
    # Filtrar solo los que tienen precio válido
    con_precio = [r for r in resultados if r['precio_numerico'] != float('inf')]
    
    print(f"\n{'='*60}")
    print(f"✓ Total farmacias consultadas: {len(farmacias)}")
    print(f"✓ Farmacias con resultados: {len(resultados)}")
    print(f"✓ Farmacias con precio disponible: {len(con_precio)}")
    
    if con_precio:
        print(f"\n🏆 MEJOR PRECIO: {con_precio[0]['farmacia']} - {con_precio[0]['precio']}")
        
        if len(con_precio) > 1:
            ahorro = con_precio[-1]['precio_numerico'] - con_precio[0]['precio_numerico']
            print(f"💰 Ahorras: ${ahorro:,.0f} vs la más cara".replace(",", "."))
    
    print("="*60 + "\n")
else:
    print("\n✗ No se encontraron resultados en ninguna farmacia")
    print("="*60 + "\n")