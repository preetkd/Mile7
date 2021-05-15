import pandas as pd
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import copy
import requests
from urllib.parse import urlparse
from io import BytesIO
import cv2



# To install this module, run:
# python -m pip install Pillow

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person,SnapshotObjectType, OperationStatusType
import shutil
from Package4Image import FileDwnLdFun
from ImageExtraction1 import Image_extractB

targetPath = 'IdentityPics.csv'
imagePath = 'identityPics-custID_PicID/'
allpic_df = pd.read_csv(targetPath)


# This key will serve all examples in this document.
KEY = "d8eeca20aef0464b8b9bb375371bb931"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://face20.cognitiveservices.azure.com/"





# Create an authenticated FaceClient.

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
print(face_client)
PERSON_GROUP_ID = 123

#face_client.person_group.create(person_group_id= PERSON_GROUP_ID, name ="Mile7")

def person_Grp(allpic_df):
        for acct in allpic_df.bankAcctID:
            person_ID =acct.rstrip('.jpg')

            person = face_client.person_group_person.create(person_group_id=PERSON_GROUP_ID, name=str(person_ID)) # adds person to person group
            print('-------',person)
            vals = allpic_df[allpic_df['bankAcctID'] == acct].values.tolist()
            target_image_file_names = [vals[0][1], vals[0][2]]

            imag1 = open(imagePath + target_image_file_names[0], 'r+b')
            imag2  = open(imagePath + target_image_file_names[1], 'r+b')
            imag1_copy = open(imagePath + target_image_file_names[0], 'r+b')
            imag2_copy = open(imagePath + target_image_file_names[1], 'r+b')



            detected_faces1 = face_client.face.detect_with_stream(imag1,detection_model= "detection_01")  ## detecting face
            lenimages1 = len(detected_faces1)
            if lenimages1 > 0:
                targetFace1 = [detected_faces1[0].face_rectangle.left, detected_faces1[0].face_rectangle.top,
                               detected_faces1[0].face_rectangle.width, detected_faces1[0].face_rectangle.height]
                print(targetFace1, 'TF1')
                face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.person_id,
                                                                     imag1_copy, detection_model="detection_01",
                                                                     target_face=targetFace1)  # , detection_model= "detection_01") # assign face to person
                print(imag1_copy, 'Img1')

            detected_faces2 = face_client.face.detect_with_stream(imag2,detection_model= "detection_01")  ## detecting face
            lenimages2 = len(detected_faces2)

            # target face is an array like [left,top,width,height]
            if lenimages2 > 0:
                targetFace2 = [detected_faces2[0].face_rectangle.left, detected_faces2[0].face_rectangle.top,
                               detected_faces2[0].face_rectangle.width,detected_faces2[0].face_rectangle.height]
                print(targetFace2, 'TF2')
                face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, person.person_id,
                                                                     imag2_copy, detection_model="detection_01",
                                                                     target_face=targetFace2)  # detection_model="detection_01") # assign face to person
                print(imag2_copy, 'Img2')



            time.sleep(20)



def train_test():
    face_client.person_group.train(PERSON_GROUP_ID)

    while (True):
        training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)

def check_config(allpic_df):

    for acct in allpic_df.bankAcctID:
        person_ID = acct.rstrip('.jpg')
        vals = allpic_df[allpic_df['bankAcctID'] == acct].values.tolist()
        target_image_file_names = [vals[0][1], vals[0][2]]
        print(targetPath + "/" + target_image_file_names[0])
        print(targetPath + "/" + target_image_file_names[1])


def delete_person_group(person_group_id):
    face_client.person_group.delete(person_group_id)

def get_person_from_person_group(person_group_id):
    face_client.person_group.get(person_group_id)

#person_Grp(allpic_df)
train_test()
#check_config(allpic_df)

# once person group has been trained
############################################ to Start after Person group is trained #######################

