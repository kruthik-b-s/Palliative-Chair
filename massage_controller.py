from motor_driver import L298N

class MassageController:
    
    MODE_OFF = 'MODE_OFF'
    MODE_LOW = 70
    MODE_MEDIUM = 85
    MODE_HIGH = 100
    
    def __init__(self, SHOULDER_MASSAGER_PINS, BACK_MASSAGER_PINS, LUMBER_MASSAGER_PINS, ARMS_MASSAGER_PINS):
        
        SHOULDER_MASSAGER_CTRL1_PIN, SHOULDER_MASSAGER_CTRL2_PIN, SHOULDER_MASSAGER_INTENSITY_PIN = SHOULDER_MASSAGER_PINS
        BACK_MASSAGER_CTRL1_PIN, BACK_MASSAGER_CTRL2_PIN, BACK_MASSAGER_INTENSITY_PIN = BACK_MASSAGER_PINS
        LUMBER_MASSAGER_CTRL1_PIN, LUMBER_MASSAGER_CTRL2_PIN, LUMBER_MASSAGER_INTENSITY_PIN = LUMBER_MASSAGER_PINS
        ARMS_MASSAGER_CTRL1_PIN, ARMS_MASSAGER_CTRL2_PIN, ARMS_MASSAGER_INTENSITY_PIN = ARMS_MASSAGER_PINS
        
        self.driver1 = L298N(SHOULDER_MASSAGER_CTRL1_PIN, SHOULDER_MASSAGER_CTRL2_PIN, SHOULDER_MASSAGER_INTENSITY_PIN, BACK_MASSAGER_CTRL1_PIN, BACK_MASSAGER_CTRL2_PIN, BACK_MASSAGER_INTENSITY_PIN)
        self.driver2 = L298N(LUMBER_MASSAGER_CTRL1_PIN, LUMBER_MASSAGER_CTRL2_PIN, LUMBER_MASSAGER_INTENSITY_PIN, ARMS_MASSAGER_CTRL1_PIN, ARMS_MASSAGER_CTRL2_PIN, ARMS_MASSAGER_INTENSITY_PIN)
    
    
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
        self.driver1.deinit()
        self.driver2.deinit()
        