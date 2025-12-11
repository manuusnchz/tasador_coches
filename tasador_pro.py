import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os

# --- CONFIGURACIÓN ---
ARCHIVO_DB = 'BMW_116D_Simple.csv'

def entrenar_modelo():
    """Carga el CSV y entrena el cerebro de la IA"""
    if not os.path.exists(ARCHIVO_DB):
        print(f"❌ ERROR: No encuentro el archivo {ARCHIVO_DB}")
        print("   Ejecuta primero el script 'crear_db_simple.py' y mete al menos 5 coches.")
        return None

    try:
        df = pd.read_csv(ARCHIVO_DB)
    except pd.errors.EmptyDataError:
        print("❌ El archivo está vacío.")
        return None

    if len(df) < 5:
        print(f"⚠️  AVISO: Solo tienes {len(df)} coches guardados. La IA necesita más datos para ser precisa.")

    # 1. Definimos las columnas de entrada (X) y el objetivo (y)
    # Como ya guardamos 'es_automatico' como 0 o 1, no hace falta procesar texto.
    X = df[['año', 'kms', 'es_automatico']]
    y = df['precio']

    # 2. Entrenamos el algoritmo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    print(f"✅ Modelo entrenado con {len(df)} coches de tu base de datos.")
    return model

def solicitar_entero(mensaje):
    while True:
        try:
            valor = input(f"{mensaje}: ").strip()
            if not valor: continue
            return int(valor)
        except ValueError:
            print("❌ Introduce un número válido.")

def predecir_precio(model):
    print("\n--- NUEVA TASACIÓN ---")
    
    # 1. Pedimos datos
    año = solicitar_entero("Año")
    kms = solicitar_entero("Kilómetros")
    
    # Input rápido para transmisión
    es_auto_input = input("¿Es AUTOMÁTICO? (1=Sí / Enter=Manual): ").strip()
    es_auto = 1 if es_auto_input == '1' else 0

    # 2. Preparamos los datos para la IA
    # Deben tener el mismo formato que el archivo CSV: [año, kms, es_automatico]
    datos_coche = pd.DataFrame([[año, kms, es_auto]], columns=['año', 'kms', 'es_automatico'])

    # 3. Predicción
    precio_estimado = model.predict(datos_coche)[0]

    # Formateamos el precio para que se lea bien (ej. 12.500 €)
    print(f"\n==========================================")
    print(f"💰 VALOR JUSTO ESTIMADO: {precio_estimado:,.0f} €")
    print(f"==========================================")

    # 4. Análisis rápido de por qué ha dado ese precio
    importancias = model.feature_importances_
    # Mapeamos los valores a nombres legibles
    nombres = ['Año', 'Kilómetros', 'Transmisión']
    
    print("\n📊 Peso de cada factor en tu mercado actual:")
    for nombre, importancia in zip(nombres, importancias):
        # Convertimos a porcentaje (ej. 0.45 -> 45%)
        print(f"   - {nombre}: {importancia*100:.1f}%")

def main():
    print("==========================================")
    print("      CEREBRO TASADOR (BMW 116d)")
    print("==========================================\n")

    # 1. Cargar y Entrenar
    model = entrenar_modelo()

    if model:
        # 2. Bucle de predicción infinito
        while True:
            predecir_precio(model)
            
            if input("\n¿Tasar otro? (Enter=Sí, n=Salir): ").lower() == 'n':
                break

if __name__ == "__main__":
    main()