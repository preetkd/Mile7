from urllib.request import urlopen
import re
import numpy as np
from zipfile import ZipFile
import pandas as pd
import io
import os
import time
import cv2

# To install this module, run:
# python -m pip install Pillow

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import shutil
from DateFnctions import  MonthlyPay, BiWeeklyPay, ThreeWeeklyPay, DefaultPay,WeeklyPay # rowcnt , FileDwnLdFun ,




def FileDwnLdFun(path):
    try:
        shutil.rmtree("Images")  # Folder Cleaned
    except:
        print("Images folder does not exist")

    zipurl = path
    # Download the file from the URL

    zipresp = urlopen(zipurl)
    # Create a new file on the hard drive
    tempzip = open('tempfile.zip', "wb")

    # Write the contents of the downloaded file into the new file
    tempzip.write(zipresp.read())
    # Close the newly-created file
    tempzip.close()
    # Re-open the newly-created file with ZipFile()
    zf = ZipFile("tempfile.zip")

# Extract its contents into <extraction_path>
    # note that extractall will automatically create the path
    zf.extractall(path = 'Images')
    # close the ZipFile instance
    zf.close()

    filname = path
    fup = re.split('/', filname)
    filenm = (re.split('\.', fup[5]))
    fileup = filenm[0] + '.csv'
    upath = fileup
    return upath

# path = FileDwnLdFun ("https://www.dropbox.com/s/5oyh93whi6tq87z/5139617.zip?dl=1")

def Image_extract():  # Function for extracting Images and creating Cchecking.csv
    # Creating a List of Identity File '

     ### Cleaning the image folder

    TestImageList = os.listdir("Images")

    test_Df = pd.DataFrame(TestImageList, columns=['Cust_bankAcctID'])
    test_Df.to_csv('test_Df.csv', index=False)

# Image_extract()


############################# MileStone3###############################

def BnkID_Fraud():


    testDF0 = pd.read_csv('test_Df.csv')


    testDF0[['custID', 'ID_jpg']] = testDF0.Cust_bankAcctID.str.split('_', expand=True)

    testDF0[['bankAcctID', 'jpg']] = testDF0.ID_jpg.str.split('.', expand=True)
    testDF = testDF0.drop(columns= ['ID_jpg' , 'jpg'], axis =1)
    print('*********testDF*********')
    print(testDF)


    # CustomerList
    custDF = pd.read_csv("liveCustomerList.csv")
    custDUp = custDF.apply(lambda x: x.astype(str))
    # custDUp = custDF.apply(lambda x: x.astype(str).str.upper()) DONT NEED UPPERCASE




    # Combined test with Customer data
    testCust = pd.merge(testDF, custDUp, on='custID', how='left')

    testCust.rename(columns={'bankAcctID': 'bankID'}, inplace=True)



    # BankLogin Check

    BankLogin = pd.read_csv("liveBankAcct.csv")

    FraudCust1 = pd.merge(testCust, BankLogin, on=['firstName', 'lastName'], how='left')

    print("wrongbank Ids ************" , FraudCust1)

    WrngBnkId = FraudCust1.drop(columns=['firstName', 'lastName'])

    WrngBnkId['bankID'] = WrngBnkId['bankID'].astype(int)


    WrngBnkId['BnkIDVerify'] = np.where(WrngBnkId['bankID'] == WrngBnkId['bankAcctID'],1,0)


    Bank_D = WrngBnkId[WrngBnkId.BnkIDVerify == 1]

    Bank_Df = Bank_D.drop(columns=['bankAcctID','BnkIDVerify'])
    Bank_Df.rename(columns={'bankID': 'bankAcctID'}, inplace=True)

    return Bank_Df

    # print(upath)

    # Write into CV --->

# Bnk_Df = BnkID_Fraud()     ## Function called


# print('*********Returened*********')
# print(Bnk_Df)

################################## Milestone 2####################

def CustID_Fraud(dft):

    CustDF= dft


    FraudDf = pd.read_csv('liveFraudList.csv')
    FraudDf['Fraud'] = 'F'


    custDU = pd.read_csv("liveCustomerList.csv")
    custDUp = custDU.apply(lambda x: x.astype(str).str.upper())



########Getting Customer Names From LiveCustomerList #################
    testCust = pd.merge(CustDF, custDUp, on='custID', how='left')
    print('F Cust Ids' , testCust)

######## Checking Names from Above on Fraud List#################

    FraudCust1 = pd.merge(testCust, FraudDf, how = 'left', on=['firstName','lastName'])

    cust_ID = FraudCust1[FraudCust1.Fraud != 'F']

    CustID = cust_ID.drop(columns=['firstName','lastName','Fraud'])
    print('********************CustID************')
    print(CustID)
    return(CustID)

# CustBank = CustID_Fraud(Bnk_Df)

########################## MileStone1 ###################################


