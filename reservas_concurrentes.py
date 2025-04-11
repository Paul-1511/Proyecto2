import psycopg2
from psycopg2 import errors
import threading
import random
import time
from datetime import datetime
import sys

# Configuración de conexión
DB_CONFIG = {
    "dbname": "reservas",
    "user": "postgres",
    "password": "postgres123",
    "host": "localhost",
    "port": "5432",
    "connect_timeout": "3"
}

# Datos para la simulación
EVENT_ID = 1
# Simulación más realista con menos asientos
AVAILABLE_SEATS = range(1, 50)  # 49 asientos disponibles para un evento pequeño-mediano
NUM_USERS = [5, 10, 20, 30]  # Más usuarios intentando reservar simultáneamente
ISOLATION_LEVELS = [
    "READ COMMITTED",
    "REPEATABLE READ",
    "SERIALIZABLE"
]

# Variable para almacenar todos los resultados
global_results = []
# Añadimos un bloqueo para sincronizar el acceso a asientos seleccionados
seat_lock = threading.Lock()
selected_seats = set()

def print_results_table():
    """Imprime la tabla de resultados con el formato deseado"""
    print("\n")
    print("| {:^20} | {:^20} | {:^16} | {:^16} | {:^15} |".format(
        "Usuarios Concurrentes", "Nivel de Aislamiento", "Reservas Exitosas", "Reservas Fallidas", "Tiempo Promedio"
    ))
    print("|" + "-"*22 + "|" + "-"*22 + "|" + "-"*18 + "|" + "-"*18 + "|" + "-"*17 + "|")
    
    for result in global_results:
        num_users = result['num_users']
        isolation = result['isolation_level']
        successful = result['successful']
        failed = num_users - successful
        
        # Calcular tiempo promedio en ms para reservas exitosas
        avg_time_ms = sum(r['time'] for r in result['results'] if r['success']) * 1000 / successful if successful > 0 else 0
        
        print("| {:^20} | {:^20} | {:^16} | {:^16} | {:^15} |".format(
            num_users, isolation, successful, failed, f"{int(avg_time_ms)} ms"
        ))

