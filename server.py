from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

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

        # Create a response message including received fields
        response_message = f'POST request received from {client_ip}. Fields received:\n'
        for key, value in parsed_data.items():
            response_message += f'  {key}: {", ".join(value)}\n'

        # Send response back to client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()