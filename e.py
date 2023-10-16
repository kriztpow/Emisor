import cv2
import socket
import pickle
import struct

# Configura la dirección IP y el puerto para la transmisión
host = '192.168.1.1'  # Cambia esto a la IP del receptor
port = 12345

# Crea un socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f'Esperando conexión en {host}:{port}...')

# Acepta la conexión entrante
client_socket, addr = server_socket.accept()

# Abre la cámara frontal
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
    ret, frame = cap.read()

    # Serializa el frame en formato pickle y luego en formato de bytes
    data = pickle.dumps(frame)
    message_size = struct.pack("L", len(data))

    # Envía el tamaño del mensaje
    client_socket.sendall(message_size)

    # Envía el frame
    client_socket.sendall(data)

# Cierra la conexión y la cámara
client_socket.close()
cap.release()
