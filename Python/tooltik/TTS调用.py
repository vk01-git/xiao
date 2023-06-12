from gtts import gTTS

text = "你好,我是小爱同学,Welcome to my home!"

tts = gTTS(text=text, lang='zh-CN')
tts.save("speech.mp3")
print("Speech has been saved!")