def image_verify(cID):
    allpic_df = pd.read_csv('IdentityPics - Copy.csv')
    imagePath = 'identityPics-custID_PicID/'

    # This key will serve all examples in this document.
    KEY = "28e599a416f44e37af84ebf4967b2702"

    # This endpoint will be used in all examples in this quickstart.
    ENDPOINT = "https://face20.cognitiveservices.azure.com/"

    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    PERSON_GROUP_ID = 123

    test_Df = cID
    #test_Df[['custID', 'ID_jpg']] = test_Df.Cust_bankAcctID.str.split('_', expand=True)
    acct_series = pd.Series(test_Df["Cust_bankAcctID"].values)
    filepath = 'Images/'

    faceIds = []
    identified_faces = []
    num_left =0
    count = 0

    # Output df
    output_df = acct_series.to_frame()    #dataframe nly have cust_bankacctId



    output_df = output_df.rename(columns={list(output_df)[0]: "Cust_bankAcctID"})
    print('output_df', output_df)
    output_df.insert(1, "face_id", 0)
    output_df.insert(2, "confidence", 0.3)
    output_df.insert(3, "identified_id", 0)
    output_df.insert(4, "custID", 0)


    acc_series_len = len(acct_series)
    if acc_series_len < 10:
        num_left = acc_series_len
    else: num_left = 10

    for acct in acct_series:

        #print('acct', type(acct))
        # The source photos contain this person

        source_image_file_name1 = test_Df[test_Df['Cust_bankAcctID'] == acct].iloc[0]['Cust_bankAcctID']
        #print('source_image_file_name1----->' , source_image_file_name1)
        testimg = filepath + source_image_file_name1

        sourceimage = cv2.imread(testimg)
        ret, buf = cv2.imencode('.jpg', sourceimage) #

        # stream-ify the buffer
        stream = io.BytesIO(buf)

        detected_faces1 = face_client.face.detect_with_stream(stream, detection_model="detection_01")  ## TestImage
        print(detected_faces1[0].face_id, '**********')

        faceIds.append(detected_faces1[0].face_id)   #  faceIds = [] getting populated

        # TestImg face_id in outputDf
        output_df.loc[output_df.Cust_bankAcctID == acct, "face_id"] = detected_faces1[0].face_id
        output_df.loc[output_df.Cust_bankAcctID == acct, "custID"] = acct.split('_')[0]
        count = count + 1

        #print('output_df  229' , output_df)
        # BatchPrinting of face_Ids of testImage
        #print('num_left', num_left , 'count-----' ,count)
        #print(count,'count')

        if (count == num_left):

           # print('****faceIds***',faceIds)
            identified_faces.extend(face_client.face.identify(face_ids=faceIds, person_group_id=PERSON_GROUP_ID,
                                                              max_num_of_candidates_returned=1,
                                                              confidence_threshold=0.45))
            faceIds = []
            num_left = acc_series_len - num_left
            #print(num_left, 'numleft')
            count = 0
            #print(count,'count2')
        time.sleep(4)
    #print('num_left2', num_left, 'count-----2', count)


    # identified_faces = face_client.face.identify(face_ids= faceIds, person_group_id=PERSON_GROUP_ID, max_num_of_candidates_returned=1, confidence_threshold=0.56)

    for face in identified_faces:
        conf = 0.2
        faceid = face.face_id       # face is the index pointing to identified_faces

        idf_id = 'A'

        ids = output_df.loc[output_df.face_id == faceid]
       # print("ids is: ", ids)

        bnk_id = ids["custID"].iloc[0]
       # print("bnk_id is: ", ids)
        if len(face.candidates) > 0:
            conf = face.candidates[0].confidence
            output_df.loc[output_df.face_id == faceid, "confidence"] = conf
            # print(face.candidates[0].person_id)
            person_id = face_client.person_group_person.get(person_group_id="123",
                                                            person_id=face.candidates[0].person_id)

            output_df.loc[output_df.face_id == faceid, "identified_id"] = person_id.name + '.jpg'
            idf_id = person_id.name #+ '.jpg'

            time.sleep(3)
        match = 0
        conf1 = conf * 100
        # print("conf bnk_id idf_id")
        # print(conf1,"  ", bnk_id, "  ", idf_id)
        #print('output_df new coulmns', output_df)

        print(output_df)
        if conf1 > 56 and bnk_id == idf_id:
            match = 1
        else:
            match = 0
        output_df.loc[output_df.face_id == faceid, "verifiedID"] = match

    print('**************output_df******', output_df)
    output_df.to_csv('conf.csv')

    image_d = output_df[output_df.verifiedID == 1]

    print('**************image_d******',image_d)
    image_df = image_d.drop(columns=['face_id','custID', 'confidence', 'identified_id'])
    #print('image_df',image_df)
    return  image_df


########################## MileStone5 ###################################
# paydf = image_verify(CustBank)