# upath = FileDwnLdFun("https://www.dropbox.com/s/dz54ud90u7fomdp/4253873.zip?dl=1")
#
# Image_extractB()

def main():

    test_Df = pd.read_csv("test_Df.csv")

    acct_series = pd.Series(test_Df["bankAcctID"].values)
    filepath = 'Images/'
    faceIds = []
    identified_faces = []
    count =0
    # Output df
    output_df = acct_series.to_frame()
    output_df = output_df.rename(columns={list(output_df)[0]: "bankAcctID"})
    output_df.insert(1, "face_id", 0)
    output_df.insert(2, "confidence", 0)
    output_df.insert(3, "identified_id",0)
    for acct in acct_series:
        print(acct)
        # The source photos contain this person
        source_image_file_name1 = str(acct)
        testimg = filepath + source_image_file_name1

        sourceimage = cv2.imread(testimg)
        ret, buf = cv2.imencode('.jpg', sourceimage)

        # stream-ify the buffer
        stream = io.BytesIO(buf)

        detected_faces1 = face_client.face.detect_with_stream(stream, detection_model="detection_01")  ## TestImage
        print(detected_faces1[0].face_id, '**********')
        faceIds.append(detected_faces1[0].face_id)   ## faceIds list getting appenededx
        
        output_df.loc[output_df.bankAcctID == acct, "face_id"] = detected_faces1[0].face_id
        count = count+1
        if(count == 10):
            print(faceIds)
            identified_faces.extend(face_client.face.identify(face_ids= faceIds, person_group_id=PERSON_GROUP_ID, max_num_of_candidates_returned=1, confidence_threshold=0.56))
            faceIds = []
            count = 0
        time.sleep(4)

    #identified_faces = face_client.face.identify(face_ids= faceIds, person_group_id=PERSON_GROUP_ID, max_num_of_candidates_returned=1, confidence_threshold=0.56)

    for face in identified_faces:
        conf = 0
        faceid = face.face_id

        idf_id ='A'
        #bnk_id = output_df.query('face_id == `'+ str(faceid)+ '`')["bankAcctID"][0]
        ids = output_df.loc[output_df.face_id == faceid]
        bnk_id = ids["bankAcctID"].iloc[0]

        if len(face.candidates)>0:
           conf = face.candidates[0].confidence
           output_df.loc[output_df.face_id == faceid, "confidence"] = conf
           #print(face.candidates[0].person_id)
           person_id = face_client.person_group_person.get(person_group_id="228", person_id=face.candidates[0].person_id)
           #print(person_id.name)
           output_df.loc[output_df.face_id == faceid, "identified_id"] = person_id.name + '.jpg'
           idf_id = person_id.name + '.jpg'

           time.sleep(3)
        match = 0
        conf1 = conf * 100


        # print('person_id.name  ' , idf_id , type(idf_id))
        #
        # print('bnk_id  ', bnk_id, type(bnk_id))

        # b_id = bnk_id.to_string()
        #
        # print('b_id  ', b_id , type(b_id))

        #output_df.loc[output_df.face_id,]
        if conf1 > 56 and bnk_id == idf_id:
            match = 1
        else: match = 0
        output_df.loc[output_df.face_id == faceid, "verifiedID"] = match
    #print(output_df)

    return output_df


# output = main()                          #### Calling Main Function
#
# #output.to_csv('C:/Users/Harpreet/Desktop/CAPSTONE/Mile1/output.csv')
#
# output[['loginID', 'ext']] = output.bankAcctID.str.split('.', expand=True)
#
# #upload_df = output.drop(columns=['ext', 'bankAcctID'], axis=1)
#
#
# upload_df = output.drop(columns=['confidence','bankAcctID','face_id','ext','identified_id'])
#
# print(upload_df)
#
# upload_df = upload_df.set_index('loginID')
#
# out_path = upath
# upload_df.to_csv(out_path)
#
#
# shutil.rmtree('/Images')

