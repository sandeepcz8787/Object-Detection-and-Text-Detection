import cv2
import time
import pyttsx3
import speech_recognition as sr
from PIL import Image
from gtts import gTTS
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\DELL\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def capture_and_show_image(cap):
    # Capture a frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        return False, None

    # Display the captured frame
    cv2.imshow("Captured Image", frame)
    return True, frame

def voice_countdown(cap):
    engine = pyttsx3.init()
    for i in range(5, 0, -1):
        # Capture and display the frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            return False
        
        # Display the frame
        cv2.imshow("Webcam Feed", frame)
        
        # Announce the countdown
        engine.say(str(i))
        engine.runAndWait()
        
        # Wait for 1 second
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            return False
    return True

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def convert_to_sound(image_path):
    try:
        open_image = Image.open(image_path)
        text = pytesseract.image_to_string(open_image)
        text_file = " ".join(text.split("\n"))
        print(text_file)
        sound = gTTS(text_file)
        sound.save("sound.mp3")
        os.system("sound.mp3")
        return True
    except Exception as bug:
        print("ERROR\n", bug)
        return

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    cv2.namedWindow("Webcam Feed")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        if not voice_countdown(cap):
            break
        
        success, captured_frame = capture_and_show_image(cap)
        if not success:
            break

        engine = pyttsx3.init()
        engine.say("Do you want to save this photo? Say ok to save or no to retake.")
        engine.runAndWait()
        
        while True:
            print("Listening for response...")
            response = recognize_speech_from_mic(recognizer, microphone)
            if response["success"] and response["transcription"]:
                print(f"You said: {response['transcription']}")
                if "ok" in response["transcription"].lower():
                    image_path = "image.jpg"
                    cv2.imwrite(image_path, captured_frame)
                    engine.say("Photo saved as image.jpg")
                    engine.runAndWait()
                    convert_to_sound(image_path)
                    return
                elif "no" in response["transcription"].lower():
                    engine.say("Retaking photo")
                    engine.runAndWait()
                    cv2.destroyWindow("Captured Image")
                    break
                else:
                    engine.say("I didn't catch that. Please say ok to save or no to retake.")
                    engine.runAndWait()
            elif response["error"]:
                print("Error:", response["error"])
                engine.say("I didn't catch that. Please say ok to save or no to retake.")
                engine.runAndWait()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
