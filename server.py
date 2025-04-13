from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the data
        content_length = int(self.headers['Content-Length'])
        # Read the data from the request
        post_data = self.rfile.read(content_length)
        
        # Parse the form data
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        # Get the client's IP address
        client_ip = self.client_address[0]

        # Print the parsed data and client IP in a readable format
        print("Received POST request from:", client_ip)
        print("Parsed Data:")
        for key, value in parsed_data.items():
            print(f"  {key}: {', '.join(value)}")  # Join multiple values for better readability

        # Create an HTML response message including received fields and an image
        response_text = f'POST request received from {client_ip}. Fields received:<br>'
        for key, value in parsed_data.items():
            response_text += f'  {key}: {", ".join(value)}<br>'
            
        html_response = f"""
        <html>
        <head><title>POST Response</title></head>
        <body>
        <h1>POST Data Received</h1>
        <p>{response_text}</p>
        <img src="/http.png" alt="Served Image" width="300"> 
        </body>
        </html>
        """

        # Send response back to client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_response.encode('utf-8'))

    def do_GET(self):
        # Serve the image file if requested
        if self.path == '/http.png':
            image_path = 'http.png' # Assuming image is in the same directory
            if os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as f:
                        self.send_response(200)
                        # Infer content type based on extension (basic example)
                        content_type = 'image/png' # Defaulting to png
                        if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                            content_type = 'image/jpeg'
                        elif image_path.lower().endswith('.gif'):
                            content_type = 'image/gif'
                        # Add more types if needed
                        self.send_header('Content-type', content_type)
                        self.end_headers()
                        self.wfile.write(f.read())
                except IOError:
                    self.send_error(500, 'Error reading image file')
            else:
                self.send_error(404, 'Image file not found')
        # Handle root path or other paths if needed
        elif self.path == '/':
             self.send_response(200)
             self.send_header('Content-type', 'text/html')
             self.end_headers()
             self.wfile.write(b"<html><body><h1>Server is running</h1><p>Submit data via POST to see it displayed with an image.</p></body></html>")
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()