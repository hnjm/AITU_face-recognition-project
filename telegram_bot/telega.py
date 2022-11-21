import requests
from telegram.ext import *
import telegram

temp = 0
def rec():
    import cv2
    import face_recognition
    import numpy as np
# Loading main and test pictures and converting to RGB format
    imgElon = face_recognition.load_image_file('ElonMusk.jpg')
    imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
    imgTest = face_recognition.load_image_file('ElonTest.jpg')
    imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

    # Scaling pictures parameters
    scale_percent = 50
    width = int(imgElon.shape[1] * scale_percent / 100)
    height = int(imgElon.shape[0] * scale_percent / 100)

    widthTest = int(imgTest.shape[1] * scale_percent / 100)
    heightTest = int(imgTest.shape[0] * scale_percent / 100)

    # Applying changes
    dsize = (width, height)
    dsizeTest = (widthTest, heightTest)
    imgElon = cv2.resize(imgElon, dsize)
    imgTest = cv2.resize(imgTest, dsize)

    # Writing down and encoding
    faceLoc = face_recognition.face_locations(imgElon)[0]
    encodeElon = face_recognition.face_encodings(imgElon)[0]
    cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

    faceLocTest = face_recognition.face_locations(imgTest)[0]
    encodeTest = face_recognition.face_encodings(imgTest)[0]
    # cv2.rectangle(imgTest, (faceLoc[3], faceLoc[0]),(faceLoc[1],faceLoc[2]), (255,0,255),2)

    # Comparing, transforming euclidean distance to similarity score
    results = face_recognition.compare_faces([encodeElon], encodeTest)
    faceDistance = face_recognition.face_distance([encodeElon], encodeTest)
    faceDistance = 100 / (1 + faceDistance)

    # Result
    print(results, faceDistance)
    cv2.putText(imgTest, f'{results} {round(faceDistance[0], 2)}%', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255),
                2)
    #cv2.imshow('Elon Musk', imgElon)
    #cv2.imshow('Elon Test', imgTest)
    cv2.waitKey(0)

    if faceDistance > 61:
        send_msg_true('This is the same person!')
    else: send_msg_true('This is the same person!')


def start_command(update, context):
    name = update.message.chat.first_name
    update.message.reply_text("Hello " + name)
    update.message.reply_text("Please share your image")


def image_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download()
    update.message.reply_text("Image received")


def send_msg_true(text):
    token = "5530368447:AAFe0X6uHPn59Ja36VaOhyBbUBj3Ne4e23k"
    chat_id = "233779360"

    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())


def main():
    print("Started")
    TOKEN = "5530368447:AAFe0X6uHPn59Ja36VaOhyBbUBj3Ne4e23k"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))

    updater.start_polling()
    import time
    time.sleep(20)
    rec()

    updater.idle()



if __name__ == '__main__':
    main()






