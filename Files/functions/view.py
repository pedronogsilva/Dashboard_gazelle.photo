import sqlite3; import os;
def clear(): os.system("cls");

def ver():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True); db_path=os.path.join(pasta, "database.db"); conn=sqlite3.connect(db_path); c=conn.cursor();
    c.execute("SELECT id, date, event, client, valor, pay, estado FROM events ORDER BY id DESC "); results=c.fetchall();
    PAGE_SIZE=15; page=0; total=len(results);

    while True:
        clear(); print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"); print(f"\n   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}");
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];
        if not results: print("\n\t\t\t   Nenhum evento criado ou encontrado. Para criar um novo carregue 1.");
        for id_, date, events, client, valor, pay, estado in page_items:
            print(f"   {date:<12}"f"{events:<50}"f"{client:<25}"f"{valor:>10.2f}€"f"{pay:^10}"f"{estado:^5}");
        total_valor=sum(row[4] for row in results); pagina_valor=sum(row[4] for row in page_items);
        print(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_valor}€\033[0m\t\033[35mTotal da Página:\033[0m {pagina_valor}€\033[0m");
        print("\n   \033[35m1.\033[0m Criar Evento   \033[35m2.\033[0m Editar Evento    \033[35m3.\033[0m Página Anterior   \033[35m4.\033[0m Página Seguinte   \033[35m5.\033[0m Menu Principal");
        choice=input("\n   > ").strip();

        if choice=="1":print()
        elif choice=="2":print()
        elif choice=="3":
            if page>0: page-=1;
        elif choice=="4":
            if end<total: page+=1;
            else: page=0;
        elif choice=="5":
            conn.close(); return;
        else: continue;

    
    
    
    
    
    
    ##else:
    ##    f
    ##        
