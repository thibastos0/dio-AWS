#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from pathlib import Path


client = boto3.client('rekognition')

def get_path(file_name: str) -> str:
    return str(Path(__file__).parent / "images" / file_name)


def recognize_celebrities(photo):       
    with open(photo, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})

    print('Detected faces for ' + photo)
    for celebrity in response['CelebrityFaces']:
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
    return len(response['CelebrityFaces'])


def main():
    #photo = 'photo-name'
    photo_paths = [
        #get_path("bbc.jpg"),
        #get_path("msn.jpg"),
        #get_path("neymar-torcedores.jpg"),
        get_path("poster_filme.jpg"),
    ]
    for photo_path in photo_paths:

        celeb_count = recognize_celebrities(photo_path)
        print("Celebrities detected: " + str(celeb_count))


if __name__ == "__main__":
    main()