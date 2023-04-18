from motor_driver import L298NSingleChannel

class HeatController:
    
    def __init__(self, HEAT_CONTROLLER_PINS):
        HEAT_CONTROLLER_CTRL1_PIN, HEAT_CONTROLLER_CTRL2_PIN, HEAT_CONTROLLER_TEMPERATURE_PIN = HEAT_CONTROLLER_PINS
        
        self.driver1 = L298NSingleChannel(HEAT_CONTROLLER_CTRL1_PIN, HEAT_CONTROLLER_CTRL2_PIN, HEAT_CONTROLLER_TEMPERATURE_PIN)
        
    
    def on(self, temperature):
        if temperature > 35:
            self.driver1.channel_a_clockwise(100)
        else:
            self.driver1.channel_a_clockwise(50)
        
    def off(self):
        self.driver1.deinit()