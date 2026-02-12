import sqlite3; import os;
from functions import clients;
def clear(): os.system("cls");

def view():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    c.execute("SELECT id, date, event, client, valor, pay, estado FROM events ORDER BY id DESC "); results=c.fetchall();
    PAGE_SIZE=15; page=0; total=len(results);

    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"f"\n\n   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}");
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];
        if not results: print("\n", " "*48, "Nenhum evento encontrado.");
        for id_, date, events, client, valor, pay, estado in page_items:
            print(f"   {date:<12}"f"{events:<50}"f"{client:<25}"f"{valor:>10.2f}€"f"{pay:^10}"f"{estado:^5}");
        total_valor=sum(row[4] for row in results); pagina_valor=sum(row[4] for row in page_items);
        choice=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_valor}€\033[0m\t\033[35mTotal da Página:\033[0m {pagina_valor}€\033[0m\n\n   \033[35m1.\033[0m Criar Evento   \033[35m2.\033[0m Editar Evento    \033[35m3.\033[0m Página Anterior   \033[35m4.\033[0m Página Seguinte   \033[35m5.\033[0m Menu Principal\n\n   > ");
        conn.commit();

        if choice=="1": add();
        elif choice=="2": print();
        elif choice=="3": 
            if page>0: page-=1;
        elif choice=="4":
            if end<total: page+=1;
            else: page=0;
        elif choice=="5": return;
        else: continue;

def add():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    clear(); print("─"*58, "•", "─"*58, "\n", " "*54, "\033[35mEVENTOS\033[0m");

    client = select_client();
    if not client: return;

    data_event=input("\n   Data do evento? (YYYY-MM-DD)\n  >");
    if len(data_event) != 10: return;

    name_event=input("\n   Nome do evento?\n  >");
    if not name_event or len(name_event) > 50: return ;

    preco=input("\n   Preço cobrado? (€)\n  >");
    if not preco: return;

    pago=input("\n   Evento pago? (S/N)\n  >").upper();
    if pago not in ("S", "N") or len(pago)!=1: return;
    pago="✓" if pago=="S" else "✗"

    estado=input("\n   Estado do evento? (M/C/E/D/S)\n  >").upper();
    if estado not in ("M","C","E","D","S") or len(estado) != 1: return;

    c.execute("INSERT INTO events (date, event, client, valor, pay, estado) VALUES (?, ?, ?, ?, ?, ?)", (data_event, name_event, client, preco, pago, estado));
    conn.commit(); return;


def select_client():
    pasta="./bin";
    os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    c.execute("SELECT id, name FROM clients ORDER BY id DESC"); clients=c.fetchall()

    if not clients:
        input("\n   Nenhum cliente encontrado. Crie um cliente primeiro."); return None;


    PAGE_SIZE=5; page=0; total=len(clients);

    while True:
        clear();
        print("─"*58, "•", "─"*58,"\n", " "*54, "\033[35mSELECIONAR CLIENTE\033[0m\n\n   Nome do cliente?");
        start=page * PAGE_SIZE; end=start+PAGE_SIZE; page_items=clients[start:end];

        for i, (id_, name) in enumerate(page_items, start=1):
            print(f"   {i}. {name}")

        choice=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m   \033[35m6.\033[0m Página Anterior   \033[35m7.\033[0m Página Seguinte\n  >").upper();

        if choice=="6": 
            if page>0: page-=1;
        elif choice=="7":
            if end<total: page+=1;
            else: page=0;
        elif choice.isdigit():
            choice=int(choice)
            if 1<=choice<=len(page_items):
                return page_items[choice-1][1]
        else:
            break