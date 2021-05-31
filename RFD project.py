# -*- coding: utf-8 -*-
"""
Created on Fri May 14 16:52:32 2021

@author: krzys
"""

import pyodbc
import os
from flask import Flask, request, redirect, url_for, render_template
import random
from waitress import serve


os.chdir(r'C:\MyPythonScripts\projekt')

app = Flask (__name__)

Username="""type your username here"""
Password="""type your password here"""
Server='type your server name here'
Database='type your db here'
Driver='SQL Server' 

conn = pyodbc.connect(f'DRIVER={Driver};\
                      SERVER={Server};\
                      DATABASE={Database};\
                      UID={Username};\
                      PWD={Password}')
                      
cursor = conn.cursor()

slownik = {}
lista_ktmow = []
slownik_id_losowy_numer = {}

def listToString(s):     
    # initialize an empty string
    str1 = ""     
    # return string  
    return (str1.join(s))

@app.route('/')
def filtrowanie():
    
    return render_template("parametry.html")

@app.route ('/wgraj', methods =['GET', 'POST'])
def form_example():
    global data_from_form, zmiana_from_form, linia_from_form, \
        slownik, ilosc, lista_ktmow
    #zrob petle losujaca losowy ciag znakow
    lista_znakow = ['a','b','c','d','e','f','g','h']
    dlugosc_listy = len(lista_znakow)
    losowa_lista_znakow = []
    flaga = False
    int_a = random.randrange(99999,999999)
    list_int_a = list(str(int_a))
    while not flaga:
        a = random.randrange(0,dlugosc_listy)
        losowa_lista_znakow.append(lista_znakow[a])
        if len (losowa_lista_znakow) == dlugosc_listy:
            flaga = True
        else:
            continue
    losowa_lista_znakow2 = []
    for i in losowa_lista_znakow:
        losowa_lista_znakow2.append(i)
        for j in list_int_a:
            losowa_lista_znakow2.append(j)
    string = listToString(losowa_lista_znakow2)        
    data_from_form = request.form.get('data_value','')
    zmiana_from_form = request.form.get('zmiana_value')
    linia_from_form = request.form.get('linia_value')
    n = 0
    slownik = {}
    lista_ktmow = []
    string1, string2 = 'cursor.execute',("""SELECT P45.*, P.powod FROM dbo.P45_REALIZACJA_ZMIANOWA P45 left join dbo.powody P on P45.KTM = P.KTM where P45.data = '{}' and P45.zmiana  = '{}' and P45.linia = '{}'""").format(data_from_form, zmiana_from_form, linia_from_form)
    sql_query = eval(string1 + '("""' + string2 + '""")')
    for i in sql_query:
        slownik[n] = i
        n = n + 1    
    ilosc = len(slownik)
    lista_ktmow = []    
    for i in slownik.values():
        lista_ktmow.append(str(i.KTM))

    """
    """
    dlugosc_random = ilosc
    flaga_random = False
    lista_random = []
    while not flaga_random:
        a = random.randrange(999999999999,9999999999999999999)
        if a in lista_random:
            continue
        else:
            lista_random.append(a)
        if len (lista_random) == dlugosc_random:
            flaga_random = True
    """
    """
    
    return render_template('list.html', slownik = slownik, lista_random = lista_random, string = string)
    
@app.route('/add_submit', methods =['GET', 'POST'])
def witaj():
    global powody
    powody = {}
    for i in lista_ktmow:
        request.form.get(str (i))
        if request.form.get(str (i)) == '':
            pass
        elif request.form.get(str (i)) == None:
            pass
        else:
            powody[i] = request.form.get(str (i))
        
    for i in range (len(slownik)):
        try:
            id_slownik = slownik[i].id
            linia = slownik[i].linia
            data = slownik[i].data
            zmiana = 'zmiana 1'
            KTM = slownik[i].KTM
            Opis = slownik[i].Opis
            Powod = powody[lista_ktmow[i]]
            string1 = 'cursor.execute'
            string2 = ("""INSERT INTO dbo.powody VALUES ('{}','{}','{}','{}','{}','{}','{}')""").format(id_slownik,linia,data,zmiana,KTM, Opis, Powod)
            c = string1 + '("""' + string2 + '""")'
            exec (c)
            conn.commit()
        except:
            continue
    return 'Udalo się'

@app.route('/delete')
def delete():
    cursor.execute("""delete from dbo.powody""")
    conn.commit()
    return "Powody usunięte"
    
@app.route('/delete/<string:id_string>', methods =['GET', 'POST'])
def usun_wpis (id_string):
    global string_ukryty, lista_docelowego, string_docelowy_po_petli
    string_ukryty = id_string
    lista_docelowego = []    
    n = 0
    for i in string_ukryty:
        try:
            int(i)
            lista_docelowego.append(i)
            n = n + 1
        except:
            break
    string_docelowy_po_petli = listToString(lista_docelowego)
    dlugosc_id_baza = len (id_string)
    #for i in
    #tutaj sprawdz ile pierwszych wyrazow jest numerycznych
    string1 = 'cursor.execute'
    string2 = ("""delete from dbo.powody where id = '{}'""").format(string_docelowy_po_petli)
    c = string1 + '("""' + string2 + '""")'
    exec(c)
    conn.commit()    
    return "Udalo sie"

if __name__ == "__main__":
    # serve(app, host='127.0.0.1', port=7078)
    # from waitress import serve
    # serve(app, host="127.0.0.1", port=8080)
    app.run(debug = False, port = 1234)

