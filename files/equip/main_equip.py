import sqlite3; import os;
def clear(): os.system("cls");

def view():
    pasta="./bin"; os.makedirs(pasta, exist_ok=True);
    db_path=os.path.join(pasta, "database.db");
    conn=sqlite3.connect(db_path); c=conn.cursor();

    PAGE_SIZE=15; page=0;

    while True:
        c.execute("SELECT id, date, garantia, name, valor FROM equip ORDER BY date DESC "); results=c.fetchall(); total=len(results);

        clear(); print("─"*58,"•","─"*58,"\n"," "*52,"\033[35mEQUIPAMENTOS\033[0m"
                       f"\n\n   {'DATA':<12}"f"{'EVENTO':<50}"f"{'CLIENTE':<25}"f"{'VALOR':<14}"f"{'PAGO':<7}"f"{'ESTADO':<3}");
        start=page*PAGE_SIZE; end=start+PAGE_SIZE; page_items=results[start:end];
        if not results: print("\n", " "*48, "Nenhum equipamento encontrado.");
        for id_, date, garantia, name, valor in page_items:
            print(f"   {date:<12}"f"{garantia:^8}"f"{name:<25}"f"{valor:>10.2f}€");
        
        choice=input(f"\n   \033[35mPágina {page+1} / {((total-1) // PAGE_SIZE)+1}\033[0m"f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_valor}€\033[0m\t\033[35mTotal de Eventos:\033[0m {total_events}\033[0m\n\n   \033[35m1.\033[0m Criar Cliente   \033[35m2.\033[0m Editar Cliente    \033[35m3.\033[0m Página Anterior   \033[35m4.\033[0m Página Seguinte   \033[35m5.\033[0m Menu Principal\n\n   > ");
        conn.commit();

        if choice=="1": print();
        elif choice=="2": print();
        elif choice=="3": 
            if page>0: page-=1;
        elif choice=="4":
            if end<total: page+=1;
            else: page=0;
        elif choice=="5": return;
        else: continue;
