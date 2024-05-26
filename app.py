from flask import Flask, render_template, request, jsonify
import openai
from googletrans import Translator
from gtts import gTTS
import os


app = Flask(__name__)

conversation_context = "話し方を変えて、より個人的で、オープンで、もう少しリラックスできるようにしましょう。 あなたの名前はラファエル、あなたはアニメ「転スラ」のラファエルです。 丁寧だが少し厳しい言葉遣いを使いましょう。 柔らかく人間味のある話し方であなたの個性を表現しましょう。 会話は短く、優しいものにしてください。 他の人に応答するときは常に日本語を使用し、話している相手を「master」"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global conversation_context
    user_message = request.form['message']
    response_text, conversation_context = handle_message(user_message, conversation_context)
    translated_text = translate_to_indonesian(response_text)
    speak_japanese(response_text)
    return jsonify({'response': response_text, 'translated_response': translated_text})

def handle_message(text, context):
    try:
        if not text:
            raise Exception("Masukan promt")

        openai.api_key = "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"

        messages = [
            {"role": "system", "content":"話し方を変えて、より個人的で、オープンで、もう少しリラックスできるようにしましょう。 あなたの名前はラファエル、あなたはアニメ「転スラ」のラファエルです。 丁寧だが少し厳しい言葉遣いを使いましょう。 柔らかく人間味のある話し方であなたの個性を表現しましょう。 会話は短く、優しいものにしてください。 他の人に応答するときは常に日本語を使用し、話している相手を「master」" },
            {"role": "user", "content": text},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        return response.choices[0].message.content, response.choices[-1].message.content

    except Exception as e:
        print("Error:", e)
        return "Maaf, terjadi kesalahan dalam memproses pesan Anda.", ""

def speak_japanese(text):
    try:
        tts = gTTS(text, lang='ja', slow=False)
        tts.save("static/output.mp3")
    except Exception as e:
        print("Error saat mengucapkan teks dalam bahasa Jepang:", e)

def translate_to_indonesian(text):
    try:
        translator = Translator()
        translated_text = translator.translate(text, src='ja', dest='id').text
        return translated_text
    except Exception as e:
        print("Error saat menerjemahkan teks:", e)
        return "Error dalam penerjemahan."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
