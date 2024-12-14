# server.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/":
                self.path = "/index.html"
            elif self.path.startswith("/run-program-1"):
                # Path to your first Python script
                script_path = r"D:\download\New folder (2)\Group 10\Group 10\ItoT.py"
                if os.path.exists(script_path):
                    subprocess.Popen(["python", script_path], shell=True)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"Running Python program from ItoT directory...")
                else:
                    self.send_error(404, "File not found")
                return
            elif self.path.startswith("/run-program-2"):
                # Path to your second Python script
                script_path = r"D:\download\New folder (2)\Group 10\Group 10\ObjectDetection.py"
                if os.path.exists(script_path):
                    subprocess.Popen(["python", script_path], shell=True)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"Running Python program from ObjectDetection directory...")
                else:
                    self.send_error(404, "File not found")
                return
            else:
                self.send_error(404, "Page not found")
                return

            if self.path == "/index.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("index.html", "rb") as file:
                    self.wfile.write(file.read())
        except Exception as e:
            self.send_error(500, str(e))

def run():
    address = ('', 8000)  # Specify your desired port here
    server = HTTPServer(address, RequestHandler)
    print(f"Starting server at http://localhost:{address[1]}")
    server.serve_forever()

if __name__ == "__main__":
    run()
