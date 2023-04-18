from motor_driver import L298N

class MassageController:
    
    MODE_OFF = 0
    MODE_LOW = 70
    MODE_MEDIUM = 85
    MODE_HIGH = 100
    
    def __init__(self, shoulder_massager_pins, back_massager_pins, lumber_massager_pins, arms_massager_pins):
        self.driver1 = L298N(*shoulder_massager_pins, *back_massager_pins)
        self.driver2 = L298N(*lumber_massager_pins, *arms_massager_pins)
    
    
    def shoulder_massager(self, mode):
        if mode == MassageController.MODE_OFF:
            self.driver1.channel_a_off()
            return
        
        self.driver1.channel_a_clockwise(mode)
    
    
    def back_massager(self, mode):
        if mode == MassageController.MODE_OFF:
            self.driver1.channel_b_off()
            return
        
        self.driver1.channel_b_clockwise(mode)
    
    
    def lumber_massager(self, mode):
        if mode == MassageController.MODE_OFF:
            self.driver2.channel_a_off()
            return
        
        self.driver2.channel_a_clockwise(mode)
    
    
    def arms_massager(self, mode):
        if mode == MassageController.MODE_OFF:
            self.driver2.channel_b_off()
            return
        
        self.driver2.channel_b_clockwise(mode)
        
    
    def off(self):
        self.driver1.channel_a_off()
        self.driver1.channel_b_off()
        self.driver2.channel_a_off()
        self.driver2.channel_b_off()
    
    
    def deinit(self):
        self.driver1.deinit()
        self.driver2.deinit()
        