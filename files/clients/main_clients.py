import sqlite3; 
import os;

from clients import edit_clients;

# ==============================
# Utility Functions
# ==============================

def clear_screen():
    """Clear console screen (Windows)."""
    os.system("cls");


def get_database_connection():
    """Ensure database directory exists and return connection + cursor."""
    db_folder = "./bin";
    os.makedirs(db_folder, exist_ok=True);
    db_path = os.path.join(db_folder, "database.db");
    connection = sqlite3.connect(db_path);
    cursor = connection.cursor();
    return connection, cursor;


# ==============================
# View Clients
# ==============================

def view():
    """Display paginated client list with financial summary."""
    connection, cursor = get_database_connection();

    PAGE_SIZE = 15;
    current_page = 0;

    while True:
        cursor.execute("""
            SELECT c.id, c.name, c.local, c.phone, c.email,
                   COALESCE(SUM(CASE WHEN e.pay = 'S' THEN e.valor ELSE 0 END), 0) AS total_paid,
                   COUNT(e.id) AS total_events
            FROM clients c
            LEFT JOIN events e ON e.client = c.name
            GROUP BY c.id
            ORDER BY c.name ASC
        """);

        results = cursor.fetchall();
        total_records = len(results);

        clear_screen();
        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mCLIENTES\033[0m"
              f"\n\n   {'NOME':<22}{'LOCAL':<25}{'TELEMÓVEL':<17}"
              f"{'EMAIL':<25}{'T. PAGO':<14}{'T. EVENTOS':<3}");

        start_index = current_page * PAGE_SIZE;
        end_index = start_index + PAGE_SIZE;
        page_records = results[start_index:end_index];

        if not results:
            print("\n", " "*48, "Nenhum cliente encontrado.");

        for client_id, name, local, phone, email, total_paid, total_events in page_records:
            print(f"   {name:<22}{local:<25}{phone:<17}"
                  f"{email:<25}{total_paid:>10.2f}€{total_events:^17}");

        total_revenue = sum(row[5] for row in results);
        total_events_count = sum(row[6] for row in results);

        user_option = input(
            f"\n   \033[35mPágina {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_revenue}€"
            f"\t\033[35mTotal de Eventos:\033[0m {total_events_count}\033[0m"
            "\n\n   \033[35m1.\033[0m Criar Cliente"
            "   \033[35m2.\033[0m Editar Cliente"
            "   \033[35m3.\033[0m Página Anterior"
            "   \033[35m4.\033[0m Página Seguinte"
            "   \033[35m5.\033[0m Menu Principal\n\n   > "
        );

        if user_option == "1":
            add();
        elif user_option == "2":
            edit_clients.edit();
        elif user_option == "3":
            if current_page > 0:
                current_page -= 1;
        elif user_option == "4":
            if end_index < total_records:
                current_page += 1;
            else:
                current_page = 0;
        elif user_option == "5":
            return;
        else:
            continue;


# ==============================
# Add Client
# ==============================

def add():
    """Collect user input and insert a new client."""
    connection, cursor = get_database_connection();
    clear_screen();
    print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mCLIENTES\033[0m");

    name = input("\n   Qual o nome do cliente?\n  > ");
    if not name or len(name) > 25:
        return;

    location = input("\n   Localidade?\n  > ");
    if len(location) > 25:
        return;

    phone = input("\n   Contacto?\n  > ");
    if len(phone) > 15:
        return;

    email = input("\n   Email?\n  > ");
    if len(email) > 30:
        return;

    cursor.execute(
        "INSERT INTO clients (name, local, phone, email) VALUES (?, ?, ?, ?)",
        (name, location, phone, email)
    );

    connection.commit();
    connection.close();