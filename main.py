import os
import platform

from laboratorio_poo import ( 
    CuentaBancariaNacional,
    CuentaBancariaInternacional,
    GestionCuentaBancaria
)

def limpiar_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print("------- Menu de Gestion de Cuenta Bancaria -------")
    print('1. Agregar Cuenta Bancaria con Moneda Nacional en la Cuenta Bancaria.')
    print('2. Agregar Cuenta Bancaria con Moneda Internacional en la Cuenta Bancaria.')
    print('3. Buscar Cuenta Bancaria por Numero de Cuenta.')
    print('4. Actualizar Cuenta Bancaria por Numero de Cuenta.')
    print('5. Eliminar Cuenta Bancaria por Numero de Cuenta.')
    print('6. Mostrar todas las Cuentas Bancarias')
    print('7. Salir.')
    print('-------------------------------------------------')

def agregar_cuentabancaria(gestion, tipo_cuentabancaria):
    try:
        nrocuenta = input('Ingrese el Numero de Cuenta: ')
        dni = int(input('Ingrese el DNI del titular de la cuenta: '))
        titular = input('Ingrese el nombre completo del titular de la cuenta: ')
        saldo = float(input('Ingrese el saldo de la cuenta: '))
        tipocuenta = input('Ingrese el tipo de cuenta, ya sea C/C o C/A: ')

        if tipo_cuentabancaria == '1':
            moneda_nac = input('Ingrese cual es la moneda nacional de la cuenta bancaria: ')
            cuentabancaria = CuentaBancariaNacional(nrocuenta, dni, titular, saldo, tipocuenta, moneda_nac)
        elif tipo_cuentabancaria == '2':
            moneda_int = input('Ingrese la moneda internacional de la cuenta bancaria')
            cuentabancaria = CuentaBancariaInternacional(nrocuenta, dni, titular, saldo, tipocuenta, moneda_int)
        else:
            print('Por favor volver a seleccionar una opcion.')
            return
        
        gestion.crear_cuentabancaria(cuentabancaria)
        input('Por favor, seleccionar enter para continuar.')

    except Exception as error:
        print(f'Error inesperado al agregar una cuenta bancaria: {error}')

def buscar_cuentabancaria_por_nrocuenta(gestion):
    nrocuenta = input('Ingrese el Numero de Cuenta que desea buscar: ')
    gestion.leer_cuentabancaria(nrocuenta)
    input('Presione enter para continuar.')

def actualizar_saldo_por_nrocuenta(gestion):
    nrocuenta = input('Ingrese el Numero de Cuenta que desea actualizar el saldo: ')
    saldo = float(input('Ingrese el nuevo saldo.'))
    gestion.actualizar_cuentabancaria(nrocuenta, saldo)
    input('Presione enter para continuar.')

def eliminar_cuentabancaria_por_nrocuenta(gestion):
    nrocuenta = input('Ingrese el Numero de Cuenta que desee eliminar.')
    gestion.eliminar_cuentabancaria(nrocuenta)
    input('Presione enter para continuar.')

def mostrar_todas_las_cuentas_bancarias(gestion):
    print('Cuentas Bancarias existentes: ')
    for cuentabancaria in gestion.leer_datos().values():
        if 'moneda nacional' in cuentabancaria:
            print(f"Numero de cuenta:{cuentabancaria['nrocuenta']} - Moneda Nacional: {cuentabancaria['moneda nacional']}")
        else:
            print(f"Numero de cuenta:{cuentabancaria['nrocuenta']} - Moneda Internacional: {cuentabancaria['moneda internacional']}")
    input('Presione enter para continuar.')

if __name__ == "__main__":
    archivo_cuentasbancarias = 'cuentas_bancarias.json'
    gestion_cuentasbancarias = GestionCuentaBancaria(archivo_cuentasbancarias)
    
    while True:
        limpiar_terminal()
        mostrar_menu()
        opcion = input('Seleccione una opcion: ')

        if opcion == '1' or opcion == '2':
            agregar_cuentabancaria(gestion_cuentasbancarias, opcion)
        elif opcion == '3':
            buscar_cuentabancaria_por_nrocuenta(gestion_cuentasbancarias)
        elif opcion == '4':
            actualizar_saldo_por_nrocuenta(gestion_cuentasbancarias)
        elif opcion == '5':
            eliminar_cuentabancaria_por_nrocuenta(gestion_cuentasbancarias)
        elif opcion == '6':
            mostrar_todas_las_cuentas_bancarias(gestion_cuentasbancarias)
        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opcion invalida')