def verify_postgresql_connection():
    """Verifica la conexión a PostgreSQL"""
    print("\n[!] Verificando conexión a PostgreSQL...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
        conn.close()
        print(f"[+] Conexión exitosa a PostgreSQL {version.split(',')[0]}")
        return True
    except Exception as e:
        print(f"\n[x] Error de conexión: {e}")
        print("\n[!] Solución requerida:")
        print("1. Asegúrate que PostgreSQL esté corriendo")
        print("2. Verifica las credenciales en DB_CONFIG")
        print("3. Configura pg_hba.conf adecuadamente")
        return False

def create_connection():
    """Crea una conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        return conn
    except psycopg2.OperationalError as e:
        print(f"\n[x] Error de conexión: {e}")
        raise ConnectionError("No se pudo establecer conexión con la base de datos")

def setup_database():
    """Prepara la base de datos para las pruebas"""
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        # Limpiamos la base de datos antes de cada prueba
        cursor.execute("DELETE FROM reservas")
        cursor.execute("ALTER SEQUENCE reservas_id_reserva_seq RESTART WITH 1")
        conn.commit()
        print("[+] Base de datos preparada exitosamente")
        
        # Reiniciamos el conjunto de asientos seleccionados
        global selected_seats
        selected_seats = set()
        
    except Exception as e:
        print(f"\n[x] Error en setup_database: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_available_seat_id():
    """Obtiene un ID de asiento que no haya sido seleccionado por otro hilo"""
    with seat_lock:
        # Obtener todos los asientos disponibles (no seleccionados previamente)
        available_seats = list(set(AVAILABLE_SEATS) - selected_seats)
        if not available_seats:
            return None
        
        # Seleccionar un asiento aleatorio de los disponibles
        seat_id = random.choice(available_seats)
        selected_seats.add(seat_id)
        return seat_id

def simulate_user(user_id, isolation_level, results, max_retries=5):
    """Simula un usuario intentando reservar el mismo asiento"""
    conn = None
    seat_id = 1  # Todos intentan reservar el mismo asiento

    for retry in range(max_retries):
        try:
            conn = create_connection()
            isolation_map = {
                "READ COMMITTED": psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
                "REPEATABLE READ": psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
                "SERIALIZABLE": psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
            }
            conn.set_isolation_level(isolation_map[isolation_level])
            
            cursor = conn.cursor()
            start_time = time.time()
            
            # Verificar si el asiento ya está reservado
            cursor.execute(
                "SELECT COUNT(*) FROM reservas WHERE id_asiento = %s", 
                (seat_id,)
            )
            count = cursor.fetchone()[0]
            
            if count == 0:
                if random.random() < 0.3:
                    time.sleep(random.uniform(0.01, 0.05))
                
                cursor.execute(
                    "INSERT INTO reservas (id_asiento, id_usuario, fecha_reserva) "
                    "VALUES (%s, %s, %s) RETURNING id_reserva",
                    (seat_id, user_id, datetime.now())
                )
                reservation_id = cursor.fetchone()[0]
                conn.commit()
                
                results.append({
                    'user_id': user_id,
                    'success': True,
                    'time': time.time() - start_time,
                    'reservation_id': reservation_id,
                    'seat_id': seat_id,
                    'retries': retry
                })
                return
            
            else:
                conn.rollback()
                time.sleep(random.uniform(0.01, 0.03))
                
                if retry == max_retries - 1:
                    results.append({
                        'user_id': user_id,
                        'success': False,
                        'error': 'Asiento ya reservado en BD',
                        'time': time.time() - start_time,
                        'seat_id': seat_id,
                        'retries': retry
                    })

        except (errors.UniqueViolation, errors.SerializationFailure) as e:
            conn.rollback()
            time.sleep(random.uniform(0.01, 0.05) * (retry + 1))
            
            if retry == max_retries - 1:
                error_type = 'Violación de unicidad' if isinstance(e, errors.UniqueViolation) else 'Error de serialización'
                results.append({
                    'user_id': user_id,
                    'success': False,
                    'error': f'{error_type} después de {max_retries} intentos',
                    'time': time.time() - start_time,
                    'seat_id': seat_id,
                    'retries': retry
                })

        except Exception as e:
            if retry == max_retries - 1:
                results.append({
                    'user_id': user_id,
                    'success': False,
                    'error': f'Excepción: {str(e)}',
                    'retries': retry
                })
        finally:
            if conn:
                try:
                    cursor.close()
                except:
                    pass
                conn.close()
    
    if not any(r.get('user_id') == user_id for r in results):
        results.append({
            'user_id': user_id,
            'success': False,
            'error': 'Agotados todos los reintentos',
            'time': 0,
            'retries': max_retries
        })


def run_test(num_users, isolation_level):
    """Ejecuta una prueba con usuarios concurrentes"""
    print(f"\n[TEST] {num_users} usuarios - Nivel {isolation_level}")
    
    try:
        setup_database()
        results = []
        threads = []
        
        # Calculamos un tiempo de llegada aleatorio para cada usuario
        arrival_times = []
        # Distribución de llegadas en un período de 2 segundos
        base_time = time.time()
        for i in range(num_users):
            # Simulamos una distribución más realista de llegadas
            arrival_time = base_time + random.expovariate(1.0) % 2.0
            arrival_times.append((i + 1, arrival_time))
        
        # Ordenamos por tiempo de llegada
        arrival_times.sort(key=lambda x: x[1])
        
        for user_id, arrival_time in arrival_times:
            # Esperamos hasta el tiempo de llegada calculado
            wait_time = arrival_time - time.time()
            if wait_time > 0:
                time.sleep(wait_time)
                
            t = threading.Thread(
                target=simulate_user,
                args=(user_id, isolation_level, results)
            )
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        successful = sum(1 for r in results if r['success'])
        print(f"\n[+] Reservas exitosas: {successful}/{num_users}")
        
        if successful > 0:
            avg_time = sum(r['time'] for r in results if r['success']) / successful
            print(f"  Tiempo promedio: {avg_time*1000:.2f} ms")
            
            # Mostrar número de reintentos promedio
            total_retries = sum(r.get('retries', 0) for r in results if r['success'])
            avg_retries = total_retries / successful if successful > 0 else 0
            print(f"  Reintentos promedio: {avg_retries:.2f}")
        
        if num_users - successful > 0:
            unique_errors = set(r['error'] for r in results if not r['success'])
            print("\n[x] Errores encontrados:")
            for error in list(unique_errors)[:3]:
                count = sum(1 for r in results if not r['success'] and r['error'] == error)
                print(f"  - {error} ({count} veces)")
        
        # Guardamos los resultados para la tabla final
        global_results.append({
            'isolation_level': isolation_level,
            'num_users': num_users,
            'successful': successful,
            'results': results
        })
    
    except Exception as e:
        print(f"\n[!] Error en la prueba: {str(e)}")

def main():
    """Función principal del simulador"""
    print("\n" + "="*60)
    print("=== SIMULADOR DE RESERVAS CONCURRENTES ===")
    print("="*60)
    
    if not verify_postgresql_connection():
        sys.exit(1)
    
    try:
        # Escenarios específicos de prueba
        test_scenarios = [
            (5, "READ COMMITTED"),
            (10, "REPEATABLE READ"),
            (20, "SERIALIZABLE"),
            (30, "SERIALIZABLE")
        ]
        
        for num_users, isolation_level in test_scenarios:
            run_test(num_users, isolation_level)
        
        # Imprimir tabla de resultados final
        print_results_table()
        
        # Mostrar estadísticas útiles
        total_users = sum(result['num_users'] for result in global_results)
        total_successful = sum(result['successful'] for result in global_results)
        total_failed = total_users - total_successful
        success_rate = (total_successful / total_users) * 100 if total_users > 0 else 0
        
        print("\n" + "="*60)
        print(f"=== RESUMEN DE RESULTADOS ===")
        print(f"Total de intentos de reserva: {total_users}")
        print(f"Reservas exitosas: {total_successful} ({success_rate:.2f}%)")
        print(f"Reservas fallidas: {total_failed} ({100-success_rate:.2f}%)")
        print("="*60)
        
        print("\n=== TODAS LAS PRUEBAS COMPLETADAS ===")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n[!] Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n[!] Error fatal: {str(e)}")
    finally:
        print("\n[!] Ejecución finalizada")

if __name__ == "__main__":
    main()