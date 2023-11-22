import glob
import cv2
import pathlib
import json
import os
import time

class scancode():

    def read_qr_code(filename,frame=""):
        """Read an image and read the QR code.
        
        Args:
            filename (string): Path to file
        
        Returns:
            qr (string): Value from QR code
        """
        
        try:
            #img = cv2.imread(filename)
            detect = cv2.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(frame)
            return value
        except:
            return

    def scanQrCode(txt):
        # define a video capture object
        vid = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            # Capture the video frame by frame
            ret, frame = vid.read()
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 
                    txt, 
                    (60, 60), 
                    font, 1, 
                    (0, 0, 255), 
                    2, 
                    cv2.LINE_4)
            
            # Display the resulting frame
            cv2.imshow('frame', frame)

            data, bbox, straight_qrcode = detector.detectAndDecode(frame)
            #print(data,bbox,straight_qrcode)
            if len(data) > 0:
                print(data)
                break
            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        return data


    def checkin_and_checkout_book(assetid,userid):
        print(assetid,userid)
    
    
        

# # import msvcrt
# if __name__ == "__main__":
#     while True:
#         print("press any key to log Asset against you, \'esc\' to Quit \n")
    
#         # else:
#         QrAsset = scanQrCode('Scan your Asset QR code, press \'q\' to exit')
#         QrSub = scanQrCode('Scan your User ID code, press \'q\' to exit')
#         print(QrAsset,QrSub)
#         # checkin_and_checkout_book(QrAsset,QrSub)