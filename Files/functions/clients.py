import sqlite3; import os;
def clear(): os.system("cls");

def view():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    while True:
        c.execute("""SELECT c.id, c.name, c.local, c.phone, c.email, COALESCE(SUM(CASE WHEN e.pay = 'S' THEN e.valor ELSE 0 END), 0) AS total_pago, COUNT(e.id) AS total_eventos FROM clients c LEFT JOIN events e ON e.client = c.name GROUP BY c.id ORDER BY c.name ASC"""); results=c.fetchall();
        PAGE_SIZE=15; page=0; total=len(results);

        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mCLIENTES\033[0m"f"\n\n   {'NOME':<22}"f"{'LOCAL':<25}"f"{'TELEMÓVEL':<17}"f"{'EMAIL':<25}"f"{'T. PAGO':<14}"f"{'T. EVENTOS':<3}"); 
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];
        if not results: print("\n", " "*48, "Nenhum cliente encontrado.");
        for id_, name, local, phone, email, pay, events_total in page_items:
            print(f"   {name:<22}"f"{local:<25}"f"{phone:<17}"f"{email:<25}"f"{pay:>10.2f}€"f"{events_total:^17}");
        total_valor=sum(row[5] for row in results); total_events=sum(row[6] for row in results);
        choice=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_valor}€\033[0m\t\033[35mTotal de Eventos:\033[0m {total_events}\033[0m\n\n   \033[35m1.\033[0m Criar Cliente   \033[35m2.\033[0m Editar Cliente    \033[35m3.\033[0m Página Anterior   \033[35m4.\033[0m Página Seguinte   \033[35m5.\033[0m Menu Principal\n\n   > ");
        conn.commit();

        if choice=="1": add();
        elif choice=="2": edit();
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
    
    dados=question();
    if not dados: return;
    name, local, phone, email=dados;

    c.execute("INSERT INTO clients (name, local, phone, email) VALUES (?, ?, ?, ?)", 
              (name, local, phone, email));
    conn.commit(); return;

def edit():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    clear(); print("─"*58,"•","─"*58,"\n"," "*53,"\033[35mCLIENTES\033[0m");
    choice_client=input("\n   Qual o nome do cliente que quer editar?\n\n  > ");
    if not choice_client or len(choice_client)>25: return;

    c.execute("SELECT * FROM clients WHERE name = ?", (choice_client,)); results = c.fetchone();
    if not results: return;
    id_, name, local, phone, email=results;

    clear(); print("─"*58,"•","─"*58,"\n"," "*53,"\033[35mCLIENTES\033[0m");
    choice_user=input(f"   {'NOME':<22}"f"{'LOCAL':<25}"f"{'TELEMÓVEL':<17}"f"{'EMAIL':<25}\n"f"   {name:<22}"f"{local:<25}"f"{phone:<17}"f"{email:<25}\n\n   Confirmar cliente para editar? (S/N)\n  > ").upper();
    if choice_user not in ("S", "N") or len(choice_user)!=1: return;
    elif choice_user=="N": return;
    else:
        dados=question();
        if not dados: return;
        name, local, phone, email=dados;
        c.execute("UPDATE clients SET name=?, local=?, phone=?, email=? WHERE id=?",
                (name, local, phone, email, id_))
        conn.commit(); return;

def question():
    clear(); print("─"*58,"•","─"*58,"\n"," "*53,"\033[35mCLIENTES\033[0m");

    name=input("\n   Qual o nome do cliente?\n  >");
    if not name or len(name)>25: return;

    local=input("\n   Localidade?\n  >");
    if len(local)>25: return;

    phone=input("\n   Contacto?\n  >");
    if len(phone)>15: return;

    email=input("\n   Email?\n  >");
    if len(email)>30: return;

    return name, local, phone, email;