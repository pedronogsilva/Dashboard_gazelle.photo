import sqlite3; import os;
def clear(): os.system("cls");

def view():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    while True:
        c.execute("SELECT id, date, event, client, valor, pay, estado FROM events ORDER BY date DESC "); results=c.fetchall();
        PAGE_SIZE=15; page=0; total=len(results);

        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"
                       f"\n\n   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}");
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];
        if not results: 
            print("\n", " "*48, "Nenhum evento encontrado.");
        for id_, date, events, client, valor, pay, estado in page_items:
            print(f"   {date:<12}"f"{events:<50}"f"{client:<25}"f"{valor:>10.2f}€"f"{pay:^10}"f"{estado:^5}");
        print("\n   \33[35mLegenda:\033[0m M-Marcado | C-Capturado | E-A Editar | D-Editado | S-Enviado | R-Cancelado");

        total_valor=sum(row[4] for row in results); pagina_valor=sum(row[4] for row in page_items);
        choice_view=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"
                     f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_valor}€\033[0m\t\033[35mTotal da Página:\033[0m {pagina_valor}€\033[0m"
                     "\n\n   \033[35m1.\033[0m Criar Evento   \033[35m2.\033[0m Editar Evento    \033[35m3.\033[0m Página Anterior   \033[35m4.\033[0m Página Seguinte   \033[35m5.\033[0m Menu Principal\n\n  > ");

        if choice_view=="1": add();
        elif choice_view=="2": edit();
        elif choice_view=="3":
            if page>0: page-=1;
        elif choice_view=="4":
            if end<total: page+=1;
            else: page=0;
        elif choice_view=="5": return;
        else: continue;

def add():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    dados=question();
    if not dados: return;
    client, date_event, name_event, preco, pago, estado=dados;
    c.execute("INSERT INTO events (date, event, client, valor, pay, estado) VALUES (?, ?, ?, ?, ?, ?)", 
              (date_event, name_event, client, preco, pago, estado));
    conn.commit(); return;

def edit():
    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");
        choice_edit=input("\n   Pesquisar por?\n\n   \033[35m1.\033[0m Data\n   \033[35m2.\033[0m Evento\n   \033[35m3.\033[0m Cliente\n   \033[35m4.\033[0m Menu Principal\n\n  >")
        if choice_edit=="1": edit_by_date();
        if choice_edit=="2": edit_by_event();
        if choice_edit=="3": edit_by_client();
        if choice_edit=="4": return;
        else: continue;

def edit_by_date():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    
    dados=choice_event_by_date();
    if not dados: return;
    c.execute("SELECT * FROM events WHERE id = ?", (dados,)); result=c.fetchone();
    id_, date, events, client, valor, pay, estado=result;

    clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m\n")
    choice_user=input(f"   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}\n"f"   {date:<12}"f"{events:<50}"f"{client:<25}"f"{valor:>10.2f}€"f"{pay:^10}"f"{estado:^5}\n\n   Confirmar evento para editar? (S/N)\n  > ").upper();
    if choice_user not in ("S", "N") or len(choice_user)!=1: return;
    elif choice_user=="N": return;
    else: 
        dados=question();
        if not dados: return;
        client, date_event, name_event,preco, pago, estado=dados;
        c.execute("UPDATE events SET date=?, event=?, client=?, valor=?, pay=?, estado=? WHERE id=?",
                (date_event, name_event, client, preco, pago, estado, id_))
        conn.commit(); return;

def choice_event_by_date():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");
    choice_event_by_date=input("\n   Qual data quer pesquisar? (YYYY-MM-DD)\n\n  > ");
    if len(choice_event_by_date)!=10: return;

    c.execute("SELECT * FROM events WHERE date = ?", (choice_event_by_date,)); results=c.fetchall();

    PAGE_SIZE=15; page=0; total=len(results);
    
    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"f"\n\n   {'  ':<3}{'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}");
        if not results: input("\n   Nenhum evento com a data selecionada. Crie um evento primeiro."); return None;
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];

        for i, (id_, date, events, client, valor, pay, estado) in enumerate(page_items, start=1):
            print(f"   \033[35m{i}. \033[0m{date:<12}"f"{events:<50}"f"{client:<25}");
        
        choice_event_by_date=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"
                     "\n\n   \033[35m6.\033[0m Página Anterior   \033[35m7.\033[0m Página Seguinte   \033[35m8.\033[0m Menu Principal\n\n  > ");

        if choice_event_by_date=="6": 
            if page>0: page-=1;
        elif choice_event_by_date=="7":
            if end<total: page+=1;
            else: page=0;
        elif choice_event_by_date=="8": return;
        elif choice_event_by_date.isdigit():
            choice_event_by_date=int(choice_event_by_date);
            if 1<=choice_event_by_date<=len(page_items):
                return page_items[choice_event_by_date-1][0];
        else: continue;

def edit_by_event():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    
    dados=choice_event_by_event();
    if not dados: return;
    c.execute("SELECT * FROM events WHERE id = ?", (dados,)); result=c.fetchone();
    id_, date, events, client, valor, pay, estado=result;

    clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m\n")
    choice_user=input(f"   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}\n"f"   {date:<12}"f"{events:<50}"f"{client:<25}"f"{valor:>10.2f}€"f"{pay:^10}"f"{estado:^5}\n\n   Confirmar evento para editar? (S/N)\n  > ").upper();
    if choice_user not in ("S", "N") or len(choice_user)!=1: return;
    else: 
        dados=question();
        if not dados: return;
        client, date_event, name_event,preco, pago, estado=dados;
        c.execute("UPDATE events SET date=?, event=?, client=?, valor=?, pay=?, estado=? WHERE id=?",
                (date_event, name_event, client, preco, pago, estado, id_))
        conn.commit(); return;

def choice_event_by_event():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");
    choice_event_by_event=input("\n   Qual evento quer pesquisar?\n\n  > ");
    if not choice_event_by_event or len(choice_event_by_event)>50: return;

    c.execute("SELECT * FROM events WHERE event = ?", (choice_event_by_event,)); results=c.fetchall();

    PAGE_SIZE=15; page=0; total=len(results);
    
    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"f"\n\n   {'  ':<3}{'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}");
        if not results: input("\n   Nenhum evento com o nome selecionada. Crie um evento primeiro."); return None;
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];

        for i, (id_, date, events, client, valor, pay, estado) in enumerate(page_items, start=1):
            print(f"   \033[35m{i}. \033[0m{date:<12}"f"{events:<50}"f"{client:<25}");
        
        choice_event_by_event=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"
                     "\n\n   \033[35m6.\033[0m Página Anterior   \033[35m7.\033[0m Página Seguinte   \033[35m8.\033[0m Menu Principal\n\n  > ");

        if choice_event_by_event=="6": 
            if page>0: page-=1;
        elif choice_event_by_event=="7":
            if end<total: page+=1;
            else: page=0;
        elif choice_event_by_event=="8": return;
        elif choice_event_by_event.isdigit():
            choice_event_by_event=int(choice_event_by_event);
            if 1<=choice_event_by_event<=len(page_items):
                return page_items[choice_event_by_event-1][0];
        else: continue;

def edit_by_client():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    dados=choice_event_by_client();
    if not dados: return;
    c.execute("SELECT * FROM events WHERE id = ?", (dados,)); result=c.fetchone();
    id_, date, events, client, valor, pay, estado=result;

    clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m\n")
    choice_user=input(f"   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}\n"f"   {date:<12}"f"{events:<50}"f"{client:<25}"f"{valor:>10.2f}€"f"{pay:^10}"f"{estado:^5}\n\n   Confirmar evento para editar? (S/N)\n  > ").upper();
    if choice_user not in ("S", "N") or len(choice_user)!=1: return;
    else: 
        dados=question();
        if not dados: return;
        client, date_event, name_event,preco, pago, estado=dados;
        c.execute("UPDATE events SET date=?, event=?, client=?, valor=?, pay=?, estado=? WHERE id=?",
                (date_event, name_event, client, preco, pago, estado, id_))
        conn.commit(); return;

def choice_event_by_client():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    choice_event_by_client=select_client();
    if not choice_event_by_client: return;

    c.execute("SELECT * FROM events WHERE client = ?", (choice_event_by_client,)); results=c.fetchall();

    PAGE_SIZE=15; page=0; total=len(results);
    
    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"f"\n\n   {'  ':<3}{'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}");
        if not results: input("\n   Nenhum evento com o cliente selecionada. Crie um evento primeiro."); return None;
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];

        for i, (id_, date, events, client, valor, pay, estado) in enumerate(page_items, start=1):
            print(f"   \033[35m{i}. \033[0m{date:<12}"f"{events:<50}"f"{client:<25}");
        
        choice_event_by_event=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"
                     "\n\n   \033[35m6.\033[0m Página Anterior   \033[35m7.\033[0m Página Seguinte   \033[35m8.\033[0m Menu Principal\n\n  > ");

        if choice_event_by_event=="6": 
            if page>0: page-=1;
        elif choice_event_by_event=="7":
            if end<total: page+=1;
            else: page=0;
        elif choice_event_by_event=="8": return;
        elif choice_event_by_event.isdigit():
            choice_event_by_event=int(choice_event_by_event);
            if 1<=choice_event_by_event<=len(page_items):
                return page_items[choice_event_by_event-1][0];
        else: continue;

