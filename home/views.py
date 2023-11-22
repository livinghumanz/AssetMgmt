from django.shortcuts import render,redirect
from django.http import request, HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib import messages
from datetime import date,datetime
from .models import Asset,Employee,In_Out_log
import smtplib
import csv

# Create your views here.

def home(request):
    asset_dic = dict(Asset.objects.values_list("asset_id","asset_name"))
    checkedIn = []
    for assetid in list(asset_dic.keys()):
        ad={}
        res = list(In_Out_log.objects.all().filter(return_date=None,asset=assetid))

        if len(res)>0:
            ad['assetid'] = assetid
            ad['asset_name'] = res[0].asset.asset_name
            ad['in_out_status'] = 'Out of Campus'
            ad['holder'] = "{0} : {1}".format(res[0].emp.emp_id,res[0].emp.emp_name)
            ad['color_s'] = 'red'
        elif len(res)==0:
            ad['assetid'] = assetid
            ad['asset_name'] = asset_dic[assetid]
            ad['in_out_status'] = 'inside Campus'
            ad['holder'] = "NA"
            ad['color_s'] = 'green'

        checkedIn.append(ad)
    print(checkedIn)

    return render(request,'home/home.html',{'result_list1':checkedIn})


def uploadFile(request):
    if request.method =='POST':
        upload_type = request.POST['upload']
        if upload_type == 'hardware':
            if request.FILES:
                hardware_csv = request.FILES['hardware-d0']

                if hardware_csv.name.split(".")[-1] != 'csv':
                    messages.error(request,"please upload a valid \".csv\" file !")
                    return render(request,'home/file_upload.html')

                # continue with the flow if the file is csv ... 
                status = updateDb(hardware_csv.read().decode('utf-8').splitlines(),'asset')

                if status == False:
                    messages.error(request,"please upload a valid \".csv\" file, DB not updated !")
                    return render(request,'home/file_upload.html')


        elif upload_type == 'userlist':
            if request.FILES:
                user_csv = request.FILES['userlist-d0']

                if user_csv.name.split(".")[-1] != 'csv':
                    messages.error(request,"please upload a valid \".csv\" file !")
                    return render(request,'home/file_upload.html')

                # continue with the flow if the file is csv ... 
                status = updateDb(user_csv.read().decode('utf-8').splitlines(),'employee')

                if status == False:
                    messages.error(request,"please upload a valid \".csv\" file, DB not updated !")
                    return render(request,'home/file_upload.html')

                
        messages.success(request,"Data propogated successfully !")
    return render(request,'home/file_upload.html')


def testApi(request):
    if request.method =='POST':
        assetid = request.POST['assetid']
        res = list(In_Out_log.objects.all().filter(asset=assetid))
        message_str = '''Asset_id, Asset_name,Asset_Description,Employee_id,Employee_name,Employee_contact,check_in_date,return_date
        
        '''
        final_dump =[]
        for ele in res:
            res1=[]
            res1.append(ele.asset.asset_id)
            res1.append(ele.asset.asset_name)
            res1.append(ele.asset.asset_description)
            res1.append(ele.emp.emp_id)
            res1.append(ele.emp.emp_name)
            res1.append(ele.emp.contact)
            res1.append(ele.checkin_date)
            res1.append(ele.return_date)
            final_dump.append(res1)
            message_str+='''{0}
            '''.format(str(res1)[1:-1])
        



        print(str(final_dump))
        sendmail(message_str)


        # 

        response= HttpResponse(content_type = 'text/csv')
        writer = csv.writer(response)
        writer.writerow(['Asset_id','Asset_name','Asset_Description','Employee_id','Employee_name','Employee_contact','check_in_date','return_date'])
        
        for entry in final_dump:
            '''entry1= list(entry)
            entry1[3]='hello'
            entry=tuple(entry1)
            print(entry)'''
            writer.writerow(entry)
        
        response['Content-Disposition'] = 'attachment; filename="Asset_{0}_Report.csv"'.format(assetid)

        messages.success(request,"report sent !!!")
        return response


        # 

        # return redirect("/")

    return JsonResponse({'clientid_dev':'AQnB1lWbzIOqujprqVab7od6EY_j1fGpAE6CvPromEGYmOXYXVsH-Wqhq-n4jNWpLcIWu3zVX7RMQoi2','assetid':assetid})


