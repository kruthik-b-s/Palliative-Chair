from motor_driver import L298NSingleChannel

class HeatController:
    
    def __init__(self, heat_controller_pins):        
        self.driver1 = L298NSingleChannel(*heat_controller_pins)
        
    def on(self, temperature):
        if temperature > 35:
            self.driver1.channel_a_clockwise(100)
        else:
            self.driver1.channel_a_clockwise(50)
        
    def off(self):
        self.driver1.channel_a_off()
        
    def deinit(self):
        self.driver1.deinit()