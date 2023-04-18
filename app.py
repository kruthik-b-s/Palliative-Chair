import gc, time
from massage_controller import MassageController
from heat_controller import HeatController
from microserver import MicroServer

class App:
    
    SHOULDER_MASSAGER_PINS = 4, 27, 32 # IN1, IN2, ENA -> Driver-1
    BACK_MASSAGER_PINS = 19, 21, 22    # IN3, IN4, ENB -> Driver-1
    LUMBER_MASSAGER_PINS = 13, 14, 18  # IN1, IN2, ENA -> Driver-2
    ARMS_MASSAGER_PINS = 23, 25, 26    # IN3, IN4, ENB -> Driver-2
    HEAT_CONTROLLER_PINS = 15, 16, 17  # IN1, IN2(RX2), ENA(TX2) -> Driver-3
    
    def __init__(self) :
        self.power = False
        self.heat = False
        self.temperature = 30
        self.shoulder = MassageController.MODE_OFF
        self.back = MassageController.MODE_OFF
        self.lumber = MassageController.MODE_OFF
        self.arms = MassageController.MODE_OFF
        self.massage_controller = MassageController(App.SHOULDER_MASSAGER_PINS, App.BACK_MASSAGER_PINS, App.LUMBER_MASSAGER_PINS, App.ARMS_MASSAGER_PINS)
        self.heat_controller = HeatController(App.HEAT_CONTROLLER_PINS)
    
    def html(self):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width" />
            <title>Palliative Chair</title>
            <link rel="stylesheet" href="styles.css">
          </head>
          <body>
            <header>
              <h1>Palliative Chair - Control Interface</h1>
            </header>
            <main>
              <section>
                <form method="POST">
                  <table>
                    <tbody>
                      <tr class="radial-shadow">
                        <td><span class="btn-name">Power :</span></td>
                        <td>
                          <div class="toggle_radio">
                            <input type="radio" class="toggle_option" id="power_first_toggle" name="power" value="off" {"" if self.power else "checked"} />
                            <input type="radio" class="toggle_option" id="power_second_toggle" name="power" value="on" {"checked" if self.power else ""} />
                            <label for="power_first_toggle"><p>OFF</p></label>
                            <label for="power_second_toggle"><p>ON</p></label>
                            <div class="toggle_option_slider"></div>
                          </div>
                        </td>
                      </tr>
                      <tr class="inset-shadow">
                        <td><span class="btn-name">Heat :</span></td>
                        <td>
                          <div class="toggle_radio">
                            <input type="radio" class="toggle_option" id="heat_first_toggle" name="heat" value="off" {"" if self.heat else "checked"} />
                            <input type="radio" class="toggle_option" id="heat_second_toggle" name="heat" value="on" {"checked" if self.heat else ""} />
                            <label for="heat_first_toggle"><p>OFF</p></label>
                            <label for="heat_second_toggle"><p>ON</p></label>
                            <div class="toggle_option_slider"></div>
                          </div>
                        </td>
                      </tr>
                      <tr class="inset-shadow">
                        <td><span class="btn-name">Temperature : <span id="temperature_placeholder"></span></span></td>
                        <td>
                          <div class="slidecontainer">
                            <input type="range" class="slider" id="temperature_input" min="25" max="40" name="temperature" value={self.temperature} >
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="form-group hard-shadow">
                    <p class="btn-name">Shoulder Massager Mode :</p>
                    <div class="toggle_radio">
                      <input type="radio" class="toggle_option" id="shoulder_first_toggle" name="shoulder" value="off" {"checked" if self.shoulder == MassageController.MODE_OFF else ""} />
                      <input type="radio" class="toggle_option" id="shoulder_second_toggle" name="shoulder" value="low" {"checked" if self.shoulder == MassageController.MODE_LOW else ""} />
                      <input type="radio" class="toggle_option" id="shoulder_third_toggle" name="shoulder" value="medium" {"checked" if self.shoulder == MassageController.MODE_MEDIUM else ""} />
                      <input type="radio" class="toggle_option" id="shoulder_fourth_toggle" name="shoulder" value="high" {"checked" if self.shoulder == MassageController.MODE_HIGH else ""} />
                      <label for="shoulder_first_toggle"><p>OFF</p></label>
                      <label for="shoulder_second_toggle"><p>LOW</p></label>
                      <label for="shoulder_third_toggle"><p>MEDIUM</p></label>
                      <label for="shoulder_fourth_toggle"><p>HIGH</p></label>
                      <div class="toggle_option_slider"></div>
                    </div>
                  </div>
                  <div class="form-group hard-shadow">
                    <p class="btn-name">Back Massager Mode :</p>
                    <div class="toggle_radio">
                      <input type="radio" class="toggle_option" id="back_first_toggle" name="back" value="off" {"checked" if self.back == MassageController.MODE_OFF else ""} />
                      <input type="radio" class="toggle_option" id="back_second_toggle" name="back" value="low" {"checked" if self.back == MassageController.MODE_LOW else ""} />
                      <input type="radio" class="toggle_option" id="back_third_toggle" name="back" value="medium" {"checked" if self.back == MassageController.MODE_MEDIUM else ""} />
                      <input type="radio" class="toggle_option" id="back_fourth_toggle" name="back" value="high" {"checked" if self.back == MassageController.MODE_HIGH else ""} />
                      <label for="back_first_toggle"><p>OFF</p></label>
                      <label for="back_second_toggle"><p>LOW</p></label>
                      <label for="back_third_toggle"><p>MEDIUM</p></label>
                      <label for="back_fourth_toggle"><p>HIGH</p></label>
                      <div class="toggle_option_slider"></div>
                    </div>
                  </div>
                  <div class="form-group hard-shadow">
                    <p class="btn-name">Lumber Massager Mode :</p>
                    <div class="toggle_radio">
                      <input type="radio" class="toggle_option" id="lumber_first_toggle" name="lumber" value="off" {"checked" if self.lumber == MassageController.MODE_OFF else ""} />
                      <input type="radio" class="toggle_option" id="lumber_second_toggle" name="lumber" value="low" {"checked" if self.lumber == MassageController.MODE_LOW else ""} />
                      <input type="radio" class="toggle_option" id="lumber_third_toggle" name="lumber" value="medium" {"checked" if self.lumber == MassageController.MODE_MEDIUM else ""} />
                      <input type="radio" class="toggle_option" id="lumber_fourth_toggle" name="lumber" value="high" {"checked" if self.lumber == MassageController.MODE_HIGH else ""} />
                      <label for="lumber_first_toggle"><p>OFF</p></label>
                      <label for="lumber_second_toggle"><p>LOW</p></label>
                      <label for="lumber_third_toggle"><p>MEDIUM</p></label>
                      <label for="lumber_fourth_toggle"><p>HIGH</p></label>
                      <div class="toggle_option_slider"></div>
                    </div>
                  </div>
                  <div class="form-group hard-shadow">
                    <p class="btn-name">Arms Massager Mode :</p>
                    <div class="toggle_radio">
                      <input type="radio" class="toggle_option" id="arms_first_toggle" name="arms" value="off" {"checked" if self.arms == MassageController.MODE_OFF else ""} />
                      <input type="radio" class="toggle_option" id="arms_second_toggle" name="arms" value="low" {"checked" if self.arms == MassageController.MODE_LOW else ""} />
                      <input type="radio" class="toggle_option" id="arms_third_toggle" name="arms" value="medium" {"checked" if self.arms == MassageController.MODE_MEDIUM else ""} />
                      <input type="radio" class="toggle_option" id="arms_fourth_toggle" name="arms" value="high" {"checked" if self.arms == MassageController.MODE_HIGH else ""} />
                      <label for="arms_first_toggle"><p>OFF</p></label>
                      <label for="arms_second_toggle"><p>LOW</p></label>
                      <label for="arms_third_toggle"><p>MEDIUM</p></label>
                      <label for="arms_fourth_toggle"><p>HIGH</p></label>
                      <div class="toggle_option_slider"></div>
                    </div>
                  </div>
                  <button type="submit" class="btn">Apply Changes</button>
                </form>
              </section>
            </main>
            <footer>
              <div>
                <p>Designed and Developed by :</p>
                <ul>
                  <li>Nikhil S</li>
                  <li>Kruthik B S</li>
                  <li>Sumanth K S</li>
                  <li>Sanjay C</li>
                </ul>
              </div>
              <div>
                <p>Special Thanks to:</p>
                <ul>
                  <li>Dr. Dattathreya (Sr. Prof. & Dean Planning, AIET)</li>
                  <li>Dr. Peter Fernandes (Prinicipal, AIET)</li>
                </ul>
                <p>For their Constant Support and Guidance</p>
              </div>
            </footer>
           <script src="script.js"></script>
          </body>
        </html>
        """
    
    def set_parameters(self, http_request):
        body_start = http_request.find(b'\r\n\r\n') + 4
        request_body = http_request[body_start:].decode('utf-8')
        
        if request_body:
            for param in request_body.split('&'):
                key, value = param.split('=')
        
                if key == 'power':
                    if value == 'on':
                        self.power =True
                    else:
                        self.power = False
                        self.heat = False
                        self.temperature = 30
                        self.shoulder = MassageController.MODE_OFF
                        self.back = MassageController.MODE_OFF
                        self.lumber = MassageController.MODE_OFF
                        self.arms = MassageController.MODE_OFF
                        return
                
                if key == 'heat':
                    if value == 'on':
                        self.heat = True
                    else:
                        self.heat = False
                
                if key == 'temperature':
                    self.temperature = int(value)
                        
                if key == 'shoulder':
                    if value == 'off':
                        self.shoulder = MassageController.MODE_OFF
                    elif value == 'low':
                        self.shoulder = MassageController.MODE_LOW
                    elif value == 'medium':
                        self.shoulder = MassageController.MODE_MEDIUM
                    elif value == 'high':
                        self.shoulder = MassageController.MODE_HIGH
                        
                if key == 'back':
                    if value == 'off':
                        self.back = MassageController.MODE_OFF
                    elif value == 'low':
                        self.back = MassageController.MODE_LOW
                    elif value == 'medium':
                        self.back = MassageController.MODE_MEDIUM
                    elif value == 'high':
                        self.back = MassageController.MODE_HIGH
                        
                if key == 'lumber':
                    if value == 'off':
                        self.lumber = MassageController.MODE_OFF
                    elif value == 'low':
                        self.lumber = MassageController.MODE_LOW
                    elif value == 'medium':
                        self.lumber = MassageController.MODE_MEDIUM
                    elif value == 'high':
                        self.lumber = MassageController.MODE_HIGH
                        
                if key == 'arms':
                    if value == 'off':
                        self.arms = MassageController.MODE_OFF
                    elif value == 'low':
                        self.arms = MassageController.MODE_LOW
                    elif value == 'medium':
                        self.arms = MassageController.MODE_MEDIUM
                    elif value == 'high':
                        self.arms = MassageController.MODE_HIGH
                    
    
    def configure_massage_controller(self):
        if not self.power:
            self.massage_controller.off()
            return
          
        self.massage_controller.shoulder_massager(self.shoulder)
        self.massage_controller.back_massager(self.back)
        self.massage_controller.lumber_massager(self.lumber)
        self.massage_controller.arms_massager(self.arms)
    
    def configure_heat_controller(self):
        if not self.heat:
            self.heat_controller.off()
            return
            
        self.heat_controller.on(self.temperature)
            
    def application(self, client_socket,client_address, client_count):
        
        while True:
            try:
                http_request = client_socket.recv(1024)
                break
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    time.sleep(0.1)
                    continue
                else:
                    raise
                
        if http_request.find(b'GET /favicon.ico') > -1:
            with open('favicon.ico', 'rb') as f:
                file_contents = f.read()
            response = f"HTTP/1.1 200 OK\nContent-Type: image/x-icon\nCache-Control: public, max-age=31536000\nConnection: close\nKeep-Alive: timeout=0\n\n"
            yield response.encode() + file_contents
            return
        
        if http_request.find(b'GET /styles.css') > -1:
            with open('styles.css', 'rb') as f:
                file_contents = f.read()
            response = f"HTTP/1.1 200 OK\nContent-Type: text/css\nCache-Control: public, max-age=31536000\nContent-Length: {len(file_contents)}\nConnection: close\nKeep-Alive: timeout=0\n\n"
            yield response.encode() + file_contents
            return
        
        if http_request.find(b'GET /script.js') > -1:
            with open('script.js', 'rb') as f:
                file_contents = f.read()
            response = f"HTTP/1.1 200 OK\nContent-Type: application/javascript\nCache-Control: public, max-age=31536000\nContent-Length: {len(file_contents)}\nConnection: close\nKeep-Alive: timeout=0\n\n"
            yield response.encode() + file_contents
            return
            
        self.set_parameters(http_request)
#         print(self.power, self.heat, self.temperature, self.shoulder, self.back, self.lumber, self.arms)
        
        self.configure_massage_controller()
        self.configure_heat_controller()
        
        content_length = sum(len(element.encode('utf-8')) for element in (line.strip() for line in self.html().split('\n')))
        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {content_length}\nConnection: close\nKeep-Alive: timeout=0\n\n"
        yield response.encode()
        data = (line.strip() for line in self.html().split('\n'))
        for fragment in data:
            yield fragment.encode()
        
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
        
        
        
