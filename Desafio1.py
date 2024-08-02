import json
import os
import random

# Clase base Cliente
class Cliente:
    def __init__(self, nombre, apellido, cuenta):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__cuenta = cuenta

# Subclase para Caja de Ahorros
class CajaDeAhorros(Cliente):
    def __init__(self, nombre, apellido, cuenta, dni):
        super().__init__(nombre, apellido, cuenta)
        self.__dni = dni

# Subclase para Cuenta Corriente
class CuentaCorriente(Cliente):
    def __init__(self, nombre, apellido, cuenta, cuit):
        super().__init__(nombre, apellido, cuenta)
        self.__cuit = cuit

# Función para cargar clientes desde el archivo
def cargar_clientes():
    if os.path.exists('Desafio1.json'):
        with open('Desafio1.json', 'r') as file:
            return json.load(file)
    else:
        return []

# Función para guardar clientes en el archivo
def guardar_clientes(clientes):
    with open('Desafio1.json', 'w') as file:
        json.dump(clientes, file, indent=4)

# Función para generar un número de cuenta único de 4 dígitos
def generar_numero_cuenta():
    clientes = cargar_clientes()
    cuentas_existentes = {cliente['cuenta'] for cliente in clientes}
    while True:
        cuenta = str(random.randint(1000, 9999))
        if cuenta not in cuentas_existentes:
            return cuenta

# Función para verificar si el DNI o CUIT ya existe
def verificar_id_existente(id_cliente, tipo_cliente):
    clientes = cargar_clientes()
    for cliente in clientes:
        if tipo_cliente == 'P' and 'dni' in cliente and cliente['dni'] == id_cliente:
            return True
        if tipo_cliente == 'E' and 'cuit' in cliente and cliente['cuit'] == id_cliente:
            return True
    return False

# Función para crear una nueva cuenta
def crear_cuenta():
    tipo_cliente = input("Ingrese el tipo de cliente ('P' para persona, 'E' para empresa): ").upper()

    if tipo_cliente == 'P':
        dni = input("Ingrese el DNI (7 u 8 dígitos): ")
        if len(dni) not in [7, 8] or not dni.isdigit():
            print("El DNI debe tener 7 u 8 dígitos.")
            return
        if verificar_id_existente(dni, tipo_cliente):
            print("El DNI ya ha sido registrado.")
            return
        id_cliente = dni
    elif tipo_cliente == 'E':
        cuit = input("Ingrese el CUIT (11 dígitos): ")
        if len(cuit) != 11 or not cuit.isdigit():
            print("El CUIT debe tener 11 dígitos.")
            return
        if verificar_id_existente(cuit, tipo_cliente):
            print("El CUIT ya ha sido registrado.")
            return
        id_cliente = cuit
    else:
        print("Tipo de cliente inválido.")
        return

    nombre = input("Ingrese el nombre: ")
    apellido = input("Ingrese el apellido: ")
    cuenta = generar_numero_cuenta()

    if tipo_cliente == 'P':
        cliente = CajaDeAhorros(nombre, apellido, cuenta, dni)
    else:
        cliente = CuentaCorriente(nombre, apellido, cuenta, cuit)

    clientes = cargar_clientes()
    clientes.append(cliente.__dict__)
    guardar_clientes(clientes)
    print(f"Cuenta N° {cuenta} a nombre de {apellido}, {nombre} (ID: {id_cliente}) creada exitosamente.")

# Función para eliminar una cuenta
def eliminar_cuenta():
    cuenta = input("Ingrese el número de cuenta a eliminar (4 dígitos): ")

    if len(cuenta) != 4 or not cuenta.isdigit():
        print("El número de cuenta debe tener 4 dígitos.")
        return

    clientes = cargar_clientes()
    cliente_a_eliminar = next((cliente for cliente in clientes if cliente['cuenta'] == cuenta), None)

    if cliente_a_eliminar:
        clientes = [cliente for cliente in clientes if cliente['cuenta'] != cuenta]
        guardar_clientes(clientes)
        id_cliente = cliente_a_eliminar.get('dni') or cliente_a_eliminar.get('cuit')
        print(f"Cuenta N° {cuenta} a nombre de {cliente_a_eliminar['apellido']}, {cliente_a_eliminar['nombre']} (ID: {id_cliente}) eliminada exitosamente.")
    else:
        print("Cuenta no encontrada.")

# Función para consultar la lista de clientes
def consultar_lista_clientes():
    clientes = cargar_clientes()
    for cliente in clientes:
        id_cliente = cliente.get('dni') or cliente.get('cuit')
        print(f"Cliente {cliente['apellido']}, {cliente['nombre']} (ID: {id_cliente}), Cuenta N°: {cliente['cuenta']}.")

# Función para mostrar el menú
def mostrar_menu():
    while True:
        print("\n========== Menú Principal ==========")
        print("1. Crear cuenta")
        print("2. Eliminar cuenta")
        print("3. Consultar lista de clientes")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crear_cuenta()
        elif opcion == '2':
            eliminar_cuenta()
        elif opcion == '3':
            consultar_lista_clientes()
        elif opcion == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione nuevamente.")

if __name__ == "__main__":
    mostrar_menu()
