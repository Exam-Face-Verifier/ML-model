import subprocess
from aspose import barcode
import cv2

def get_qr():
    output = subprocess.check_output("ipconfig", shell=True)
    output = output.decode("utf-8")
    req_ip = ""


    for item in output.strip().split("\n"):
        if "IPv4 Address" in item:
            req_ip = item.strip().split(":")[1].strip()
            break
        
    generator = barcode.generation.BarcodeGenerator(barcode.generation.EncodeTypes.QR)
    generator.code_text = req_ip
    generator.parameters.barcode.x_dimension.pixels = 8.0
    generator.parameters.resolution = 512.0

    generator.save("Text_QR_Code.jpg")

    img = cv2.imread("Text_QR_Code.jpg")
    cv2.putText(img, 'Please scan using the app.', (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    cv2.imshow("IP QR",img)
    cv2.waitKey(0)
