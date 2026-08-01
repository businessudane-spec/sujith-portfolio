import http.server
import os

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Resolve the actual file path
        path = self.translate_path(self.path)
        
        # Check if file exists, or if directory exists check for index.html
        exists = os.path.exists(path)
        if exists and os.path.isdir(path):
            exists = os.path.exists(os.path.join(path, 'index.html'))
            
        # If file/directory index doesn't exist, serve custom 404.html
        if not exists:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            try:
                # Fallback path to the root 404.html
                root_dir = os.getcwd()
                with open(os.path.join(root_dir, '404.html'), 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(b"404 Not Found")
            return
            
        return super().do_GET()

if __name__ == '__main__':
    print(f"Starting server on port {PORT} with custom 404 fallback...")
    server = http.server.HTTPServer(('0.0.0.0', PORT), CustomHTTPRequestHandler)
    server.serve_forever()
