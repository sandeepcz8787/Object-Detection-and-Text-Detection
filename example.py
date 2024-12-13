from PIL import Image
from gtts import gTTS
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd=(r"C:\Users\sande\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")

def convert_to_sound(image):
    try:
        open_image=Image.open(image)
        text=pytesseract.image_to_string(open_image)
        text_file=" ".join(text.split("\n"))
        print(text_file)
        sound=gTTS(text_file)
        sound.save("sound.mp3")
        os.system("sound.mp3")
        return True
    except Exception as bug:
        print("ERROR\n",bug)
        return

if __name__=="__main__":
    convert_to_sound(r"image1.jpg")
    input()