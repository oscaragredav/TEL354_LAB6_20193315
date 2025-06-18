class Alumno:
  def __init__(self, n, p, c=None):
    self.nombre = n
    self.codigo = c
    self.pc = p

  def imprimir(self):
    print(f"\tNombre:\t{self.nombre}")
    if self.codigo is not None:
      print(f"\tCodigo:\t{self.codigo}")
    print(f"\tPC:\t{self.pc}")
    
class Servicio:
    def __init__(self, n, pr, p):
        self.nombre = n
        self.protocolo = pr
        self.puerto = p
    def imprimir(self):
        print(f"\tNombre:\t{self.nombre}")
        print(f"\tProtoc:\t{self.protocolo}")
        print(f"\tPuerto:\t{self.puerto}")
    
class Servidor:
    def __init__(self, n, ip, servicios=None):
        self.nombre = n
        self.direccion = ip
        if servicios is None:
            self.servicios = []
        else:
            self.servicios = servicios

    def imprimir(self):
        print(f"\tNombre:\t{self.nombre}")
        print(f"\tDirec:\t{self.direccion}")
        print("\tServicios:")
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
        print(f"Curso:\t{self.nombre}")
        print(f"Estado:\t{self.estado}")
        print("Alumnos:")
        for i, alumno in enumerate(self.alumnos, 1):
            alumno.imprimir()
        print("Servicios:")
        for i, servicio in enumerate(self.servicios, 1):
            print(f"   Servicio {i}:")
            servicio.imprimir()


if __name__ == "__main__":
    a1 = Alumno("Oscar", "50-81-40-4C-04-86", 20193315)
    a2 = Alumno("Antonio", "50-81-40-4C-C9-0B", 2019316)
    alms = [a1, a2]

    s1 = Servicio("Web", "HTTP", 80)
    s2 = Servicio("FTP", "FTP", 21)
    srvs = [s1, s2]
    
    servidor1 = Servidor("Servidor1", "192.168.10.20", srvs)

    curso1 = Curso("Curso Python", "Activo", alms, srvs)

    curso1.imprimir()
    print("-----")

    a3 = Alumno("Agreda", "50-81-40-4C-B0-A2", None)
    curso1.agregar_alumno(a3)
    curso1.imprimir()
    print("-----")

    curso1.eliminar_alumno(a2)
    curso1.imprimir()