def updateDb(csv_file,tablename):
    # with open(csv_file,'r') as csvfile:
    reader = csv.DictReader(csv_file)
    try:
        for row in reader:
            
            if tablename == 'employee':
                # print(row['id'],row['name'],row['contact'],row['location'])
                Employee.objects.create(emp_id=row['id'],emp_name=row['name'],contact=row['contact'],work_location=row['location'])

            if tablename == 'asset':
                # print(row['id'],row['name'],row['description'],row['location'])
                Asset.objects.create(asset_id=row['id'],asset_name=row['name'],asset_description=row['description'],base_location=row['location'])
            
        return True
    except:
        return False

    # csvfile.close()
    
def sendmail(message):
    # pass
 
    # list of email_id to send the mail
    li = ["efgh66666666@gmail.com"]
    
    for dest in li:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("lucytherobo@gmail.com", "locv kdfs taxf iukn")
        message = "Subject: {0}\n\n{1}".format('Report of Asset 111',message)
        s.sendmail("lucytherobo@gmail.com", dest, message)
        s.quit()


def log_checkin_out(request):

    from .qrcode_scanner import scancode
    QrAsset = scancode.scanQrCode('Scan your Asset QR code, press \'q\' to exit')
    QrUser = scancode.scanQrCode('Scan your User ID code, press \'q\' to exit')
    
    # QRAsset --  1115,smart home kit,Project development kit,New Jersy
    # QRUser --  9980,joseph,4086123511,California
    print("QRAsset -- ",QrAsset)
    print("QRUser -- ",QrUser)
    # scancode.checkin_and_checkout_book(QrAsset,QrUser)

    asset_id = QrAsset.split(',')[0]
    employee_id = QrUser.split(',')[0]
    log_status="Error occured, check-in / check-out not done !!"

    if asset_id in list(Asset.objects.values_list("asset_id",flat=1)) and employee_id in list(Employee.objects.values_list("emp_id",flat=1)):
        # messages.success(request,"Valid entry ...")
        print("hey matched ....")
        res = list(In_Out_log.objects.all().filter(return_date=None,asset=asset_id,emp=employee_id))

        if len(res) == 0:
            # create in_out_log object and push new entry
            asset_instance = Asset.objects.all().filter(asset_id=asset_id)
            employee_instance = Employee.objects.all().filter(emp_id=employee_id)
            try:
                In_Out_log.objects.create(asset=asset_instance[0],emp=employee_instance[0],checkin_date=datetime.now())
                log_status = "Asset checked-in successful !!!"
            except:
                log_status = "Check-in not done, please try again !!!"

        elif len(res) >=1:
            # update the first entry
            try:
                update_return = In_Out_log.objects.get(return_date=None,asset=asset_id,emp=employee_id)
                update_return.return_date = datetime.now()
                update_return.save()
                log_status = "Asset returned successful ..."
            except:
                log_status = " Asset not returned, please use valid data !!! "


    else:
        # messages.warning(request,"invalid entry !!! ")
        print("sad not matched ....")
        log_status = "invalid Qr code scanned, please scan Asset QR followed by employee ID..."


        '''
        import datetime
        asset_instance = Asset.objects.all().filter(asset_id='1113')
        employee_instance = Employee.objects.all().filter(emp_id='9980')
        In_Out_log.objects.create(asset=asset_instance[0],emp=employee_instance[0],checkin_date=datetime.datetime.now())


        update_return = In_Out_log.objects.get(return_date=None,asset='1113',emp='9980')
        update_return.return_date = datetime.datetime.now()
        update_return.save()


        '''

    return JsonResponse({'Asset':QrAsset,'Employee':QrUser,'log_status':log_status})