import sqlite3; import os;
from functions import events, clients;

def initialize_db():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True); db_path=os.path.join(pasta, "database.db"); conn=sqlite3.connect(db_path); c=conn.cursor();
    c.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE NOT NULL, event VARCHAR(50) NOT NULL, client VARCHAR(25) NOT NULL, valor DECIMAL(10,2) NOT NULL, pay VARCHAR(1) NOT NULL, estado VARCHAR(1) NOT NULL)''');
    c.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(25) NOT NULL, local VARCHAR(25), phone VARCHAR(15), email VARCHAR(30))''');
    conn.commit();

def dashboard():
    clear(); print("""\033[35m
   ╔██████╗  █████╗ ███████╗███████╗██╗     ██╗     ███████╗
   ██╔════╝ ██╔══██╗╚══███╔╝██╔════╝██║     ██║     ██╔════╝
   ██║  ███╗███████║  ███╔╝ █████╗  ██║     ██║     █████╗
   ██║   ██║██╔══██║ ███╔╝  ██╔══╝  ██║     ██║     ██╔══╝
   ╚██████╔╝██║  ██║███████╗███████╗███████╗███████╗███████╗
    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝
                D A S H B O A R D - P H O T O\033[0m
────────────────────────────────────────────────────────────
"""); print(" \033[35m1.\033[0m Eventos\t \033[35m2.\033[0m Clientes\t \033[35m3.\033[0m Equipamentos \033[35m4.\033[0m Exemplo\n \033[35m5.\033[0m Exemplo\t \033[35m6.\033[0m Exemplo\t \033[35m7.\033[0m Exemplo\t \033[35m8.\033[0m Fechar"); 

def exit(): os.sys.exit();
def clear(): os.system("cls");

while True:
    initialize_db(); dashboard(); option=input("\n > ");

    if option=="1": events.view()
    elif option=="2": clients.view();
    elif option=="3": clear();
    elif option=="4": clear();
    elif option=="5": clear();
    elif option=="6": clear();
    elif option=="7": clear();
    elif option=="8": exit();
    else: clear(); 
