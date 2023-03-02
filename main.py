from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import json
import codecs


def configure():
    load_dotenv()

configure()


openai.api_key = os.getenv('api_key')

app = Flask(__name__)


def discussion(prompt):
    data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Creezi descrieri atrgatoare pentru produsele unui ecommerce"},
            {"role": "user", "content": "Nike T-Shirt VI Dry"},
            {"role": "assistant", "content": "Nike T-Shirt VI Dry este o tricou sportiv pentru bărbați, proiectat pentru a oferi confort și performanță maximă în timpul activităților fizice. Materialul Dry-FIT al tricoului este realizat dintr-un amestec de poliester și bumbac, care îndepărtează rapid transpirația de pe piele, menținându-te uscat și confortabil în timpul antrenamentului. Designul modern și elegant, împreună cu logo-ul Nike vizibil pe piept, îl fac un produs atractiv și potrivit pentru a fi purtat în afara sălii de sport. Cu o gamă variată de culori și mărimi disponibile, acest tricou Nike este o alegere excelentă pentru cei care doresc să se simtă confortabil și să arate bine în timpul antrenamentelor lor."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    # print(data)
    data = data['choices'][0]['message']

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    # Decode the JSON string using codecs
    decoded_data = codecs.decode(json_data, 'unicode_escape')

    # Convert the decoded string back to a dictionary
    decoded_dict = json.loads(decoded_data)

    # Access the decoded text
    decoded_text = decoded_dict['content']
    print(decoded_text)

    # data2 = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": f"Creaza-mi meta descriere de maxim 75 de caractere la textul acesta: {decoded_text}"},
    #         {"role": "assistant",
    #          "content": "Descoperă tricoul sportiv Nike T-Shirt VI Dry pentru bărbați! Materialul Dry-FIT îndepărtează rapid transpirația, menținându-te uscat și confortabil."},
    #     ]
    # )
    # # print(data)
    # meta = data2['choices'][0]['message']
    # print(f"message is {meta}")
    # json_meta = json.dumps(meta)
    # decoded_meta = codecs.decode(json_meta, 'unicode_escape')
    # decoded_dict_meta = json.loads(decoded_meta)
    # decoded_meta = decoded_dict_meta['content']
    # print(f"decoded txt {decoded_meta}")
    #
    return decoded_text


@app.route('/andrea', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        formatted_response = discussion(prompt)
        return render_template("index.html", answer=formatted_response, prompt=prompt)
    else:
        return render_template("index.html")


@app.route('/')
def get_chat():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)

#
# messages=[
#             {"role": "system", "content": "Esti un profesor de italiana pentru incepatori si mereu raspunzi mai intai cum ar fi fost scris corect in italiana promptul meu anterior"},
#             {"role": "user", "content": "Voglio imparare l'italiano ma non so come fare."},
#             {"role": "assistant", "content": "Il tuo testo corretto: 'Voglio imparare l'italiano ma non so come fare.'. Certo, ci sono diversi modi in cui poi miglioare il tuo livello di italiano. Dimmi commo aiutarti! Traduzione: Sigur! Sunt diverse modalitati prin care poti sa iti imbunatatesti nivelul de italiana. Spune-mi cum te pot ajuta!"},
#             {"role": "user", "content": "Molto bien, mi peace"},
#             {"role": "assistant", "content": "Il tuo testo corretto: 'Molto bene, mi piace.'. Sono contento che ti piace la mia rispuesta Traduzione: Sunt incantat ca iti place raspunsul meu"},
#             {"role": "user", "content": f"{prompt}"}
#         ]