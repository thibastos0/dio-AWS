import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

def detect_file_text() -> None:
    textract = boto3.client("textract")
    
    # Document
    file_path = str(Path(__file__).parent / "images" / "lista-material-escolar.jpeg")
    
    # Re1oad document content
    with open(file_path, "rb") as file:
        # document_bytes = file.read() # aula
        imageBytes = bytearray(file.read())

    try:
        # Call Amazon Textract
        # response = textract.detect_document_text(Document={"Bytes": document_bytes}) # aula
        response = textract.detect_document_text(Document={'Bytes': imageBytes})
        with open("response.json", "w") as response_file:
            response_file.write(json.dumps(response))

    except ClientError as e:
        print(f"Erro processando documento: {e}")

def get_lines() -> list[str]:
    try:
        # print detected text
    
        with open("response.json", "r") as f:
            data = json.loads(f.read())
            blocks = data["Blocks"]
        
            return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]
    except IOError:
        detect_file_text()
    return []

def main():

    for line in get_lines():
        print(line)


if __name__ == main():
    main()