import time
import telepot
from telepot.loop import MessageLoop
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

tbot = telepot.Bot("AQUI VAI O SEU TOKEN DO @FATHERBOT DO TELEGRAM") #cria o bot responsável por enviar e receber as mensagens do telegram.

bot = ChatBot('Bot Inteligente') #cria o segundo bot responsável por realizar o aprendizado de maquina.

conversa = ['Oi', 'Olá', 'Tudo bem?', 'Tudo ótimo', 'Você gosta de programar?', 'Sim, eu programo em Python'] #vetor responsável por orientar o bot nas suas primeiras conversas.

trainer = ListTrainer(bot)
#bot.set_trainer(ListTrainer)
trainer.train(conversa)
#bot.train(conversa)

msgPadrao = False #variavel responsavel por verificar se enviou a mensagem padrão ou Não

def handle(msg): #funcao responsavel por receber a mensagem do telegram e responder ao usuário.
    global msgPadrao #define a variavel msgPadrao como global para ser utilizada dentro desse escopo
    content_type, chat_type, chat_id = telepot.glance(msg)

    if (msgPadrao==False): #verifica se a mensagem padrão não foi enviada
        nome = msg['from']['first_name'] #busca o nome da pessoa que está enviando a mensagem
        tbot.sendMessage(chat_id, 'Olá, '+nome) #faz o envio da mensagem padrão com o nome do telegram
        msgPadrao = True

    pergunta = msg["text"] #pega a mensagem em si enviada pelo telegram.
    resposta = bot.get_response(pergunta) #envia a pergunta que você enviou para o bot e processa retornando uma resposta. Essa resposta é armazenada num banco de dados sqlite que é criado automaticamente, onde o bot irá analisar e gravar sua mensagem para aprendizado.
    
    if float(resposta.confidence) > 0.5: #verifica se a confiança da resposta é maior do que 0.5. se for maior ele envia uma resposta relacionado com a pergunta.
        print('TW Bot: ', resposta)
        tbot.sendMessage(chat_id, resposta.text) # funcao para o envio da resposta ao usuario
    else:
        print('TW Bot: Ainda não sei responder esta pergunta')
        tbot.sendMessage(chat_id, 'Ainda não sei responder esta pergunta') # se a resposta nao for de confiança, então ele envia essa frase padrão.

MessageLoop(tbot, handle).run_as_thread() #função responsável por ficar escutando o telegram. Então toda vez que você envia uma mensagem via telegram para o seu bot (tbot), ele recebe a mensagem e chama a função handle passando como parametro a mensagem que você enviou.

while True: #while responsável por deixar os bots sempre funcionando (até ser encerrado manualmente)
    time.sleep(150)