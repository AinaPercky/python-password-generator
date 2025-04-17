from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import random
import string
import json

def generate_password(length, include_digits, include_special_chars, include_capital):
    characters = string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_special_chars:
        characters += string.punctuation
    if include_capital:
        characters += string.ascii_uppercase

    return ''.join(random.choice(characters) for _ in range(length))

class PasswordAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/generate-password':
            query_params = urllib.parse.parse_qs(parsed_path.query)

            print("Query params received:", query_params)

            length = int(query_params.get("length", ["8"])[0])
            digits = query_params.get("digits", ["true"])[0].lower() == "true"
            special = query_params.get("special", ["true"])[0].lower() == "true"
            capital = query_params.get("capital", ["true"])[0].lower() == "true"

            # Debug print: parsed values
            print(f"Parsed -> length={length}, digits={digits}, special={special}, capital={capital}")

            password = generate_password(length, digits, special, capital)
            response = {"password": password}

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Endpoint not found")

if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("", port), PasswordAPIHandler)
    print(f"✅ Password API running on http://localhost:{port}/generate-password")
    server.serve_forever()
