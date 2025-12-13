#import struct

class oneSatData:
    def __init__(self, prn = 0, elevation = 0, azimuth = 0, snr = 0):
        self.prn = prn
        self.elevation = elevation
        self.azimuth = azimuth
        self.snr = snr
    def returnCSV(self):
        return f'{self.prn},{self.elevation},{self.azimuth},{self.snr}'

class lineData:
    def __init__(self,timestamp = 0, constellation: str = 'GX', data_list: list[oneSatData] | None = None):
        self.timestamp = timestamp
        self.constellation = constellation
        self.data_list = data_list if data_list is not None else []
    def returnCSV(self):
        sat_data_str = ",".join([data.returnCSV() for data in self.data_list])
        CSVStr = f'{self.timestamp},{self.constellation},{sat_data_str}\n'
        return CSVStr
    def display(self):
        print(self.returnCSV())


'''
class Data:
    #SYNC_BYTE = 0xAA

    def __init__(self, timestamp, ax, ay, az, gx, gy, gz):
        self.timestamp = timestamp
        self.ax = ax
        self.ay = ay
        self.az = az
        self.gx = gx
        self.gy = gy
        self.gz = gz

    def display(self):
        CSVString = f"{self.timestamp}, {self.ax}, {self.ay}, {self.az}, {self.gx}, {self.gy}, {self.gz}"
        print(CSVString)

    def returnCSV(self):
        return f"{self.timestamp}, {self.ax:.1f}, {self.ay:.1f}, {self.az:.1f}, {self.gx:.1f}, {self.gy:.1f}, {self.gz:.1f}\n"

    @classmethod
    def fromBytes(cls, data):
        calculated_checksum = sum(data[:-1]) & 0xFF
        received_checksum = data[-1]

        if calculated_checksum != received_checksum:
            #print(f"Checksum mismatch! Calc: {calculated_checksum}, Recv: {received_checksum}")
            return False
        try:
            unpacked = struct.unpack(cls.FORMAT, data)
            return cls(unpacked[1], unpacked[2], unpacked[3], unpacked[4], unpacked[5], unpacked[6], unpacked[7])
        except struct.error:
            return False
    
        
class OtherSensorsData:
    FORMAT = '<BI3f?fB'
    SIZE = 23
    SYNC_BYTE = 0x55

    def __init__(self, timestamp, temperature, pressure, altitute, moisture, isDry):
        self.timestamp = timestamp
        self.temperature = temperature
        self.pressure = pressure
        self.altitute = altitute
        self.moisture = moisture
        self.isDry = isDry
    
    def display(self):
        print(f"{self.timestamp}, {self.temperature}, {self.pressure}, {self.altitute}, {self.moisture}, {self.isDry}")
    
    def returnCSV(self):
        return f"{self.timestamp}, {self.temperature:.1f}, {self.pressure:.1f}, {self.altitute:.1f}, {self.moisture:.1f}, {self.isDry}\n"

    @classmethod
    def fromBytes(cls, data):
        calculated_checksum = sum(data[:-1]) & 0xFF
        received_checksum = data[-1]

        if calculated_checksum != received_checksum:
            #print(f"Checksum mismatch! Calc: {calculated_checksum}, Recv: {received_checksum}")
            return False

        try:
            unpacked = struct.unpack(cls.FORMAT, data)
            return cls(unpacked[1], unpacked[2], unpacked[3], unpacked[4], unpacked[5], unpacked[6])
        except struct.error:
            return False
'''