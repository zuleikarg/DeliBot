#!/usr/bin/env python3

import rospy
from my_code.msg import data_speech

import gtts
from playsound import playsound

count = 0
first_nf = True
first_f = True

def speech(data):
    global count, first_nf, first_f
    # in spanish
    # tts = gtts.gTTS("Hola, mi nombre es DeliBot", lang="es")
    # tts.save("hola.mp3")
    # playsound("hola.mp3")

    # tts = gtts.gTTS("EL AFILADOR, EL AFILADOR", lang="es")
    # tts.save("hola.mp3")
    # playsound("hola.mp3")
    # persona = "Pablo Juan"


    if(data.found == False):
        print(count)
        if(count >=35 or first_nf == True):
            tts = gtts.gTTS(data.name + " hay un paquete para ti", lang="es")
            tts.save("hola.mp3")
            playsound("hola.mp3")
            count = 0
            first_nf = False
        else:
            count = count +1
    else:
        print(count)
        if(count >=70 or first_f == True):
            tts = gtts.gTTS(data.name + " recoja su paquete", lang="es")
            tts.save("hola.mp3")
            playsound("hola.mp3")
            count = 0
            first_f = False
        else:
            count = count +1


if __name__ == '__main__':
    rospy.init_node('speech_node', anonymous=True)
    rospy.Subscriber('/speech', data_speech, speech)

    rospy.spin()