from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()

openai.api_key = os.getenv('api_key')

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def create_prompt(user_input=""):
    prompt = f"""
    Per favore, fai la correzione e la traduzione in rumeno per il mio input e doppo che mi hai risposto, fai anche la traduzione per la tua risposta. Fa essatamente come negli esempi e non dimenticare di continuare la conversazione:
Esempio:
[io]: Sei fantastico! Adoro imparare così con te!
[italiano]: Il tuo testo corretto: "Sei fantastico! Mi piace imparare così con te!"
Traducerea în română: "Ești fantastic! Îmi place să învăț așa cu tine!"
[italiano]: Grazie per i tuoi commenti! Sono felice di sapere che ti stai godendo la nostra sessione di apprendimento dello spagnolo. C'è qualcosa in particolare che vuoi chiedere o praticare oggi?
Traduzione rumena: “Mulțumesc pentru comentarii! Mă bucur să știu că vă bucurați de sesiunea noastră de învățare a spaniolei. Vrei să întrebi sau să exersezi ceva anume astăzi?"
Inizia correggendo questo testo e rispondi: {user_input}
#     """
#     prompt = f"""Exemplu de input: 'Sneakers Nike Jordan 1 Size(42.5)'
#     Outputul pe care il astept de la tine este o descriere de prdous de 150 de cuvinte ca in exemplu de mai jos, incepe cu titlul:
#     ### Titlul produsului ###
#     Despre produsul Sneakers Nike Jordan 1 Size(42.5):\n
#     ### Descrere produs ###
#     Sneakers Nike Jordan 1 Size(42.5) sunt o alegere perfectă pentru cei care doresc să își completeze colecția cu o pereche de adidași de calitate superioară. Designul acestor sneakers este atemporal. Combinația de culori atrăgătoare fac din aceștia o alegere ideală atât pentru purtarea zilnică, cât și pentru ocazii speciale. Materialele de calitate premium ale Sneakers Nike Jordan 1 Size(42.5) asigură un confort maxim, iar talpa cu profil înalt oferă o aderență bună. Brandul Nike și logo-ul Jordan sunt simboluri recunoscute la nivel mondial și aduc un plus de stil și eleganță. Nu ratați ocazia de a vă procura acești sneakers unici si comozi!\n
#     ### Descrere META ###
#     Descriere meta de maxim 80 de caractere: Nike Jordan 1 Size(42.5) sunt ideali pentru pasionații de adidași de calitate superioară. Designul atemporal și culorile atrăgătoare fac diferența.
#     Pe exact structura asta, fa-mi o descriere pentru: {user_input}
#     """
    return prompt


def discussion(prompt):
    data = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
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
        print(formatted_response)
        return render_template("index.html", answer=formatted_response, prompt=prompt)
    else:
        return render_template("index.html")


@app.route('/')
def get_all_posts():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

