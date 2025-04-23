import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Setup paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
UNIVERSITIES_FILE = os.path.join(DATA_DIR, "universities.json")

# Helper functions
def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

class SimpleRequestHandler(BaseHTTPRequestHandler):

    def set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.set_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/students":
            students = load_json(STUDENTS_FILE)
            universities = {u["id"]: u["name"] for u in load_json(UNIVERSITIES_FILE)}
            for student in students:
                uid = student.get("university_id")
                student["university_name"] = universities.get(uid, "") if uid else None
            self.respond_json(students)

        elif self.path == "/universities":
            universities = load_json(UNIVERSITIES_FILE)
            self.respond_json(universities)

        else:
            self.respond_error(404, "Endpoint not found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.respond_error(400, "Invalid JSON")
            return

        if self.path == "/students":
            self.handle_add_student(data)
        elif self.path == "/link":
            self.handle_link_student(data)
        else:
            self.respond_error(404, "Endpoint not found")

    def handle_add_student(self, data):
        if "name" not in data:
            self.respond_error(400, "Missing student name")
            return

        students = load_json(STUDENTS_FILE)
        new_id = max([s["id"] for s in students], default=0) + 1
        new_student = {
            "id": new_id,
            "name": data["name"],
            "university_id": None
        }
        students.append(new_student)
        save_json(STUDENTS_FILE, students)

        self.respond_json({"message": "Student added"}, 201)

    def handle_link_student(self, data):
        if "student_id" not in data or "university_id" not in data:
            self.respond_error(400, "Missing fields")
            return

        students = load_json(STUDENTS_FILE)
        updated = False
        for student in students:
            if student["id"] == data["student_id"]:
                student["university_id"] = data["university_id"]
                updated = True
                break

        if not updated:
            self.respond_error(404, "Student not found")
            return

        save_json(STUDENTS_FILE, students)
        self.respond_json({"message": "Student linked successfully"})

    def respond_json(self, data, status=200):
        self.send_response(status)
        self.set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def respond_error(self, status, message):
        self.send_response(status)
        self.set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

    def log_message(self, format, *args):
        return  # Silence logs for clean output

def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8000):
    server_address = ('', port)
    print(f"✅ Server running at http://localhost:{port}/")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
