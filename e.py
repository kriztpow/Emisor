import cv2
import imutils
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
                    frame = get_frame()  # Función que captura un frame de la cámara
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
    # Esta función debe capturar y devolver un frame de la cámara frontal
    # Puedes usar OpenCV para capturar la cámara

def main():
    try:
        server = ThreadedHTTPServer(('0.0.0.0', 8080), CamHandler)
        print("Server started on port 8080")
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()
