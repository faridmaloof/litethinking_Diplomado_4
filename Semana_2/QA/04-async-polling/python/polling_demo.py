import time

# Simulamos nuestra base de datos donde la orden está pendiente
base_de_datos = {"orden_123": "PENDIENTE"}


def simular_evento_kafka():
    # Simulamos que Kafka actualiza la orden después de 4 segundos
    print("Kafka: Procesando evento en background...")
    time.sleep(4)
    base_de_datos["orden_123"] = "CANCELADO"
    print("Kafka: ¡Evento procesado!")


# --- EL ANTI-PATRÓN (El QA Tradicional) ---
def prueba_tradicional_mala():
    print("\n--- PRUEBA MALA (Sleep) ---")
    print("Enviando petición de pago...")
    # Aquí fallaría si usamos time.sleep(2) porque Kafka tarda 4s.
    # Si usamos time.sleep(10), desperdiciamos 6 segundos valiosos.
    time.sleep(5)
    assert base_de_datos["orden_123"] == "CANCELADO"
    print("Prueba Mala: Exitosa, pero lenta/frágil.")


# --- LA SOLUCIÓN SDET (Active Polling) ---
def prueba_sdet_buena():
    print("\n--- PRUEBA SDET (Active Polling) ---")
    print("Enviando petición de pago...")

    timeout_maximo = 10  # Segundos
    intervalo = 0.5      # Preguntar cada medio segundo
    tiempo_transcurrido = 0

    while tiempo_transcurrido < timeout_maximo:
        estado_actual = base_de_datos["orden_123"]
        print(f"Polling: Revisando BD... Estado: {estado_actual}")

        if estado_actual == "CANCELADO":
            print("Prueba SDET: Exitosa! Validación rápida y sin desperdiciar tiempo.")
            return True

        time.sleep(intervalo)
        tiempo_transcurrido += intervalo

    print("Prueba SDET: Falló por Timeout.")
    return False


# Ejecución (Debes ejecutar esto en la terminal)
import threading

# Iniciamos el proceso asíncrono en background
hilo_kafka = threading.Thread(target=simular_evento_kafka)
hilo_kafka.start()

# Ejecutamos la prueba inteligente
prueba_sdet_buena()
