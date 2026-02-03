import sqlite3; import os;
from functions import view;

def initialize_db():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True); db_path=os.path.join(pasta, "database.db"); conn=sqlite3.connect(db_path); c=conn.cursor();
    c.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE NOT NULL, event VARCHAR(50) NOT NULL, client VARCHAR(50) NOT NULL, valor DECIMAL(10,2) NOT NULL, pay BOOLEAN NOT NULL DEFAULT 0, estado VARCHAR(1) NOT NULL)''');
    c.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50) NOT NULL, local VARCHAR(50), phone VARCHAR(15), email VARCHAR(50), total_pago DECIMAL(12,2) DEFAULT 0, total_eventos INT DEFAULT 0)''');
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
"""); print(" \033[35m1.\033[0m Eventos\t \033[35m2.\033[0m Clientes\t \033[35m3.\033[0m Equipamentos \033[35m4.\033[0m Exemplo\n \033[35m5.\033[0m Exemplo\t \033[35m6.\033[0m Exemplo\t \033[35m7.\033[0m Exemplo\t \033[35m8.\033[0m Exemplo"); 

def exit(): clear(); print("Exiting App..."); os.sys.exit();
def clear(): os.system("cls");

while True:
    initialize_db(); dashboard(); option=input("\n > ");

    if option=="1": view.ver()
    elif option=="2": clear();
    elif option=="3": clear();
    elif option=="4": clear();
    elif option=="5": clear();
    elif option=="6": clear();
    else: clear(); 