def question():
    clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");

    client=select_client();
    if not client: return;

    date_event=input("\n   Data do evento? (YYYY-MM-DD)\n  > ");
    if len(date_event)!=10: return;

    name_event=input("\n   Nome do evento?\n  > ");
    if not name_event or len(name_event)>50: return;

    preco=input("\n   Preço cobrado? (€)\n  > ");
    if not preco: return;

    pago=input("\n   Evento pago? (S/N)\n  > ").upper();
    if pago not in ("S", "N") or len(pago)!=1: return;

    estado=input("\n   Estado do evento? (M/C/E/D/S)\n  > ").upper();
    if estado not in ("M","C","E","D","S") or len(estado)!=1: return;

    return client, date_event, name_event, preco, pago, estado;

def select_client():
    pasta="./bin";
    os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();
    c.execute("SELECT id, name FROM clients ORDER BY id DESC"); search=c.fetchall();

    if not search: input("\n   Nenhum cliente encontrado. Crie um cliente primeiro."); return None;

    PAGE_SIZE=5; page=0; total=len(search);

    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m\n\n   Nome do Cliente?");
        start=page * PAGE_SIZE; end=start+PAGE_SIZE; page_items=search[start:end];

        for i, (id_, name) in enumerate(page_items, start=1):
            print(f"   {i}. {name}");

        choice_select_client=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m   \033[35m6.\033[0m Página Anterior   \033[35m7.\033[0m Página Seguinte   \033[35m8.\033[0m Menu Principal\n\n  > ");

        if choice_select_client=="6": 
            if page>0: page-=1;
        elif choice_select_client=="7":
            if end<total: page+=1;
            else: page=0;
        elif choice_select_client=="8": return;
        elif choice_select_client.isdigit():
            choice_select_client=int(choice_select_client);
            if 1<=choice_select_client<=len(page_items):
                return page_items[choice_select_client-1][1];
        else: continue;
