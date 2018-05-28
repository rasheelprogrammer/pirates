# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.chat.ChatGarbler
import string, random
from otp.otpbase import OTPLocalizer

class ChatGarbler:
    __module__ = __name__

    def garble(self, avatar, message):
        newMessage = ''
        numWords = random.randint(1, 7)
        wordlist = OTPLocalizer.ChatGarblerDefault
        for i in range(1, numWords + 1):
            wordIndex = random.randint(0, len(wordlist) - 1)
            newMessage = newMessage + wordlist[wordIndex]
            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage

    def garbleSingle(self, avatar, message):
        newMessage = ''
        numWords = 1
        wordlist = OTPLocalizer.ChatGarblerDefault
        for i in range(1, numWords + 1):
            wordIndex = random.randint(0, len(wordlist) - 1)
            newMessage = newMessage + wordlist[wordIndex]
            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage