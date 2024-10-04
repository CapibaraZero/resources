import csv
import os 
import json
from enum import Enum


class IRProtocol(Enum):
    UNKNOWN = 0
    # PULSE_WIDTH = 1
    # PULSE_DISTANCE = 2
    APPLE = 3
    DENON = 4
    JVC = 5
    # LG = 6
    # LG2 = 7
    NEC = 8
    NEC2 = 9
    # ONKYO = 10
    PANASONIC = 11
    # KASEIKYO
    # KASEIKYO_DENON
    # KASEIKYO_SHARP
    # KASEIKYO_JVC
    # KASEIKYO_MITSUBISHI
    RC5 = 17
    RC6 = 18
    # SAMSUNG
    # SAMSUNGLG
    # SAMSUNG48
    SHARP = 22
    SONY = 23
    # BANG_OLUFSEN
    BOSEWAVE = 25
    # LEGO_PF
    # MAGIQUEST
    # WHYNTER
    # FAST

# protocols = []

for root, dirs, files in os.walk("./irdb/codes"):
    for name in files:
        if name == "index" or name == "index.sh":
            continue
        converted_root = root.replace("irdb", "capibara_irdb")
        csv_file = root + '/' + name
        json_file = converted_root + "/" + name.replace(".csv", ".json")
        #print(json_file)
        #print(root.replace("irdb", "capibara_irdb"))
        if not os.path.isdir(converted_root):
            os.makedirs(converted_root)
        #print(name)
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            signals = []
            for row in reader:
                try:
                    # protocols.append(row["protocol"])
                    parsed_signal = {}
                    parsed_signal["name"] = row["functionname"]
                    protocol_raw = row["protocol"]
                    if protocol_raw == "Apple":
                        parsed_signal["protocol"] = IRProtocol.APPLE.value
                    elif "Denon" in protocol_raw :
                        parsed_signal["protocol"] = IRProtocol.DENON.value
                    elif "JVC" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.JVC.value
                    elif protocol_raw.lower() == "nec" or "NEC1" in protocol_raw or "NECx1" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.NEC.value
                    elif protocol_raw == "NEC2" or "NEC2" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.NEC2.value
                    elif "Panasonic" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.PANASONIC.value
                    elif"RC5" in  protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.RC5.value
                    elif "RC6" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.RC6.value
                    elif "Sharp" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.SHARP.value
                    elif "Sony" in protocol_raw:
                        parsed_signal["protocol"] = IRProtocol.SONY.value 
                    elif protocol_raw == "Bose":
                        parsed_signal["protocol"] = IRProtocol.BOSEWAVE.value
                    else:
                        continue
                    if row['subdevice'] != -1:
                        parsed_signal["address"] = (int(row['device']) << 8) | int(row['subdevice'])
                    else:
                        parsed_signal["address"] = int(row['device'])
                    parsed_signal["command"] = int(row['function'])
                   # print(parsed_signal)
                    signals.append(parsed_signal)
                except:
                    continue
            json_result = json.dumps(signals)
            f = open(json_file, "w")
            f.write(json_result)
            f.close()

# print(set(protocols))