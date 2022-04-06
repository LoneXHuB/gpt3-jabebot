from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from jabebot import ask, append_interaction_to_chat_log, show_da_way,ask_sql

app = Flask(__name__)
# to reset change secret key
app.config['SECRET_KEY'] = '89djhff9lhkd93'

@app.route('/xenchat', methods=['POST'])
def response():
    incoming_msg = request.values['Body']
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                         chat_log)
    msg = MessagingResponse()
    msg.message(answer)
    return str(msg)

@app.route('/xenchat-sql', methods=['POST'])
def sql_response():
    incoming_msg = request.values['Body']
    chat_log = session.get('chat_log')
    answer = ask_sql(incoming_msg)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                         chat_log)
    msg = MessagingResponse()
    msg.message(answer)
    
    print("sql : " + str(msg))
    if len(str(msg)) > 1600:
        return str(msg)[1:1599]
    return "sql : " + str(msg)

if __name__ == '__main__':
    show_da_way()
    app.run(debug=True)