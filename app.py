import gc, time
from nettools import start_access_point
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
        self.massage_controller = None
        self.heat_controller = None
    
    def html(self):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width" />
            <title>Palliative Chair</title>
            <style>
              *,
              *::after,
              *::before {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
              }}
              :root {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 16px;
              }}
              .hard-shadow {{
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
              }}
              .inset-shadow {{
                box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.5);
              }}
              .radial-shadow {{
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 0, 0, 0.2), 0 0 30px rgba(0, 0, 0, 0.1);
              }}
              body {{
                width: max-content;
                min-height: 100vh;
                margin: 0 auto;
                padding: 2rem;
                background-color: #333;
                color: #eee;
              }}
              h1 {{
                font-size: 1.5rem;
                text-align: center;
                padding: 1rem;
                font-weight: bolder;
                font-style: italic;
                text-decoration: underline;
              }}
              main {{
                margin: 1rem 0;
                padding: 0 1rem;
                border-bottom: 1px solid #ccc;
                padding-bottom: 20px;
              }}
              form {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 2rem;
              }}
              table {{
                border-spacing: 2rem;
                border-collapse: separate;
              }}
              td {{
                padding: 1rem 2rem;
              }}
              .btn-name {{
                font-size: 1rem;
                font-weight: 500;
              }}
              .form-group {{
                display: flex;
                flex-direction: column;
                padding: 1rem;
                gap: 1rem;
              }}
              .slidecontainer {{
                width: 100%;
              }}
              .slider {{
                -webkit-appearance: none;
                appearance: none;
                width: 100%;
                height: 15px;
                border-radius: 5px;  
                background: #d3d3d3;
                outline: none;
                opacity: 0.7;
                -webkit-transition: .2s;
                transition: opacity .2s;
              }}
              .slider:hover {{
                opacity: 1;
              }}
              .slider::-webkit-slider-thumb {{
                -webkit-appearance: none;
                appearance: none;
                width: 25px;
                height: 25px;
                border-radius: 50%;
                background: #04AA6D;
                cursor: pointer;
              }}
              .slider::-moz-range-thumb {{
                width: 25px;
                height: 25px; 
                background: #04AA6D;
                cursor: pointer;
              }}
              .toggle_radio {{
                position: relative;
                background: rgba(255, 255, 255, 0.1);
                margin: 4px auto;
                overflow: hidden;
                padding: 0 !important;
                -webkit-border-radius: 50px;
                -moz-border-radius: 50px;
                border-radius: 50px;
                position: relative;
                height: 26px;
                width: fit-content;
              }}
              .toggle_radio > * {{
                float: left;
              }}
              .toggle_radio input[type='radio'] {{
                display: none;
              }}
              .toggle_radio label {{
                font-size: 0.75rem;
                color: rgba(255, 255, 255, 0.9);
                z-index: 0;
                display: block;
                width: 100px;
                height: 20px;
                margin: 3px 3px;
                -webkit-border-radius: 50px;
                -moz-border-radius: 50px;
                border-radius: 50px;
                cursor: pointer;
                z-index: 1;
                text-align: center;
              }}
              .toggle_option_slider {{
                width: 100px;
                height: 20px;
                position: absolute;
                top: 3px;
                -webkit-border-radius: 50px;
                -moz-border-radius: 50px;
                border-radius: 50px;
                -webkit-transition: all 0.4s ease;
                -moz-transition: all 0.4s ease;
                -o-transition: all 0.4s ease;
                -ms-transition: all 0.4s ease;
                transition: all 0.4s ease;
              }}
              #power_first_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 3px;
              }}
              #power_second_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 109px;
              }}
              #heat_first_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 3px;
              }}
              #heat_second_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 109px;
              }}
              #shoulder_first_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 3px;
              }}
              #shoulder_second_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 109px;
              }}
              #shoulder_third_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 215px;
              }}
              #shoulder_fourth_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 322px;
              }}
              #back_first_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 3px;
              }}
              #back_second_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 109px;
              }}
              #back_third_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 215px;
              }}
              #back_fourth_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 322px;
              }}
              #lumber_first_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 3px;
              }}
              #lumber_second_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 109px;
              }}
              #lumber_third_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 215px;
              }}
              #lumber_fourth_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 322px;
              }}
              #arms_first_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 3px;
              }}
              #arms_second_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 109px;
              }}
              #arms_third_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 215px;
              }}
              #arms_fourth_toggle:checked ~ .toggle_option_slider {{
                background: rgba(255, 255, 255, 0.3);
                left: 322px;
              }}
              .btn {{
                margin-top: 2rem;
                padding: 1rem;
                border: none;
                outline: none;
                font-size: 1rem;
                font-weight: bold;
                border-radius: 50px;
                box-shadow: -10px -10px 30px rgba(255, 255, 255, 0.05), 10px 10px 30px rgba(0, 0, 0, 0.15);
              }}
              .btn:hover,
              .btn:focus {{
                cursor: pointer;
                background-color: green;
                color: #ddd;
              }}
              footer {{
                display: flex;
                flex-direction: column;
                gap: 1.5rem;
              }}
              footer ul {{
                list-style: none;
                margin: 0.5rem 0;
              }}
            </style>
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
           <script>
              const powerbtns = document.querySelectorAll('input[type="radio"][name="power"]');
              const heatbtns = document.querySelectorAll('input[type="radio"][name="heat"]');
              const otherbtns = Array.prototype.slice.call(document.querySelectorAll('input'), 2);
              const offbtns = document.querySelectorAll('input[value="off"]');
              const temperature_input = document.getElementById('temperature_input');
              const temperature_placeholder = document.getElementById('temperature_placeholder');
              temperature_placeholder.innerText = temperature_input.value;
              temperature_input.addEventListener('input', e => temperature_placeholder.innerText = e.target.value);
              if (powerbtns[0].checked) {{
                for (let i = 0; i < otherbtns.length; i++) {{
                  otherbtns[i].disabled = true;
                }}
              }}
              powerbtns.forEach(function (powerbtn) {{
                powerbtn.addEventListener('click', function () {{
                  if (this.value === 'off') {{
                    for (let i = 0; i < otherbtns.length; i++) {{
                      otherbtns[i].disabled = true;
                    }}
                    offbtns.forEach(btn => btn.checked = true);
                  }} else if (this.value === 'on') {{
                    for (let i = 0; i < otherbtns.length; i++) {{
                      if (otherbtns[i].type !== 'range')
                        otherbtns[i].disabled = false;
                    }}
                  }}
                }});
              }});
              heatbtns.forEach(function (heatbtn) {{
                heatbtn.addEventListener('click', function () {{
                  if (this.value === 'off') {{
                    temperature_input.disabled = true;
                  }} else if (this.value === 'on') {{
                    temperature_input.disabled = false;
                  }}
                }});
              }});
            </script>
          </body>
        </html>
        """
    
    def set_parameters(self, parameters_dict):
        for key, value in parameters_dict.items():
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
                    
    def get_parameters_dict(self, http_request):
        
        body_start = http_request.find(b'\r\n\r\n') + 4
        request_body = http_request[body_start:].decode('utf-8')
        parameters_dict = {}
        
        if request_body:
            for param in request_body.split('&'):
                key, value = param.split('=')
                parameters_dict[key] = value
        
        return parameters_dict
    
    def configure_massage_controller(self):
        if self.power == False and self.massage_controller != None:
            self.massage_controller.off()
            self.massage_controller = None
            return
        
        if self.power:
            if self.massage_controller is None:
                self.massage_controller = MassageController(App.SHOULDER_MASSAGER_PINS, App.BACK_MASSAGER_PINS, App.LUMBER_MASSAGER_PINS, App.ARMS_MASSAGER_PINS)
            
            self.massage_controller.shoulder_massager(self.shoulder)
            self.massage_controller.back_massager(self.back)
            self.massage_controller.lumber_massager(self.lumber)
            self.massage_controller.arms_massager(self.arms)
    
    def configure_heat_controller(self):
        if self.heat == False and self.heat_controller != None:
            self.heat_controller.off()
            self.heat_controller = None
            return
        
        if self.heat:
            if self.heat_controller is None:
                self.heat_controller = HeatController(App.HEAT_CONTROLLER_PINS)
            
            self.heat_controller.on(self.temperature)
            
            
            

    def application(self, client_socket,client_address, client_count):
        
        while True:
            try:
                http_request = client_socket.recv(2048)
                break
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    time.sleep(0.1)
                    continue
                else:
                    raise
            
        is_favicon_request = http_request.find(b'GET /favicon.ico') > -1
        
        if is_favicon_request:
            response = b'HTTP/1.1 200 OK\nContent-Type: image/x-icon\nConnection: close\nKeep-Alive: timeout=0\n\n'
            with open('favicon.ico', 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    response += chunk
            yield response
            return
            
        parameters_dict = self.get_parameters_dict(http_request)
        self.set_parameters(parameters_dict)
#         print(parameters_dict)
#         print(self.power, self.heat, self.temperature, self.shoulder, self.back, self.lumber, self.arms)
        
        self.configure_massage_controller()
        self.configure_heat_controller()
        
        content_length = sum(len(element.encode('utf-8')) for element in (line.strip() for line in self.html().split('\n')))
        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: {content_length}\nConnection: close\nKeep-Alive: timeout=0\n\n"
        yield bytes(response,'utf-8')
        gc.collect()
        data = (line.strip() for line in self.html().split('\n'))
        for fragment in data:
            yield bytes(fragment,'utf-8')
        

    def run(self):
        gc.collect()
        start_access_point()
        server = MicroServer()
        server.application = self.application
        server.serve()
        
        
