import yaml

with open('datos.yaml', 'r') as file:
    datos = yaml.safe_load(file)

print("Servidores:")
for servidor in datos['servidores']:
    print(servidor['nombre'])