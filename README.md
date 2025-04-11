# Proyecto2

## Autores:
Pablo Méndez, Karen Pineda

## 
Este proyecto simula un sistema de reservas concurrentes para eventos, utilizando diferentes niveles de aislamiento de transacciones en PostgreSQL. La aplicación permite evaluar el rendimiento y la eficacia de distintas configuraciones de aislamiento de transacciones en un escenario realista de reserva de asientos.

## Descriprión 
El simulador crea múltiples hilos concurrentes que intentan reservar asientos para un evento, simulando un escenario real donde muchos usuarios intentan conseguir entradas simultáneamente. La aplicación muestra estadísticas detalladas sobre las reservas exitosas, fallidas, tiempos de procesamiento y causas de error en diferentes configuraciones.

## Requisitos previos

- Python 3.6 o superior
- PostgreSQL 10 o superior
- Librería psycopg2 para Python

## Instalación

1. Clona o descarga este repositorio
``` bash
git clone https://github.com/Paul-1511/Proyecto2.git
```

2. Instala las dependencias necesarias
``` bash
pip install psycopg2-binary
```

3. Configura la base de datos PostgreSQL:


## Configuración
Antes de ejecutar el simulador, verifica y modifica si es necesario los siguientes parámetros en el archivo `reservas_concurrentes.py`:

```python
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
AVAILABLE_SEATS = range(1, 50)  # 49 asientos disponibles
NUM_USERS = [5, 10, 20, 30]   # Número de usuarios concurrentes a probar
```

Ajusta estos valores según tus necesidades
- `DB_CONFIG`: Cambia los parametros de conexión según tu configuración de PostgreSQL
- `AVAILABLE_SEATS`: Modifica el rango para aumentar o disminuir el número de asientos disponibles
- `NUM_USERS`: Ajusta la cantidad de usuarios concurrentes para cada prueba

## Ejecución
Para ejecutar la simulación:
1. Asegúrate de que PostgreSQL esté en ejecución
2. Ejecuta el script:
``` bash
python reservas_concurrentes.py
```
3. El programa verificará automáticamente la conexión a PostgreSQL y, si es exitosa, comenzará las pruebas de simulación.

## Interpretación de resultados
Al finalizar la ejecución, el programa mostrará una tabla de resultados con la siguiente información para cada escenario probado:

- Usuarios Concurrentes: Número de usuarios que intentaron hacer reservas simultáneamente
- Nivel de Aislamiento: Nivel de aislamiento de transacciones utilizado (READ COMMITTED, REPEATABLE READ, SERIALIZABLE)
- Reservas Exitosas: Cantidad de reservas realizadas con éxito
- Reservas Fallidas: Cantidad de intentos de reserva que no tuvieron éxito
- Tiempo Promedio: Tiempo promedio de procesamiento de las reservas exitosas

Además, al final de todas las pruebas, se mostrará un resumen global con estadísticas combinadas.

## Solución de problemas
Si el programa muestra errores de conexión a PostgreSQL:

1. Verifica que PostgreSQL esté en ejecución
2. Comprueba las credenciales en `DB_CONFIG`
3. Asegúrate de que la base de datos `reservas` existe y tiene la estructura correcta
4. Revisa que el usuario de PostgreSQL tiene permisos para acceder a la base de datos

## Características avanzadas

- Tiempo de espera variable entre usuarios: Simula llegadas no uniformes
- Reintentos automáticos: Cada usuario intenta hasta 5 veces si su primera reserva falla
- Simulación de procesamiento de pagos: Añade retrasos aleatorios para representar tiempos de procesamiento

## Nota sobre la concurrencia
Esta simulación utiliza hilos (threads) de Python para simular la concurrencia. Debido al GIL (Global Interpreter Lock) de Python, la concurrencia real puede ser limitada. Para entornos de producción con mayor concurrencia, considera implementar la lógica en otro lenguaje o utilizar procesos en lugar de hilos.







