import json
import boto3
import botocore
import cv2
import sys

def handler(event, context):
    s3 = boto3.resource('s3')
    bucket = 'iosprojfixed-deployments-mobilehub-1649974884'
    key = 'party-dresses.jpg'
    local_path = '/tmp/local_party-dresses.jpg'

    try:
        s3.meta.client.download_file(bucket, key, local_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Read the image
    image = cv2.imread(local_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    print ("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    local_path2 = "tmp/detected_image.jpg"
    # save image
    status = cv2.imwrite(local_path2,image)
     
    print("Image written to file-system : ",status)



    try:
        s3.meta.client.upload_file(local_path2, bucket, 'hello.jpg')
    except botocore.exceptions.ClientError as e:
        print("error");
        raise
    
    # s3 = boto3.resource("s3")
    # s3.Bucket("iosprojfixed-deployments-mobilehub-1649974884").download_file('party-dresses.jpg', '/tmp/party-dresses.jpg')

    responseCode = 200
    link = "https://s3.amazonaws.com/iosprojfixed-deployments-mobilehub-1649974884/hello.jpg"    
    # image_result = open(path,'wb')
    # image_result.write(img)
    # image_result.close()
    
    # image_64_encode = base64.encodestring(path)
    response = {
        'statusCode': responseCode,
        'headers':{
            # "x-custom-header":"custom header value",
            "content-type":"image/jpg"
        },
        'body':"",
        'isBase64Encoded':True,
        'link':link
    }

    return response