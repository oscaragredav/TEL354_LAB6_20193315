class Alumno:
  def __init__(self, n, p):
    self.nombre = n
    self.pc = p

  def imprimir(self):
    print(self.__dict__)
    
class Servicio:
    def __init__(self, n, pr, p):
        self.nombre = n
        self.protocolo = pr
        self.puerto = p
    def imprimir(self):
        print(self.__dict__)
    
class Servidor:
    def __init__(self, n, ip, servicios=None):
        self.nombre = n
        self.direccion = ip
        if servicios is None:
            self.servicios = []
        else:
            self.servicios = servicios

    def imprimir(self):
        print(f"'Nombre': '{self.nombre}', 'Direccion': '{self.direccion}'")
        print("'Servicios':")
        for servicio in self.servicios:
            servicio.imprimir()

class Curso:
    def __init__(self, n, e, alumnos=None, servicios=None):
        self.nombre = n
        self.estado = e
        if servicios is None:
            self.servicios = []
        else:
            self.servicios = servicios
        if alumnos is None:
            self.alumnos = []
        else:
            self.alumnos = alumnos

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)
    
    def eliminar_alumno(self, alumno):
        self.alumnos.remove(alumno)

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def imprimir(self):
        print(f"'Curso': '{self.nombre}', 'Estado': '{self.estado}'")
        print("'Alumnos':")
        for alumno in self.alumnos:
            alumno.imprimir()
        print("'Servicios':")
        for servicio in self.servicios:
            servicio.imprimir()


if __name__ == "__main__":
    a1 = Alumno("Oscar", "50-81-40-4C-04-86")
    a2 = Alumno("Antonio", "50-81-40-4C-C9-0B")
    alms = [a1, a2]

    s1 = Servicio("Web", "HTTP", 80)
    s2 = Servicio("FTP", "FTP", 21)
    srvs = [s1, s2]
    
    servidor1 = Servidor("Servidor1", "192.168.10.20", srvs)

    curso1 = Curso("Curso Python", "Activo", alms, srvs)

    curso1.imprimir()
    print("-----")

    a3 = Alumno("Agreda", "50-81-40-4C-B0-A2")
    curso1.agregar_alumno(a3)
    curso1.imprimir()
    print("-----")

    curso1.eliminar_alumno(a2)
    curso1.imprimir()