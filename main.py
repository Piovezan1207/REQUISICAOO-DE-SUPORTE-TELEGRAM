                                                ######### VINICIUS PIOVEZAN - 2021 #############

from flask import Flask, jsonify, render_template, request ,redirect, send_file , flash, url_for, session
import planilha, gerador
import requests
import json
import telebot  



bot = telebot.TeleBot('<TOKEN>') #BOT Token telegram - Token do BOT que irá ser adicionado nos grupos para fazer as chamadas

app = Flask(__name__)
app.secret_key = 'chave'

############################################################### ROTAS DO USUSARIO ##########################################################

@app.route("/", methods=['GET']) #Redirect para o Home
def H():
    return redirect(url_for('Home'))

@app.route("/home", methods=['GET']) #Página Home, onde terá uma lista para escolher qualquer sala e fazer o chamado
def Home():
    sala = request.args.get('sala')
    permitidas = planilha.ler("salas")

    if sala == None:
        sala = '---' 

    if sala.rstrip() in permitidas:
        suporte = "/Requisitar?sala={}&tipo=suporte".format(sala)
        limpeza = "/Requisitar?sala={}&tipo=limpeza".format(sala)
        return render_template('home.html', sala_ = sala, suporte = suporte, limpeza = limpeza  )
    else:
        return render_template('home2.html', permitidas = permitidas)

@app.route("/Requisitar", methods=['GET']) #Faz o chamado no telegram
def Requisitar():
    sala = request.args.get('sala')
    tipo = request.args.get('tipo')
    bot_id_chat = planilha.ler("id")
    permitidas = planilha.ler("salas")

    if sala == None:
        sala = '' 

    if sala.rstrip() in permitidas:
        if tipo == "suporte":
            texto = "O suporte técnico foi chamado na sala {}".format(sala)
            try:
                bot.send_message(bot_id_chat[0], texto)
                pass
            except:
                pass
        elif tipo == "limpeza":
            texto = "A equipe de limpeza foi chamado na sala {}".format(sala)
            try:
                bot.send_message(bot_id_chat[1], texto)
                pass
            except:
                pass
        url = "/Terminado?sala={}&tipo={}".format(sala,tipo)
        return redirect(url)
    else:
        return render_template('home2.html', permitidas = permitidas)

@app.route("/Terminado", methods=['GET']) #Página de confirmação do chamado
def Terminado():
    sala = request.args.get('sala')
    permitidas = planilha.ler("salas")

    if sala == None:
        sala = '' 

    if sala.rstrip() in permitidas:
        tipo = request.args.get('tipo')
        home = "/home?sala={}&tipo={}".format(sala,tipo)
        return render_template('Requisitar.html' , sala = sala, tipo = tipo, home = home)
    else:
        return render_template('home2.html', permitidas = permitidas)

############################################################### ROTAS DE LOGIN ##########################################################

@app.route("/login", methods=['GET'])
def login():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:  
        return render_template('login.html')
    else:
        flash('Você já está logado!')
        return redirect(url_for('Home'))
        

@app.route("/Autenticar", methods=['POST','GET'])
def Autenticar():
    usuario = "LOGIN"
    senha = 'SENHA'
    if usuario == request.form['usuario'] and senha == request.form['senha']:
        session['usuario_logado'] =usuario
        flash('Login feito com sucesso.')
        return redirect(url_for('Configuracao'))
    else:
        flash('Usuario ou senha incorretos, tente novamente.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout feito.')
    return redirect(url_for('Home'))

################################################### ROTAS DE CONFIGURAÇÃO ########################################################## 

@app.route("/config", methods=['GET'])
def Configuracao(): 
    if 'usuario_logado' not in session or session['usuario_logado'] == None:  
        return redirect(url_for('login'))
    else:    
        permitidas = planilha.ler("salas")
        salas =  planilha.ler("salas")
        link =  planilha.ler("link")
        ID =  planilha.ler("id")
        return render_template('Configuracao.html', salas = salas, ID = ID, permitidas = permitidas, link = link) 

################################################### REGRAS DE NEGÓCIO ########################################################## 

@app.route("/adicionar", methods=['GET']) #Adicionar uma nova sala na planilha
def adicionar():
    sala = request.args.get('sala')
    planilha.adicionar("salas",sala)
    return redirect(url_for('Configuracao'))

@app.route("/remover", methods=['GET']) #Remover uma sala da planilha
def remover():
    sala = request.args.get('sala')
    planilha.remover(sala)
    return redirect(url_for('Configuracao'))

@app.route("/mudar_ID_sup", methods=['GET']) #Modificar o ID do chat em que o bot vai enviar o chamado de suporte
def mudar_ID_sup():
    id_ = request.args.get('id')
    planilha.adicionar("idA",id_)
    return redirect(url_for('Configuracao'))

@app.route("/mudar_ID_limp", methods=['GET']) #Modificar o ID do chat em que o bot vai enviar o chamado de limpeza
def mudar_ID_limp():
    id_ = request.args.get('id')
    planilha.adicionar("idB",id_)
    return redirect(url_for('Configuracao'))

@app.route("/mudar_link", methods=['GET']) #Deve ser o link da aplicação, sem nenhuma parematro. Será utilizada para criação do QR code. 
def mudar_link():
    link = request.args.get('link')
    planilha.adicionar("link",link)
    return redirect(url_for('Configuracao'))

@app.route("/gerar_QR", methods=['GET']) #Gerar um QR code de uma sala
def QR():   
    sala = request.args.get('sala')
    link = planilha.ler("link")
    link = link[0]
    gerador.criar_QR(sala,link)
    return send_file("QR.png", mimetype='image/png',as_attachment=True) 



################################################################################################################
if __name__ == "__main__":
    app.run(port=8923, host='0.0.0.0', debug=True, threaded=True)