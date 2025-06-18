import yaml
import requests
from ej2 import Alumno, Servicio, Servidor, Curso
from ej4 import get_attachment_points, get_route

class NetworkManager:
    def __init__(self):
        self.alumnos = []
        self.cursos = []
        self.servidores = []
        self.conexiones = []
        self.controller_ip = "10.20.12.30"
        
    def cargar_datos(self, archivo):
        with open(archivo, 'r') as file:
            datos = yaml.safe_load(file)
            
            for alumno_data in datos.get('alumnos', []):
                self.alumnos.append(Alumno(
                    n=alumno_data['nombre'],
                    p=alumno_data['mac'],
                    c=alumno_data['codigo']
                ))
            
            for servidor_data in datos.get('servidores', []):
                servicios = []
                for servicio_data in servidor_data.get('servicios', []):
                    servicios.append(Servicio(
                        servicio_data['nombre'],
                        servicio_data['protocolo'],
                        servicio_data['puerto']
                    ))
                self.servidores.append(Servidor(
                    servidor_data['nombre'],
                    servidor_data['ip'],
                    servicios
                ))
            
            for curso_data in datos.get('cursos', []):
                alumnos_curso = []
                for codigo in curso_data.get('alumnos', []):
                    for alumno in self.alumnos:
                        if hasattr(alumno, 'codigo') and alumno.codigo == codigo:
                            alumnos_curso.append(alumno)
                
                servidores_curso = []
                for servidor_data in curso_data.get('servidores', []):
                    for servidor in self.servidores:
                        if servidor.nombre == servidor_data['nombre']:
                            servidores_curso.append(servidor)
                
                self.cursos.append(Curso(
                    curso_data['nombre'],
                    curso_data['estado'],
                    alumnos_curso,
                    servidores_curso
                ))

#PRINCIPAL
    def mostrar_menu_principal(self):
        print("###########")
        print("Seleccione una opción:")
        print("1) Importar")
        print("2) Exportar")
        print("3) Cursos")
        print("4) Alumnos")
        print("5) Servidores")
        print("6) Políticas")
        print("7) Conexiones")
        print("8) Salir")
    def menu(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input(">>> ")
            
            if opcion == "1":
                archivo = input("Nombre del archivo a importar: ")
                self.cargar_datos(archivo)
                print(f"Datos importados desde {archivo}")
            elif opcion == "2":
                print("Exportar")
            elif opcion == "3":
                self.menu_cursos()
            elif opcion == "4":
                self.menu_alumnos()
            elif opcion == "5":
                self.menu_servidores()
            elif opcion == "6":
                self.menu_politicas()
            elif opcion == "7":
                self.menu_conexiones()
            elif opcion == "0":
                break

#CURSOS
    def menu_cursos(self):
        while True:
            print("\n--- GESTIÓN DE CURSOS ---")
            print("1) Crear curso")
            print("2) Listar cursos")
            print("3) Mostrar detalle de curso")
            print("4) Actualizar curso")
            print("5) Borrar curso")
            print("0) Volver al menú principal")
            
            opcion = input(">>> ")
            
            if opcion == "2":
                self.listar_curso()
            elif opcion == "3":
                self.mostrar_detalle_curso()
            elif opcion == "4":
                self.actualizar_curso()
            elif opcion == "0":
                break
    def listar_curso(self):
        print("\nListado de cursos:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.nombre} ({curso.estado})")  
    def mostrar_detalle_curso(self):
        self.listar_curso()
        try:
            idx = int(input("Seleccione un curso: ")) - 1
            curso = self.cursos[idx]
            curso.imprimir()
        except:
            print("Selección inválida")
    def actualizar_curso(self):
        print("\n--- ACTUALIZAR CURSO ---")

#ALUMNOS
    def menu_alumnos(self):
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1) Listar alumnos")
            print("2) Mostrar detalle de alumno")
            print("3) Crear alumno")
            print("0) Volver al menú principal")
            
            opcion = input(">>> ")
            
            if opcion == "1":
                self.listar_alumnos()
            elif opcion == "2":
                self.mostrar_detalle_alumno()
            elif opcion == "3":
                self.crear_alumno()
            elif opcion == "0":
                break
    def listar_alumnos(self):
        print("\nListado de alumnos:")
        for i, alumno in enumerate(self.alumnos, 1):
            print(f"{i}. {alumno.nombre}")
    def mostrar_detalle_alumno(self):
        self.listar_alumnos()
        try:
            idx = int(input("Seleccione un alumno: ")) - 1
            alumno = self.alumnos[idx]
            alumno.imprimir()
        except:
            print("Selección inválida")
    def crear_alumno(self):
        print("\n--- CREAR ALUMNO ---")
        nombre = input(">>> Nombre: ")
        mac = input(">>> PC: ")
        codigo = input(">>> Código: ")
        
        nuevo_alumno = Alumno(n= nombre, p = mac, c= codigo)
        self.alumnos.append(nuevo_alumno)
        print(f"Alumno {nombre} creado con éxito.")

#SERVIDORES
    def menu_servidores(self):
        while True:
            print("\n--- GESTIÓN DE SERVIDORES ---")
            print("1) Crear servidor")
            print("2) Listar servidores")
            print("3) Mostrar detalle de servidor")
            print("4) Actualizar servidor")
            print("5) Borrar servidor")
            print("0) Volver al menú principal")
            
            opcion = input(">>> ")
            
            if opcion == "2":
                self.listar_servidor()
            elif opcion == "3":
                self.mostrar_detalle_servidor()
            elif opcion == "0":
                break
    def listar_servidor(self):
        print("\nListado de servidores:")
        for i, servidor in enumerate(self.servidores, 1):
            print(f"{i}. {servidor.nombre} ({servidor.direccion})")
    def mostrar_detalle_servidor(self):
        self.listar_servidor()
        try:
            idx = int(input("Seleccione un servidor: ")) - 1
            servidor = self.servidores[idx]
            servidor.imprimir()
        except:
            print("Selección inválida")

#CONEXIONES
    def menu_conexiones(self):
        while True:
            print("\n--- GESTIÓN DE CONEXIONES ---")
            print("1) Crear conexión")
            print("2) Listar conexiones")
            print("3) Mostrar detalle de conexión")
            print("4) Recalcular conexión")
            print("5) Actualizar conexión")
            print("6) Borrar conexión")
            
            opcion = input(">>> ")
            
            if opcion == "1":
                self.listar_conexiones()
            elif opcion == "2":
                self.mostrar_detalle_conexion()
            elif opcion == "3":
                self.crear_conexion()
            elif opcion == "4":
                break

if __name__ == "__main__":
    manager = NetworkManager()
    print("\n###########")
    print("Network Policy manager de La UPSM")
    manager.menu()