import gc, time, json
from massage_controller import MassageController
from heat_controller import HeatController
from microserver import MicroServer

class App:
    
    SHOULDER_MASSAGER_PINS = 4, 27, 32 # IN1, IN2, ENA -> Driver-2
    LUMBER_MASSAGER_PINS = 19, 21, 22  # IN3, IN4, ENB -> Driver-2
    THIGHS_MASSAGER_PINS = 13, 14, 18  # IN1, IN2, ENA -> Driver-1
    ARMS_MASSAGER_PINS = 23, 25, 26    # IN3, IN4, ENB -> Driver-1
    HEAT_CONTROLLER_PINS = 15, 16, 17  # IN1, IN2(RX2), ENA(TX2) -> Driver-3
    
    def __init__(self) :
        self.power = False
        self.heat = False
        self.temperature = 30
        self.shoulder = self.lumber = self.thighs = self.arms = MassageController.MODE_OFF
        self.massage_controller = MassageController(App.SHOULDER_MASSAGER_PINS, App.LUMBER_MASSAGER_PINS, App.THIGHS_MASSAGER_PINS, App.ARMS_MASSAGER_PINS)
        self.heat_controller = HeatController(App.HEAT_CONTROLLER_PINS)
    
    
    def set_parameters(self, body_json):
        for key, value in body_json.items():
            if key == 'power':
                if value == 'on':
                    self.power =True
                else:
                    self.power = False
                    self.heat = False
                    self.temperature = 30
                    self.shoulder = self.lumber = self.thighs = self.arms = MassageController.MODE_OFF
                    return

            elif key == 'heat':
                self.heat = value == 'on'
            elif key == 'temperature':
                self.temperature = int(value)

            else:
                MODE_MAP = {
                    'off': MassageController.MODE_OFF,
                    'low': MassageController.MODE_LOW,
                    'medium': MassageController.MODE_MEDIUM,
                    'high': MassageController.MODE_HIGH,
                }

                setattr(self, key, MODE_MAP[value])
                    
    
    def configure_massage_controller(self):
        if not self.power:
            self.massage_controller.off()
            return
          
        self.massage_controller.shoulder_massager(self.shoulder)
        self.massage_controller.lumber_massager(self.lumber)
        self.massage_controller.thighs_massager(self.thighs)
        self.massage_controller.arms_massager(self.arms)
    
    def configure_heat_controller(self):
        if not self.heat:
            self.heat_controller.off()
            return
            
        self.heat_controller.on(self.temperature)
        
    def parse_http_request(self, http_request):
        if not http_request:
            return
        lines = http_request.split(b'\r\n')
        method, path, version = lines[0].split(b' ')
        headers = {}
        body = ''
        for line in lines[1:]:
            if line == b'':
                break
            key, value = line.split(b': ')
            headers[key.decode('utf-8')] = value.decode('utf-8')
        content_length = int(headers.get('Content-Length', 0))
        try:
            if content_length > 0:
                body = http_request[-content_length:].decode('utf-8')
            body_json = json.loads(body)
        except:
            body_json = {}

        return method.decode('utf-8'), path.decode('utf-8'), version.decode('utf-8'), headers, body_json
            
    def application(self, client_socket,client_address, client_count):
        
        while True:
            try:
                http_request = client_socket.recv(1024)
                break
            except OSError as e:
                if e.errno != errno.EAGAIN:
                    raise

                time.sleep(0.1)
                continue
        method, path, _, _, body_json = self.parse_http_request(http_request)

        if method == 'GET' and path == '/':
            with open('index.html', 'rb') as f:
                file_contents = f.read()
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(file_contents)}\r\nConnection: close\r\nKeep-Alive: timeout=0\r\n\r\n"
            yield response_header.encode()
            chunk_size = 1024
            for i in range(0, len(file_contents), chunk_size):
                yield file_contents[i:i+chunk_size]
            return

        if method == 'GET' and path == '/favicon.ico':
            with open('favicon.ico', 'rb') as f:
                file_contents = f.read()
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\nCache-Control: public, max-age=31536000\r\nConnection: close\r\nKeep-Alive: timeout=0\r\n\r\n"
            yield response_header.encode()
            chunk_size = 1024
            for i in range(0, len(file_contents), chunk_size):
                yield file_contents[i:i+chunk_size]
            return

        if method == 'GET' and path == '/styles.css':
            with open('styles.css', 'rb') as f:
                file_contents = f.read()
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nCache-Control: public, max-age=31536000\r\nContent-Length: {len(file_contents)}\r\nConnection: close\r\nKeep-Alive: timeout=0\r\n\r\n"
            yield response_header.encode()
            chunk_size = 1024
            for i in range(0, len(file_contents), chunk_size):
                yield file_contents[i:i+chunk_size]
            return

        if method == 'GET' and path == '/script.js':
            with open('script.js', 'rb') as f:
                file_contents = f.read()
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: application/javascript\r\nCache-Control: public, max-age=31536000\r\nContent-Length: {len(file_contents)}\r\nConnection: close\r\nKeep-Alive: timeout=0\r\n\r\n"
            yield response_header.encode()
            chunk_size = 1024
            for i in range(0, len(file_contents), chunk_size):
                yield file_contents[i:i+chunk_size]
            return

        if method == 'GET' and path == '/parameters':
            MODE_MAP = {
                MassageController.MODE_OFF: 'off',
                MassageController.MODE_LOW: 'low',
                MassageController.MODE_MEDIUM: 'medium',
                MassageController.MODE_HIGH: 'high',
            }
            parameters = {
                'power' : 'on' if self.power else 'off',
                'heat': 'on' if self.heat else 'off',
                'temperature' : self.temperature,
                'shoulder' : MODE_MAP[self.shoulder],
                'lumber' : MODE_MAP[self.lumber],
                'thighs' : MODE_MAP[self.thighs],
                'arms' : MODE_MAP[self.arms]
            }
            response_body = json.dumps(parameters)
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\nKeep-Alive: timeout=0\r\n\r\n"
            yield response_header.encode()
            yield response_body.encode()
            return

        if method == 'PUT' and path == '/parameters':
            self.set_parameters(body_json)
            self.configure_massage_controller()
            self.configure_heat_controller()            
            data = {'status' : 'success', 'msg' : 'Applied Changes Successfully'} 
            response_body = json.dumps(data)
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\nConnection: close\r\nKeep-Alive: timeout=0\r\n\r\n"
            yield response_header.encode()
            yield response_body.encode()
            return
            
        
    def run(self):
        try:
            gc.collect()
            server = MicroServer()
            server.application = self.application
            server.serve()
        except Exception as e:
            print(e)
        finally:
            self.massage_controller.deinit()
            self.heat_controller.deinit()
        
        
        
