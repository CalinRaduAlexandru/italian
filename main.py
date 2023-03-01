from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv


def configure():
    load_dotenv()


openai.api_key = os.getenv('api_key')

app = Flask(__name__)


# @app.route('/', methods=['GET'])
def create_prompt(user_input=""):
    prompt = f""" Per favore, usando al minimo 200 parole, fai la correzione e la traduzione in rumeno per il mio input e fai anche la traduzione per la tua risposta. Fa essatamente come negli esempi e non dimenticare di continuare la conversazione:
Il tuo testo corretto: "Voglio imparare l'italiano ma non so come fare." Traducerea în română: "Vreau să învăț italiana dar nu știu cum să fac asta.". Risponso: Capisco! Ci sono molte risorse online che puoi usare per imparare l'italiano. Quale tipo di aiuto cercavi? Raspuns: Am înțeles! Există multe resurse online pe care le puteți folosi pentru a învăța limba italiană. Ce fel de ajutor căutai?
Inizia correggendo questo testo e rispondi:
     {user_input}
    """
    # prompt = f"""Exemplu de input: 'Sneakers Nike Jordan 1 Size(42.5)'
    # Outputul pe care il astept de la tine este o descriere de prdous de 150 de cuvinte ca in exemplu de mai jos, incepe cu titlul:
    # ### Titlul produsului ###
    # Despre produsul Sneakers Nike Jordan 1 Size(42.5):\n
    # ### Descrere produs ###
    # Sneakers Nike Jordan 1 Size(42.5) sunt o alegere perfectă pentru cei care doresc să își completeze colecția cu o pereche de adidași de calitate superioară. Designul acestor sneakers este atemporal. Combinația de culori atrăgătoare fac din aceștia o alegere ideală atât pentru purtarea zilnică, cât și pentru ocazii speciale. Materialele de calitate premium ale Sneakers Nike Jordan 1 Size(42.5) asigură un confort maxim, iar talpa cu profil înalt oferă o aderență bună. Brandul Nike și logo-ul Jordan sunt simboluri recunoscute la nivel mondial și aduc un plus de stil și eleganță. Nu ratați ocazia de a vă procura acești sneakers unici si comozi!\n
    # ### Descrere META ###
    # Descriere meta de maxim 80 de caractere: Nike Jordan 1 Size(42.5) sunt ideali pentru pasionații de adidași de calitate superioară. Designul atemporal și culorile atrăgătoare fac diferența.
    # Pe exact structura asta, fa-mi o descriere pentru: {user_input}
    # """
    return prompt


def discussion(prompt):
    data = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    processed_data = data['choices'][0]['text'].split(",")
    new_data = '\n'.join(processed_data)
    print(data)

    return new_data


@app.route('/andrea', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        formatted_response = discussion(create_prompt(prompt))
        # print(formatted_response)
        return render_template("index.html", answer=formatted_response, prompt=prompt)
    else:
        return render_template("index.html")


@app.route('/')
def get_chat():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