def payday_fn(imdf):

    fin = pd.read_csv('test_Df.csv')
    fin[['custID', 'ID_jpg']] = fin.Cust_bankAcctID.str.split('_', expand=True)
    #fin[['bankAcctID', 'jpg']] = fin.ID_jpg.str.split('.', expand=True)
    fin = fin.rename(columns={"custID": "loginID"})
    fin = fin.drop(columns=['ID_jpg'], axis=1)

    print(">>>>>>>>>>>>>>>>>>>>>>>>imdf>>>>>>>>>>>>>>>>")
    print(imdf)
    imdf[['custID', 'ID_jpg']] = imdf.Cust_bankAcctID.str.split('_', expand=True)
    imdf[['bankAcctID', 'jpg']] = imdf.ID_jpg.str.split('.', expand=True)
    imdf = imdf.rename(columns={"custID": "loginID"})


    test1= imdf.drop(columns=['ID_jpg', 'jpg'], axis=1)

    test1['bankAcctID'] = test1['bankAcctID'].astype(int)

    strt_blance = pd.read_csv("startBalance.csv")  # Not using in this milestone

    trnsc = pd.read_csv("bankTransactions.csv")

    trnsc['bankAcctID'] = trnsc['bankAcctID'].astype(int)

    test1 = test1.sort_values(by=['bankAcctID'], ascending=[True])

    acct_trans = pd.merge(test1, trnsc, on='bankAcctID', how='left')


    acct_trans = acct_trans[acct_trans['transAmount'] > 200.00]



    acct_payday = acct_trans.sort_values(by=['bankAcctID', 'date'], ascending=[True, False])
    acct_payday['date'] = pd.to_datetime(acct_payday['date'])

    acct_payday1 = acct_payday[acct_payday['date'] > "2020-02-29"]


    acct_payday12 = acct_payday1.groupby("bankAcctID").count()
    acct_payday12 = acct_payday12.drop(columns=['date'])
    acct_payday12 = acct_payday12.rename(columns={'transAmount': 'freq'})

    acct_payday123 = pd.merge(acct_payday1, acct_payday12, on="bankAcctID", how='right')
    print('*********acct_payday123*********')
    print(acct_payday123)

    acct_serie = pd.Series(acct_payday123["bankAcctID"].values)
    acct_series = acct_serie.drop_duplicates()

    output_df = acct_series.to_frame()
    output_df.insert(1, "date", 'NA')
    output_df = output_df.rename(columns={list(output_df)[0]: "bankAcctID"})
    # print(test1)
    for i in acct_series:
        # print(i,'---------------')

        acct_freq = acct_payday123[acct_payday123['bankAcctID'] == i]['freq'].values[0]
        # acct_payday123 .loc[acct_payday123 ['bankAcctID'] == i,'freq'].item()
        # acct_payday123 123.query('bankAcctID =='+str(i))['freq'][0]  # query takes whole condition as string
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print(acct_freq)
        dtL = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[0]

        pre_date = ""
        if  0 < acct_freq <= 2:

            pre_date = MonthlyPay(dtL)

        elif 2 < acct_freq <= 4:
            dtF = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[1]
            if acct_freq == 3:
                dtF0 = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[2]
            else:dtF0 = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[3]

            pre_date = BiWeeklyPay(dtL, dtF,dtF0)

        elif 4<acct_freq <=6:
            dtF = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[1]
            pre_date = ThreeWeeklyPay(dtL, dtF)

        elif 6<acct_freq <= 8:
            dtF = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[1]
            pre_date = WeeklyPay(dtL, dtF)

        elif acct_freq == 9:
            dtF = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[1]
            pre_date = DefaultPay(dtL, dtF)
        elif acct_freq > 8:
            dtF = acct_payday123.loc[acct_payday123['bankAcctID'] == i, 'date'].iloc[1]
            # dtF = acct_payday123.query('bankAcctID ==' + str(i))['date'][1]
            pre_date = DefaultPay(dtL, dtF)
        output_df.loc[output_df.bankAcctID == i, "date"] = pre_date

    output_df = output_df.set_index('bankAcctID')

    output = pd.merge(test1, output_df, on='bankAcctID', how='left')
    finout = pd.merge(fin,output,  on='Cust_bankAcctID', how='left')

    finalDF = finout.drop(columns=['verifiedID', 'Cust_bankAcctID','loginID_y', 'bankAcctID'])
    finalDF = finalDF.rename(columns={"loginID_x": "loginID"})
    finalDF.fillna('NA')
    print(finalDF)
    return finalDF


def main7(urlpath, file_name):

    path = FileDwnLdFun(urlpath)

    Image_extract()

    Bnk_Df = BnkID_Fraud()

    CustBank = CustID_Fraud(Bnk_Df)

    paydf = image_verify(CustBank)

    outdf = payday_fn(paydf)

    outdf.to_csv(path, index=False)

    flname = path.split('.')[0]

    print(flname)
    file_name.value = flname

def main8(input_arg):
    main7(*input_arg)

#main7("https://www.dropbox.com/s/5qcl1odyznjbory/5159845.zip?dl=1")



# outdf = payday_fn(paydf)
#
# print(outdf,type)
