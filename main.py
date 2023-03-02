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


def description(prompt):
    data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Creezi descrieri atrgatoare pentru produsele unui ecommerce"},
            {"role": "user", "content": "Nike T-Shirt VI Dry"},
            {"role": "assistant",
             "content": "Nike T-Shirt VI Dry este o tricou sportiv pentru bărbați, proiectat pentru a oferi confort și performanță maximă în timpul activităților fizice. Materialul Dry-FIT al tricoului este realizat dintr-un amestec de poliester și bumbac, care îndepărtează rapid transpirația de pe piele, menținându-te uscat și confortabil în timpul antrenamentului. Designul modern și elegant, împreună cu logo-ul Nike vizibil pe piept, îl fac un produs atractiv și potrivit pentru a fi purtat în afara sălii de sport. Cu o gamă variată de culori și mărimi disponibile, acest tricou Nike este o alegere excelentă pentru cei care doresc să se simtă confortabil și să arate bine în timpul antrenamentelor lor."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    # print(data)
    data = data['choices'][0]['message']

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    # Decode the JSON string using codecs
    decoded_data = codecs.decode(json_data, 'unicode_escape',)

    # Convert the decoded string back to a dictionary
    decoded_dict = json.loads(decoded_data)

    # Access the decoded text
    decoded_text = decoded_dict['content']

    return decoded_text

def meta_text(prompt):
    data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Crează meta descrieri atragatoare, incadreaza-te in spatiul recomandat unei descrieri meta pentru produsele unui ecommerce. Obligatoriu ca raspunsul sa fie intre 20 si 22 de cuvinte si obligatoriu mereu sa folosesti si sa incluzi promptul in raspuns fara sa alterezi sau sa scoti niciun cuvant"},
            {"role": "user", "content": "Nike T-Shirt VI Dry"},
            {"role": "assistant",
             "content": "Descoperă confortul și respirabilitatea într-un singur tricou Nike T-Shirt VI Dry. Perfect pentru antrenamente sau activități zilnice."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    data = data['choices'][0]['message']

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data)

    # Decode the JSON string using codecs
    decoded_data = codecs.decode(json_data, 'unicode_escape', )

    # Convert the decoded string back to a dictionary
    decoded_dict = json.loads(decoded_data)

    # Access the decoded text
    decoded_text = decoded_dict['content']

    return decoded_text


@app.route('/response', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        formatted_response = description(prompt)
        meta = meta_text(prompt)
        return render_template("index.html", answer=formatted_response, meta=meta, prompt=prompt)
    else:
        return render_template("index.html")


@app.route('/')
def get_chat():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
