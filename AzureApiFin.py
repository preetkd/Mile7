
import io

import time

# To install this module, run:
#python -m pip install Pillow

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import cv2
import pandas as pd
from Package4Image import FileDwnLdFun
from ImageExtraction1 import Image_extract
import shutil


shutil.rmtree('C:/Users/Harpreet/Desktop/CAPSTONE/Mile1/Images')

# def Azure_result(dataframe) ## can dataframe be passed in a function
upath = FileDwnLdFun("https://www.dropbox.com/s/qigrjqbwo7ofbc5/434375.zip?dl=1")

# Getting checking.csv created
Image_extract()

### Data frame from checking csv
checkingdf = pd.read_csv("C:/Users/Harpreet/Desktop/CAPSTONE/Mile1/checking.csv")

acct_series = pd.Series(checkingdf["bankAcctID"].values)

# This key will serve all examples in this document.
KEY = "30985004a5914d1e8a01a3769b8b1897"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://facerecogharpreet.cognitiveservices.azure.com/"


##############################################

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Base url for the Verify and Facelist/Large Facelist operations
IMAGE_BASE_URL = 'https://csdx.blob.core.windows.net/resources/Face/Images/'   ### NOT USING

filepath = 'C:/Users/Harpreet/Desktop/CAPSTONE/Mile1/Images/'
targetPath = 'C:/Users/Harpreet/Desktop/CAPSTONE/Mile1/identityPics-custID_PicID/'


#Output df
output_df =acct_series.to_frame()

output_df = output_df.rename(columns={list(output_df)[0]: "bankAcctID"})

print(output_df)
#output_df.insert(1, "c_level", 0)
output_df.insert(1, "verifiedID", 0)


# Create a list to hold the target photos of the same person
for acct in acct_series:
    print(acct)
    # The source photos contain this person
    source_image_file_name1 = str(acct)
    print(source_image_file_name1)
    vals = checkingdf[checkingdf['bankAcctID'] == acct].values.tolist()
    target_image_file_names=[vals[0][4],vals[0][5]]               #'1007_20033.jpg','1007_20034.jpg']
    print(target_image_file_names)
    # Detect face(s) from source image 1, returns a list[DetectedFaces]

    # We use detection model 3 to get better performance.
    testimg = filepath+source_image_file_name1 #+

    # image = open(testimg, 'rb')
    sourceimage = cv2.imread(testimg)

    ret,buf = cv2.imencode('.jpg', sourceimage)

    # stream-ify the buffer
    stream = io.BytesIO(buf)
    # print(buf)
    # print(stream)
    detected_faces1 = face_client.face.detect_with_stream(stream, detection_model="detection_01")  ## TestImage
    print(detected_faces1[0].face_id,'**********')
    #Add the returned face's face ID
    source_image1_id = detected_faces1[0].face_id
    print('{} face(s) detected from image {}.'.format(len(detected_faces1), source_image_file_name1))

    # List for the target face IDs (uuids)

    detected_faces_ids = []
    # Detect faces from target image url list, returns a list[DetectedFaces]
    for image_file_name in target_image_file_names:
        # We use detection model 3 to get better performance.

        image = open(image_file_name, 'rb')
        detected_faces = face_client.face.detect_with_stream(image)   ####, detection_model='detection_03'
        # Add the returned face's face ID
        detected_faces_ids.append(detected_faces[0].face_id)
    ## print('{} face(s) detected from image {}.'.format(len(detected_faces), image_file_name))

    #######################   VERIFY IMAGES   ########################

    # Verification example for faces of the same person. The higher the confidence, the more identical the faces in the images are.
    # Since target faces are the same person, in this example, we can use the 1st ID in the detected_faces_ids list to compare.
    i=0
    conf_level = 0
    #output = pd.DataFrame()
    #for testimage in source_image1_id: ### LOOP for test image Dataframe
    for image_file_name in target_image_file_names:

        verify_result_same = face_client.face.verify_face_to_face(source_image1_id, detected_faces_ids[i])
        print('Faces from {} & {} are of the same person, with confidence: {}'
             .format(source_image_file_name1, target_image_file_names[i], verify_result_same.confidence)
            if verify_result_same.is_identical
            else 'Faces from {} & {} are of a different person, with confidence: {}'
                .format(source_image_file_name1, target_image_file_names[i], verify_result_same.confidence))
        i=i+1

        if verify_result_same.confidence > 0.56:
            c_level = verify_result_same.confidence*100
            break
        if verify_result_same.confidence > 0.9:
            c_level = 0.001
            break
        if verify_result_same.confidence < 0.56:
            conf_level= conf_level + verify_result_same.confidence
            c_level = (conf_level/2)*100
    if c_level > 56 and c_level < 95:
        match = 1
    # elif c_level < 92:
    #     match = 0
    else: match = 0
    ##print(c_level)
    ## print(match)
    ## Append the result in DataFrame

    #output_df.loc[output_df.bankAcctID == acct, "c_level"] = c_level
    output_df.loc[output_df.bankAcctID== acct, "verifiedID"] = match
    time.sleep(15)




output_df[['loginID','ext']] = output_df.bankAcctID.str.split('.',expand = True)
upload_df = output_df.drop(columns =['ext','bankAcctID'],axis=1)

print(output_df)
#upload_df = output_df.drop(columns=['c_level','bankAcctID'])

print(upload_df)

upload_df = upload_df.set_index('loginID')

out_path =  upath
upload_df.to_csv(out_path)

# # Verification example for faces of different persons.
# # Since target faces are same person, in this example, we can use the 1st ID in the detected_faces_ids list to compare.
# verify_result_diff = face_client.face.verify_face_to_face(source_image2_id, detected_faces_ids[0])
# print('Faces from {} & {} are of the same person, with confidence: {}'
#     .format(source_image_file_name2, target_image_file_names[0], verify_result_diff.confidence)
#     if verify_result_diff.is_identical
#     else 'Faces from {} & {} are of a different person, with confidence: {}'
#         .format(source_image_file_name2, target_image_file_names[0], verify_result_diff.confidence))