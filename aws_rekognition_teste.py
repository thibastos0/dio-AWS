#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from pathlib import Path

from PIL import Image, ImageDraw

client = boto3.client('rekognition')

def get_path(file_name: str) -> str:
    return str(Path(__file__).parent / "images" / file_name)


def recognize_celebrities(photo):       
    with open(photo, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})

    bound = []
    cont = 0

    print('Detected faces for ' + photo)

    for celebrity in response['CelebrityFaces']:
        
        confidence = celebrity.get("MatchConfidence", 0) # dictionary.get(keyname, value) //value is returned if the specified key does not exist
        if confidence > 90:
            print('Name: ' + celebrity['Name'])
            print('Id: ' + celebrity['Id'])
            print('KnownGender: ' + celebrity['KnownGender']['Type'])
            print('Smile: ' + str(celebrity['Face']['Smile']['Value']))
            print('Position:')
            print('   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
            print('   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
            print('Info')
            for url in celebrity['Urls']:
                print('   ' + url)
            print()

            bound.append(celebrity['Face']['BoundingBox'])
            cont += 1

    return cont, bound

def show_bounding_boxes(image_path, out_path, box_sets):
    """
    Draws bounding boxes on an image and shows it with the default image viewer.

    :param image_bytes: The image to draw, as bytes.
    :param box_sets: A list of lists of bounding boxes to draw on the image.
    """
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    for box in box_sets:
        #print(f'ver: {box["Left"]}')
        left = image.width * box["Left"]
        top = image.height * box["Top"]
        right = (image.width * box["Width"]) + left
        bottom = (image.height * box["Height"]) + top
        draw.rectangle([left, top, right, bottom], outline='#0ee56e', width=3)
    image.save(out_path)


def main():
    photo_paths = [
        get_path("bbc.jpg"),
        get_path("msn.jpg"),
        get_path("neymar-torcedores.jpg"),
        get_path("poster_filme.jpg"),
    ]
    for photo_path in photo_paths:

        celeb_count, boundBox = recognize_celebrities(photo_path)
        print("Celebrities detected: " + str(celeb_count))
        output_path = get_path(f"{Path(photo_path).stem}-resultado.jpg")
        show_bounding_boxes(photo_path, output_path, boundBox)   

if __name__ == "__main__":
    main()