import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            try:
                while True:
                    frame = get_frame()
                    if frame is not None:
                        ret, jpg = cv2.imencode('.jpg', frame)
                        self.wfile.write("--jpgboundary\r\n".encode())
                        self.send_header('Content-type', 'image/jpeg')
                        self.send_header('Content-length', str(jpg.size))
                        self.end_headers()
                        self.wfile.write(jpg.tobytes())
                        self.wfile.write("\r\n".encode())
            except KeyboardInterrupt:
                pass
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Only .mjpg supported.".encode())

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """This is an HTTPServer that supports thread-based concurrency."""

def get_frame():
    cap = cv2.VideoCapture(0)  # Abre la cámara frontal (puede variar según tu dispositivo)
    
    if not cap.isOpened():
        return None  # No se pudo abrir la cámara
    
    ret, frame = cap.read()
    
    if not ret:
        return None  # No se pudo capturar un frame
    
    # Realiza cualquier procesamiento adicional necesario en 'frame' aquí
    
    cap.release()  # Libera la cámara
    
    return frame

def main():
    try:
        server = ThreadedHTTPServer(('127.0.0.1', 8080), CamHandler)
        print("Server started on port 8080")
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
