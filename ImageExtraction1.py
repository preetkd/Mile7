# Extracting from previously exratcted folder from Proff A's DropBox


import numpy as np

import os

import pandas as pd

# Downloading Zip file from URL




def Image_extract():  # Function for extracting Images and creating Cchecking.csv
    # Creating a List of Identity File '

    ID_Value_Flist= os.listdir("identityPics-custID_PicID")
    TestImageList = os.listdir("Images")

    test_Df = pd.DataFrame(TestImageList, columns= ['bankAcctID'])


    #test_Df.rename(columns={list(test_Df)[0]: "bankAcctID"}, index= 'bankAcctID')
    #test_Df.index("bnakAcctID")
    print(test_Df)
    # List of Customer Id - 5 numbers from Identity File
    # ID_Key = ID_Value_Flist[0][0:4] LOGIC   ----  ID_D = dict(zip(ID_key,ID_Value_Flist)) ---- ID_key.append(ID_Value_Flist[i][0:4])

    ID_key = []
    i=0
    strlen = len
    ID_D = {}
    for i in range(0,5703) :
        key = ID_Value_Flist[i][0:4] +".jpg"
        value = ID_D.get(key)
        if value is None:
            value =[]
        value.append(ID_Value_Flist[i])
        ID_D[key] = value

    verify_Df = pd.DataFrame.from_dict(ID_D, orient='index') #, columns= ['bankAcctID','VerfyPic1','VerfyPic2','VerfyPic3','VerfyPic4','VerfyPic5'])

    verify_Df.reset_index(inplace=True)  #Creating column bankAcctID
    verify_Df = verify_Df.rename (columns= {'index':'bankAcctID'})

    verify_Df.drop(verify_Df.iloc[:, 3:237],inplace= True, axis=1)
    verify_Df.rename(columns={0:'verifyPic1',1:'verifyPic2' }, inplace=True)  # Verify Dataframe done

    checking_DF = pd.merge(test_Df, verify_Df, on = 'bankAcctID', how = 'left')
    checking_DF['test_path'] = 'Images/'+ checking_DF.bankAcctID  ########## Datafram with testing image Address and Verification Images Address
    checking_DF['verify_path1'] = 'identityPics-custID_PicID/'+ checking_DF.verifyPic1
    checking_DF['verify_path2'] = 'identityPics-custID_PicID/'+ checking_DF.verifyPic2


    checking_DF['verify_path1'] = np.where(checking_DF['verify_path1'].isnull(),checking_DF['test_path'],checking_DF['verify_path1'])
    checking_DF['verify_path2'] = np.where(checking_DF['verify_path2'].isnull(), checking_DF['test_path'],checking_DF['verify_path2'])

    # checking_DF['verifyPic1'] = np.where(checking_DF['verifyPic1'].isnull(), checking_DF['bankAcctID'],checking_DF['verifyPic1'])
    # checking_DF['verifyPic2'] = np.where(checking_DF['verifyPic2'].isnull(), checking_DF['bankAcctID'],checking_DF['verifyPic2'])
    #print(checking_DF)
    checking_DF.to_csv('checking.csv', index= False)
    verify_Df.to_csv('IdentityPics.csv', index=False)


def Image_extractB():  # Function for extracting Images and creating Cchecking.csv
    # Creating a List of Identity File '

     ### Cleaning the image folder

    TestImageList = os.listdir("Images")

    test_Df = pd.DataFrame(TestImageList, columns=['Cust_bankAcctID'])
    test_Df.to_csv('test_Df.csv', index=False)

#print(check_DF)

# Interaction with Azure Face API

Image_extract()


