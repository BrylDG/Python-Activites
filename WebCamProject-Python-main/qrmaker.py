import qrcode
import numpy as np
from PIL import Image  # Ensure this import is present

class QRMaker:
    def create_qr(self,data:str):
        # Instantiate QRCode object
        qr = qrcode.QRCode(version=2, box_size=10, border=2)
        # Add data to the QR code
        qr.add_data(data)
        # Compile the data into a QR code array
        qr.make()
        # Print the image shape
        print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
        # Transfer the array into an actual image
        img = qr.make_image(fill_color="black", back_color="white")
        # Save it to a file
        img.save(f"static/images/studentimage/{data}.png")
