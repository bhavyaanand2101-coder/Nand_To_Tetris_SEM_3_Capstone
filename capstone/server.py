import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8046

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve dashboard.html by default
        if path == "/" or path == "":
            return os.path.join(os.path.dirname(__file__), "dashboard.html")
        return super().translate_path(path)

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"=== Hack Computer Dashboard Running ===")
            print(f"URL: http://localhost:{PORT}")
            print(f"Press Ctrl+C to stop.")
            sys.stdout.flush()
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
