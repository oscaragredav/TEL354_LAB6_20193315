import yaml
import requests
from ej2 import Alumno, Servicio, Servidor, Curso
from ej4 import get_attachment_points, get_route

def alumno_autorizado(alumno, servidor_nombre, servicio_nombre, cursos):
    for curso in cursos:
        if curso.estado == "DICTANDO" and alumno in curso.alumnos:
            for servidor in curso.servidores:
                if servidor.nombre == servidor_nombre:
                    servicios = [s.nombre for s in servidor.servicios]
                    if servicio_nombre in servicios:
                        return True
    return False

def get_attachment_points(mac_address):
    url = f"http://10.20.12.30:8080/wm/device/"
    response = requests.get(url)
    devices = response.json()

    for device in devices:
        if device['mac'][0].lower() == mac_address.lower():
            ap = device.get('attachmentPoint', [])
            if ap:
                dpid = ap[0].get('switchDPID')
                print(f"DPID: {dpid}")
                port = ap[0].get('port')
                print(f"Puerto: {port}")
                return dpid, port

    print(f"No se encontró la MAC")
    return None

def get_route(src_dpid, src_port, dst_dpid, dst_port):
    url = f"http://10.20.12.30:8080/wm/topology/route/{src_dpid}/{src_port}/{dst_dpid}/{dst_port}/json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error en la API")
        return []

    path = response.json()
    ruta = [(hop['switch'], hop['port']) for hop in path]
    return ruta

def build_route(route, alumno, servidor, servicio):
    mac_src = alumno.pc 
    ip_dst = servidor.ip
    puerto_l4 = servicio.puerto
    protocolo = servicio.protocolo.upper()
    proto_num = "0x06" if protocolo == "TCP" else "0x11"  

    for i in range(len(route)-1):
        dpid, out_port = route[i]

        flow = {
            "switch": dpid,
            "name": f"fwd_{i}_{alumno.codigo}",
            "priority": "32768",
            "eth_type": "0x0800",
            "eth_src": mac_src,
            "ipv4_dst": ip_dst,
            "ip_proto": proto_num,
            f"{protocolo.lower()}_dst": puerto_l4,
            "active": "true",
            "actions": f"output={out_port}"
        }
        enviar_flujo(flow)

        flow_back = {
            "switch": dpid,
            "name": f"bwd_{i}_{alumno.codigo}",
            "priority": "32768",
            "eth_type": "0x0800",
            "eth_dst": mac_src,
            "ipv4_src": ip_dst,
            "ip_proto": proto_num,
            f"{protocolo.lower()}_src": puerto_l4,
            "active": "true",
            "actions": f"output={out_port}"
        }
        enviar_flujo(flow_back)

        arp = {
            "switch": dpid,
            "name": f"arp_{i}_{alumno.codigo}",
            "eth_type": "0x0806",
            "priority": "32769",
            "actions": f"output={out_port}"
        }
        enviar_flujo(arp)

def enviar_flujo(flow):
    url = "http://10.20.12.30:8080/wm/staticflowentrypusher/json"
    response = requests.post(url, json=flow)
    if response.status_code == 200:
        print(f"Flow enviado: {flow['name']}")
    else:
        print(f"Error al enviar flow: {response.text}")

class NetworkManager:
    def __init__(self):
        self.alumnos = []
        self.cursos = []
        self.servidores = []
        self.conexiones = []
        
        
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
        print("1) Agregar alumno")
        print("2) Eliminar alumno")
        opcion = input(">>> ")
        self.listar_curso()
        try:
            idx_curso = int(input("Seleccione un curso: ")) - 1
            curso = self.cursos[idx_curso]
            self.listar_alumnos()
            idx_alumno = int(input("Seleccione un alumno: ")) - 1
            alumno = self.alumnos[idx_alumno]
            if opcion == "1":
                if alumno not in curso.alumnos:
                    curso.agregar_alumno(alumno)
                    print(f"Alumno {alumno.nombre} agregado al curso {curso.nombre}.")
                else:
                    print("El alumno ya está en el curso.")
            elif opcion == "2":
                if alumno in curso.alumnos:
                    curso.eliminar_alumno(alumno)
                    print(f"Alumno {alumno.nombre} eliminado del curso {curso.nombre}.")
                else:
                    print("El alumno no está en el curso.")
            else:
                print("Opción inválida.")
        except:
            print("Selección inválida")

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
            print(f"{i}. {servidor.nombre} ({servidor.ip})")
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
            print("0) Volver al menú principal")
            
            opcion = input(">>> ")
            
            if opcion == "1":
                self.crear_conexion()
            elif opcion == "2":
                self.listar_conexiones()
            elif opcion == "6":
                self.borrar_conexion()
            elif opcion == "0":
                break
    
    def crear_conexion(self):
        try:
            self.listar_alumnos()
            idx_a = int(input("Seleccione alumno: ")) - 1
            alumno = self.alumnos[idx_a]

            self.listar_servidor()
            idx_s = int(input("Seleccione servidor: ")) - 1
            servidor = self.servidores[idx_s]

            print("Servicios disponibles:")
            for i, servicio in enumerate(servidor.servicios, 1):
                print(f"{i}) {servicio.nombre}")
            idx_sv = int(input("Seleccione servicio: ")) - 1
            servicio = servidor.servicios[idx_sv]

            if not alumno_autorizado(alumno, servidor.nombre, servicio.nombre, self.cursos):
                print("Acceso denegado: alumno no autorizado para el servicio.")
                return

            ap_alumno = get_attachment_points(alumno.mac)
            ap_servidor = get_attachment_points("fa:16:3e:a1:dd:54")  

            if not ap_alumno or not ap_servidor:
                print("Error al obtener puntos de conexión")
                return

            ruta = get_route(ap_alumno[0], ap_alumno[1], ap_servidor[0], ap_servidor[1])

            if not ruta:
                print("No se encontró ruta")
                return

            build_route(ruta, alumno, servidor, servicio)
            self.conexiones.append((alumno, servidor, servicio))
            print("Conexión creada exitosamente.")
        except Exception as e:
            print(f"Error al crear la conexión: {str(e)}")

    def listar_conexiones(self):
        print("\nConexiones activas:")
        for i, (alumno, servidor, servicio) in enumerate(self.conexiones, 1):
            print(f"{i}. {alumno.nombre} -> {servidor.nombre} ({servicio.nombre})")

    def borrar_conexion(self):
        self.listar_conexiones()
        try:
            idx = int(input("Seleccione una conexión para borrar: ")) - 1
            if 0 <= idx < len(self.conexiones):
                del self.conexiones[idx]
                print("Conexión borrada exitosamente.")
            else:
                print("Selección inválida.")
        except ValueError:
            print("Entrada no válida. Debe ser un número.")

if __name__ == "__main__":
    manager = NetworkManager()
    print("\n###########")
    print("Network Policy manager de La UPSM")
    manager.menu()