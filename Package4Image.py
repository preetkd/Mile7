

# Downloading Zip file from URL
from urllib.request import urlopen
from zipfile import ZipFile
import re




# Function to Unzipfile  defining upload path

def FileDwnLdFun(path):
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
    fileup = filenm[0]+'.csv'
    upath = fileup
    return upath




# Zipping done , Image folder created in ImageExtraction1.py




#----------------------------------------------------------------------------------
# #your path
# col_dir = 'Mile1Images/*.jpg'
# 
# #creating a collection with the available images
# images = imread_collection(col_dir)
# assert isinstance(images, object)
# 
# print("single Image" )
# print(images[0])
# i=1
# for img in images:
#     print("image -------------------")
#     if i is 1:
#         break
#     print(img)
# 
# 
# 
# def load_images(folder):
#     images = []
#     for filename in folder:
#         print(filename)
#         img = cv2.imread(filename)
#         if img is not None:
#             images.append(img)
#     return images
# 
# 
# #images1 = load_images(col)