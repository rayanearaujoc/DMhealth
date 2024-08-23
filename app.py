from flask import Flask, render_template, request, session, redirect, url_for
import google.generativeai as genai

genai.configure(api_key='AIzaSyBV0NYDtAk8RpzmmZnxFviJvz3pezHgh6o')

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(
        max_output_tokens=1500,
        temperature=0.7,
    ))

app = Flask(__name__)
app.secret_key = 'rayanemelhorprogamador'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if "messages" not in session:
        session["messages"] = [{"role": "Bot", "content": "👋 Olá, sou um chatbot psicólogo aqui para ajudar com suas preocupações profissionais. Por favor, sinta-se à vontade para desabafar."}]
    
    if request.method == "POST":
        if request.form.get("logout"):
            return redirect(url_for("relatorio"))

        user_input = request.form.get("user_input")
        if user_input:
            session["messages"].append({"role": "Usuário", "content": user_input})
            conversation_history = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in session["messages"]])

            prompt = (
                "Você é um chatbot que simula um psicólogo e está conversando com um profissional. "
                "Pergunte ao usuário como ele está se sentindo no trabalho e peça para ele falar sobre seus desafios e preocupações profissionais. "
                "Faça perguntas que ajudem a explorar como ele está lidando com o ambiente de trabalho e as expectativas. "
                "Envie mensagens de apoio e comandos de escrita que ajudem o usuário a refletir sobre suas experiências no trabalho. "
                "Mantenha uma conversa acolhedora e formal. Responda de forma concisa.\n\n"
                f"Histórico da conversa:\n{conversation_history}"
            )

            bot_response = model.generate_content(prompt).text
            session["messages"].append({"role": "Bot", "content": bot_response})
            session.modified = True

    return render_template("chatbot.html", messages=session["messages"])

@app.route('/relatório')
def relatorio():
    return render_template('relatorio.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)