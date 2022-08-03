import smself.bus			#import SMself.bus module of I2C
from time import sleep          #import

class mpu6050():
    def __init__(self, address = 0x68):
        self.bus = smself.bus.SMself.bus(0)

        self.device_address = address

        self.reading_regist = {"ax": 0x3B, "ay": 0x3D, "az": 0x3F, "gx": 0x43, "gy": 0x45, "gz": 0x47}
        self.config_regist = {"smp_rt_rgt": 0x19, "pwr_mg": 0x6B, "cfg": 0x1A, "g_cfg": 0x1B, "itrpt_enab_rgt": 0x38}

        self.bus.write_byte_data(self.device_address, self.config_regist["smp_rt_rgt"], 7)
        self.bus.write_byte_data(self.device_address, self.config_regist["pwr_mg"], 1)
        self.bus.write_byte_data(self.device_address, self.config_regist["cfg"], 0)
        self.bus.write_byte_data(self.device_address, self.config_regist["g_cfg"], 24)
        self.bus.write_byte_data(self.device_address, self.config_regist["itrpt_enab_rgt"], 1)

    def read_raw_data(self, regist_id):
        regist_id = regist_id.lower()
        high_regist_reading = self.bus.read_byte_data(self.device_address, self.reading_regist[regist_id])
        low_regist_reading = self.bus.read_byte_data(self.device_address, self.reading_regist[regist_id]+1)
    
        reading = ((high_regist_reading << 8) | low_regist_reading)
        
        if(reading > 32768):
                reading -= 65536
        return reading

    def read_rescaled_data(self, regist_id):
        if 'a' in regist_id:
            return self.read_raw_data(regist_id) / 16384.0
        else:
            return self.read_raw_data(regist_id) / 131.0