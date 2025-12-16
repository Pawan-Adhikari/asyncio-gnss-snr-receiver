import asyncio
import serial
import pynmea2
from packets.structs import lineData, oneSatData
import time
from CircularQueue.AsyncCircularQueue import AsyncCircularQueue


async def serialRead(GPQueue: AsyncCircularQueue , GLQueue: AsyncCircularQueue, SERIAL, sample_count, ProcessQueueGP, ProcessQueueGL):
    while True:
        port_name = SERIAL    
        print(f"Connecting to serial port: {port_name}")

        while True:
            try:
                ser = serial.Serial(port_name, 115200, timeout=0.1)
                print(f"Connected to serial port: {port_name}")
                break
            except serial.SerialException as e:
                print(f"Serial Error: {e}")
                print("Attempting to reconnect in 2s")
                await asyncio.sleep(2)

        loop = asyncio.get_running_loop()
        GPLineData = lineData(constellation="GP")
        GLLineData = lineData(constellation="GL")
        lastPushTimestamp_GP = 0
        lastPushTimestamp_GL = 0
        while True:
            try:
                raw_line = await loop.run_in_executor(None, ser.readline)
                line = raw_line.decode('ascii', errors='ignore').strip()

                if line.startswith('$GPGSV'):
                    msg = pynmea2.parse(line)

                    #CONVERSION TO DICTIONARY
                    #msg is of type QuerySentence.
                    #Every pynmea class has .fields which can be used to contruct dictinary out of the sentences
                    #.fields returns this format:
                    #(('Number of messages of type in cycle', 'num_messages'), ('Message Number', 'msg_num'), ('Total number of SVs in view', 'num_sv_in_view'), ('SV PRN number 1', 'sv_prn_num_1'), ('Elevation in degrees 1', 'elevation_deg_1'), ('Azimuth, deg from true north 1', 'azimuth_1'), ('SNR 1', 'snr_1'), ('SV PRN number 2', 'sv_prn_num_2'), ('Elevation in degrees 2', 'elevation_deg_2'), ('Azimuth, deg from true north 2', 'azimuth_2'), ('SNR 2', 'snr_2'), ('SV PRN number 3', 'sv_prn_num_3'), ('Elevation in degrees 3', 'elevation_deg_3'), ('Azimuth, deg from true north 3', 'azimuth_3'), ('SNR 3', 'snr_3'), ('SV PRN number 4', 'sv_prn_num_4'), ('Elevation in degrees 4', 'elevation_deg_4'), ('Azimuth, deg from true north 4', 'azimuth_4'), ('SNR 4', 'snr_4'))
                    #so we need the second entry of each field tuple in fields

                    msg_dict = {field[1]: getattr(msg, field[1]) for field in msg.fields}
                    #print(msg.fields)
                    #print(msg_dict)

                    for i in range (1,5):
                        prn = int(msg_dict[f'sv_prn_num_{i}'] or 0)
                        elevation = int(msg_dict[f'elevation_deg_{i}'] or 0)
                        azimuth = int(msg_dict[f'azimuth_{i}'] or 0)
                        snr = int(msg_dict[f'snr_{i}'] or 0)

                        currentOneSatData = oneSatData(prn, elevation, azimuth, snr)
                        
                        if currentOneSatData.elevation > 15:
                            GPLineData.data_list.append(currentOneSatData)

                    if msg_dict['num_messages'] == msg_dict['msg_num']:
                        GPLineData.timestamp = int(time.time())
                        
                        if GPLineData.timestamp - lastPushTimestamp_GP >= sample_count:
                            await GPQueue.put(GPLineData)
                            ProcessQueueGP.put(GPLineData)
                            lastPushTimestamp_GP = int(time.time())
                        GPLineData = lineData(constellation="GP")
                        

                #print(f"DEBUG: {line}") 
                if line.startswith('$GLGSV'):
                    msg = pynmea2.parse(line)

                    #CONVERSION TO DICTIONARY
                    #msg is of type QuerySentence.
                    #Every pynmea class has .fields which can be used to contruct dictinary out of the sentences
                    #.fields returns this format:
                    #(('Number of messages of type in cycle', 'num_messages'), ('Message Number', 'msg_num'), ('Total number of SVs in view', 'num_sv_in_view'), ('SV PRN number 1', 'sv_prn_num_1'), ('Elevation in degrees 1', 'elevation_deg_1'), ('Azimuth, deg from true north 1', 'azimuth_1'), ('SNR 1', 'snr_1'), ('SV PRN number 2', 'sv_prn_num_2'), ('Elevation in degrees 2', 'elevation_deg_2'), ('Azimuth, deg from true north 2', 'azimuth_2'), ('SNR 2', 'snr_2'), ('SV PRN number 3', 'sv_prn_num_3'), ('Elevation in degrees 3', 'elevation_deg_3'), ('Azimuth, deg from true north 3', 'azimuth_3'), ('SNR 3', 'snr_3'), ('SV PRN number 4', 'sv_prn_num_4'), ('Elevation in degrees 4', 'elevation_deg_4'), ('Azimuth, deg from true north 4', 'azimuth_4'), ('SNR 4', 'snr_4'))
                    #so we need the second entry of each field tuple in fields

                    msg_dict = {field[1]: getattr(msg, field[1]) for field in msg.fields}
                    #print(msg.fields)
                    #print(msg_dict)

                    for i in range (1,5):
                        prn = int(msg_dict[f'sv_prn_num_{i}'] or 0)
                        elevation = int(msg_dict[f'elevation_deg_{i}'] or 0)
                        azimuth = int(msg_dict[f'azimuth_{i}'] or 0)
                        snr = int(msg_dict[f'snr_{i}'] or 0)

                        currentOneSatData = oneSatData(prn, elevation, azimuth, snr)

                        if currentOneSatData.elevation > 15:
                            GLLineData.data_list.append(currentOneSatData)

                    if msg_dict['num_messages'] == msg_dict['msg_num']:
                        GLLineData.timestamp = int(time.time())
                        #GLLineData.display()
                        if GLLineData.timestamp - lastPushTimestamp_GL >= sample_count:
                            await GLQueue.put(GLLineData)
                            ProcessQueueGL.put(GLLineData)
                            lastPushTimestamp_GL = int(time.time())
                        GLLineData = lineData(constellation="GL")



            except serial.SerialException as e:
                print('Device error: {}'.format(e))
                print('Trying to reconnect in 5seconds')
                await asyncio.sleep(5)
                break
            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                continue
