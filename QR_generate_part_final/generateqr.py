import pyqrcode 
import png 
from pyqrcode import QRCode 
  

def generate_qr(qrtext,filetype):
    # String which represents the QR code 
    s = qrtext
    
    # Generate QR code 
    url = pyqrcode.create(s) 
    
    # Create and save the svg file naming "myqr.svg" 
    # url.svg("myqr.svg", scale = 8) 
    
    # segregate file as per type " Asset/ Employee"
    list_msg=qrtext.split(',')

    if filetype == 'employee':
        QrFileName = "EmployeeQr/Emp_{0}-{1}.png".format(list_msg[0],list_msg[1])
    elif filetype == 'asset':
        QrFileName = "AssetQr/Asset_{0}-{1}.png".format(list_msg[0],list_msg[1])

    # Create and save the png file naming "myqr.png" 
    url.png(QrFileName, scale = 6)


import csv

def read_csv_file(file_name,file_type):
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file,)
        i=0
        qr_content = []
        for lines in csvFile:
            if i==0:
                i=1
                continue
        
            qrtext = ",".join(list(map(evaluate,str(lines)[1:-1].split(','))))
            generate_qr(qrtext,file_type)
            qr_content.append(qrtext)

    print(qr_content)

def evaluate(n):
    return eval(n)


read_csv_file('asset.csv','asset')
read_csv_file('users.csv','employee')