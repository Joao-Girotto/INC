import socket
import struct

UDP_IP = "192.168.61.2"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Recebendo dados binários em {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    #print(f"Dados crus: {data[:20]}... ({len(data)} bytes)")

    try:
        if len(data) >= 12:
            x, y, z = struct.unpack('<fff', data[:12]) 
            print(f"Gyro - X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
        else:
            print("Pacote pequeno demais para 3 floats")
    except Exception as e:
        print("Erro ao interpretar os dados:", e)
