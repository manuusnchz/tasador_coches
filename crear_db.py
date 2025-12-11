import csv
import os

# --- CONFIGURACIÓN ---
ARCHIVO_OBJETIVO = 'BMW_116D_Simple.csv'

COLUMNAS = ['año', 'kms', 'es_automatico', 'precio']

def cargar_registros_existentes():
    """
    Lee el archivo CSV y carga los coches en memoria para comprobar duplicados.
    Devuelve un conjunto (set) de tuplas con formato texto.
    """
    registros = set()
    if os.path.exists(ARCHIVO_OBJETIVO):
        with open(ARCHIVO_OBJETIVO, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None) # Saltamos la cabecera
            for row in reader:
                if row: # Evitamos filas vacías
                    # Guardamos la fila exacta como una tupla (que es inmutable y rápida de buscar)
                    registros.add(tuple(row))
    return registros

def solicitar_entero(mensaje):
    while True:
        try:
            valor = input(f"{mensaje}: ").strip()
            if not valor: continue
            return int(valor)
        except ValueError:
            print("❌ Solo números, por favor.")

def solicitar_transmision():
    valor = input("¿Es AUTOMÁTICO? (1=Sí / Enter=Manual): ").strip()
    if valor == '1': return 1
    return 0 

def asegurar_archivo():
    if not os.path.exists(ARCHIVO_OBJETIVO):
        with open(ARCHIVO_OBJETIVO, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(COLUMNAS)
        print(f"🆕 Archivo {ARCHIVO_OBJETIVO} creado.")

def main():
    asegurar_archivo()
    
    # 1. Cargamos lo que ya existe en memoria
    coches_existentes = cargar_registros_existentes()
    print(f"📂 Base de datos cargada. Tienes {len(coches_existentes)} coches registrados.")
    
    print(f"==========================================")
    print(f"   RECOLECTOR SEGURO (Anti-Duplicados)")
    print(f"==========================================\n")

    while True:
        print("--- NUEVO COCHE ---")
        
        # Recogida de datos
        año = solicitar_entero("Año")
        kms = solicitar_entero("Kilómetros")
        es_auto = solicitar_transmision()
        precio = solicitar_entero("PRECIO (€)")
        
        # --- VERIFICACIÓN DE DUPLICADOS ---
        # Creamos una 'firma' del coche actual en formato texto (igual que el CSV)
        firma_coche = (str(año), str(kms), str(es_auto), str(precio))
        
        if firma_coche in coches_existentes:
            print("\n❌ ¡ALTO! ESTE COCHE YA ESTÁ EN LA LISTA.")
            print("   Se ha detectado un registro idéntico (mismo año, km, cambio y precio).")
            print("   👉 No se guardará para evitar ensuciar la IA.")
        else:
            # Si es nuevo, guardamos en Archivo y en Memoria
            with open(ARCHIVO_OBJETIVO, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(firma_coche)
            
            # Lo añadimos a la memoria por si intentas meter el mismo dos veces seguidas
            coches_existentes.add(firma_coche)
            
            tipo = "AUTO" if es_auto == 1 else "MANUAL"
            print(f"✅ Guardado: {año} | {kms}km | {tipo} | {precio}€")

        print("-" * 30)
        if input("¿Seguir? (Enter=Sí, n=Salir): ").lower() == 'n':
            break

if __name__ == "__main__":
    main()