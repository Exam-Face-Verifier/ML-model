import subprocess
import os
from aspose import barcode
import cv2
import re
import matplotlib.pyplot as plt
import qrcode

def get_qr():
    req_ip = None
    
    try:
        if os.name == 'nt':
            output = subprocess.check_output("ipconfig", shell=True).decode("utf-8")
            for item in output.strip().split("\n"):
                if "IPv4 Address" in item or "IPv4 Address." in item:
                    req_ip = item.strip().split(":")[1].strip()
                    break
        else:  # Linux/Unix
            output = subprocess.check_output("ifconfig", shell=True).decode("utf-8")
            match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
            if match:
                req_ip = match.group(1)
                
        if not req_ip:
            raise ValueError("No IPv4 address found.")
        # print(f"Extracted IP: {req_ip}")

        generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.QR)
        generator.code_text = req_ip
        generator.parameters.barcode.x_dimension.pixels = 2.0
        generator.parameters.resolution = 128
        qr_path = "temp/Text_QR_Code.jpg"
        generator.save(qr_path)

        img = cv2.imread(qr_path)
        cv2.putText(img, 'Please scan using the app.', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        if os.name == 'nt':
            cv2.imshow("IP QR", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            os.system(f"catimg -w 64 -r 2 {qr_path}")

    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
