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
        """Carga datos desde un archivo YAML"""
        with open(archivo, 'r') as file:
            datos = yaml.safe_load(file)
            
            # Cargar alumnos
            for alumno_data in datos.get('alumnos', []):
                self.alumnos.append(Alumno(
                    alumno_data['nombre'],
                    alumno_data['mac']
                ))
            
            # Cargar servidores
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
            
            # Cargar cursos
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

    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n###########")
        print("Network Policy manager de La UPSM")
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

    def menu_alumnos(self):
        """Submenú para gestión de alumnos"""
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1) Listar alumnos")
            print("2) Mostrar detalle de alumno")
            print("3) Crear alumno")
            print("4) Volver al menú principal")
            
            opcion = input(">>> ")
            
            if opcion == "1":
                self.listar_alumnos()
            elif opcion == "2":
                self.mostrar_detalle_alumno()
            elif opcion == "3":
                self.crear_alumno()
            elif opcion == "4":
                break

    def listar_alumnos(self):
        """Lista todos los alumnos"""
        print("\nListado de alumnos:")
        for i, alumno in enumerate(self.alumnos, 1):
            print(f"{i}. {alumno.nombre}")

    def mostrar_detalle_alumno(self):
        """Muestra detalles de un alumno específico"""
        self.listar_alumnos()
        try:
            idx = int(input("Seleccione un alumno: ")) - 1
            alumno = self.alumnos[idx]
            print(f"\nDetalle de {alumno.nombre}:")
            print(f"- Código: {getattr(alumno, 'codigo', 'No asignado')}")
            print(f"- MAC: {alumno.pc}")
            
            print("\nCursos matriculados:")
            for curso in self.cursos:
                if alumno in curso.alumnos:
                    print(f"- {curso.nombre} ({curso.estado})")
        except:
            print("Selección inválida")

    def crear_alumno(self):
        """Crea un nuevo alumno"""
        nombre = input("Nombre del alumno: ")
        codigo = input("Código del alumno: ")
        mac = input("Dirección MAC: ")
        
        nuevo_alumno = Alumno(nombre, mac)
        nuevo_alumno.codigo = codigo
        self.alumnos.append(nuevo_alumno)
        print(f"Alumno {nombre} creado exitosamente!")

    # Implementar métodos similares para cursos, servidores y conexiones

    def menu_principal(self):
        """Controla el flujo principal de la aplicación"""
        while True:
            self.mostrar_menu_principal()
            opcion = input(">>> ")
            
            if opcion == "1":
                archivo = input("Nombre del archivo a importar: ")
                self.cargar_datos(archivo)
            elif opcion == "2":
                print("Exportar (a implementar)")
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
            elif opcion == "8":
                print("Saliendo del sistema...")
                break

if __name__ == "__main__":
    manager = NetworkManager()
    manager.menu_principal()