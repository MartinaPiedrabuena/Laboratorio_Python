'''
Desafío 4: Sistema de Gestión de Cuentas Bancarias

Objetivo: Desarrollar un sistema para administrar cuentas bancarias de clientes.

Requisitos:
- Crear una clase base CuentaBancaria con atributos como número de cuenta, saldo, titular de la cuenta, etc.
- Definir al menos 2 clases derivadas para diferentes tipos de cuentas bancarias (por ejemplo, CuentaBancariaCorrientes, CuentaBancariaAhorro) con atributos y métodos específicos.
- Implementar operaciones CRUD para gestionar las cuentas bancarias.
- Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
- Persistir los datos en archivo JSON
'''

import json

class CuentaBancaria:
    def __init__(self, nrocuenta, dni, titular, saldo, tipocuenta):
        self.__nrocuenta = self.validar_nrocuenta(nrocuenta)
        self.__dni = self.validar_dni(dni)
        self.__titular = titular
        self.__saldo = self.validar_saldo(saldo)
        self.__tipocuenta = tipocuenta

    @property
    def nrocuenta(self):
        return self.__nrocuenta

    @property
    def dni(self):
        return self.__dni

    @property
    def titular(self):
        return self.__titular.capitalize()

    @property
    def saldo(self):
        return self.__saldo

    @property
    def tipocuenta(self):
        return self.__tipocuenta
    
    @nrocuenta.setter
    def nrocuenta(self, nueva_cuenta):
        self.__nrocuenta = self.validar_nrocuenta(nueva_cuenta)

    @dni.setter
    def dni(self, nuevo_dni):
        self.__dni = self.validar_dni(nuevo_dni)

    @saldo.setter
    def saldo(self, nuevo_saldo):
        self.__saldo = self.validar_saldo(nuevo_saldo)

    def validar_nrocuenta(self, nrocuenta):
        try:
            nrocuenta_num = int(nrocuenta)
            if nrocuenta_num < 0:
                raise ValueError('El numero de cuenta no puede ser negativo')
            return nrocuenta_num
        except ValueError:
            raise ValueError('El numero de cuenta debe ser valido')
        except Exception as error:
            print(f'Error inesperado: {error}')
        
    def validar_dni(self, dni):
        try:
            dni_num = int(dni)
            if dni_num <= 0:
                raise ValueError('El dni debe ser mayor a cero.')
            return dni_num
        except ValueError:
            raise ValueError('El DNI debe ser numerico')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def validar_saldo(self, saldo):
        try:
            saldo_num = float(saldo)
            if saldo_num < 0:
                raise ValueError('El saldo en la cuenta no puede ser negativo')
            return saldo_num
        except ValueError:
            raise ValueError('El saldo en la cuenta debe ser un valor numerico')
        except Exception as error:
            print(f'Error inesperado: {error}')        

    def to_dict(self):
        return {
            'nrocuenta': self.nrocuenta,
            'dni': self.dni,
            'titular': self.titular,
            'saldo': self.saldo,
            'tipocuenta': self.tipocuenta
        }
    
    def __str__(self):
        return f'{self.titular} {self.nrocuenta}'
    
class CuentaBancariaNacional(CuentaBancaria):
    def __init__(self, nrocuenta, dni, titular, saldo, tipocuenta, moneda_nac):
        super().__init__(nrocuenta, dni, titular, saldo, tipocuenta)
        self.__moneda_nac = moneda_nac

    @property
    def moneda_nac(self):
        return self.__moneda_nac
    
    def to_dict(self):
        dato = super().to_dict()
        dato['moneda nacional'] = self.moneda_nac
        return dato
    
    def __str__(self):
        return f'{super().__str__()} - Moneda Nacional: {self.moneda_nac}'
        
class CuentaBancariaInternacional(CuentaBancaria):
    def __init__(self, nrocuenta, dni, titular, saldo, tipocuenta, moneda_int):
        super().__init__(nrocuenta, dni, titular, saldo, tipocuenta)
        self.__moneda_int = moneda_int

    @property
    def moneda_int(self):
        return self.__moneda_int
    
    def to_dict(self):
        dato = super().to_dict()
        dato['moneda internacional'] = self.moneda_int
        return dato
    
    def __str__(self):
        return f'{super().__str__()} - Moneda Internacional: {self.moneda_int}'
    
class GestionCuentaBancaria:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except ValueError:
            print('Se encontro un valor no numerico en el archivo')
        except Exception as error:
            raise Exception(f'Error inesperado: {error}')
        else:
            return datos
        
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=3)
        except IOError as error:
            print(f'Error al guardar los datos en {self.archivo}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_cuentabancaria(self, cuentabancaria):
        try: 
            datos = self.leer_datos()
            nrocuenta = cuentabancaria.nrocuenta
            if not str(nrocuenta) in datos.keys():
                datos[nrocuenta] = cuentabancaria.to_dict()
                self.guardar_datos(datos)
                print(f'Cuenta numero {cuentabancaria.nrocuenta} creada correctamente.')
            else:
                print(f'Cuenta Bancaria {nrocuenta} ya existente')
        except Exception as error:
            print(f'Error inesperado al crear una cuenta bancaria: {error}')

    def leer_cuentabancaria(self, nrocuenta):
        try:
            datos = self.leer_datos()
            if nrocuenta in datos:
                cuentabancaria_data = datos[nrocuenta]
                if 'moneda nacional' in cuentabancaria_data:
                    cuentabancaria = CuentaBancariaNacional(**cuentabancaria_data)
                else:
                    cuentabancaria = CuentaBancariaInternacional(**cuentabancaria_data)
                print(f'Numero de Cuenta: {nrocuenta} hallada correctamente')
            else:
                print(f'Numero de cuenta: {nrocuenta} no encontrado')
        except ValueError:
            raise print('Se encontro un valor no numerico en el numero de cuenta')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def actualizar_cuentabancaria(self, nrocuenta, nuevo_saldo):
        try:
            datos = self.leer_datos()
            if str(nrocuenta) in datos.keys():
                datos[nrocuenta]['saldo'] = nuevo_saldo
                self.guardar_datos(datos)
                print(f'Saldo actualizado correctamente en la cuenta: {nrocuenta}')
            else:
                print(f'No se encontro una cuenta bancaria con el numero de cuenta {nrocuenta}')
        except ValueError:
            raise print('Se encontro un valor no numerico en el numero de cuenta.')
        except Exception as error:
            print(f'Error inesperado al actualizar la cuenta numero:{nrocuenta}, {error}')

    def eliminar_cuentabancaria(self, nrocuenta):
        try:
            datos = self.leer_datos()
            if str(nrocuenta) in datos.keys():
                del datos[nrocuenta]
                self.guardar_datos(datos)
                print(f'Cuenta bancaria {nrocuenta} eliminada correctamente.')
            else: 
                print(f'Cuenta bancaria {nrocuenta} no encontrada.')
        except ValueError:
            raise print(f'Se encontro un valor no numerico en el numero de cuenta.')
        except Exception as error:
            print(f'Error inesperado al tratar de eliminar la cuenta bancaria: {error}')








