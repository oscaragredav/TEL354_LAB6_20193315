import requests

h1_mac = "fa:16:3e:3e:a5:f0"
h3_mac = "fa:16:3e:a1:dd:54"

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

if __name__ == "__main__":
    print("h1")
    h1_point = get_attachment_points(h1_mac)
    print("h3")
    h3_point = get_attachment_points(h3_mac)

    if h1_point and h3_point:
        ruta = get_route(h1_point[0], h1_point[1], h3_point[0], h3_point[1])

        if ruta:
            print("Ruta")
            for switch, port in ruta:
                print(f"Switch: {switch} - Puerto: {port}")
        else:
            print("No se encontro ruta")
