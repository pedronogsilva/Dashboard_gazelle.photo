import sqlite3; 
import os;

from clients import main_clients;
from events import edit_events;


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
# Event Viewer (Main Menu)
# ==============================

def view_events():
    """Display paginated list of events with navigation options."""
    connection, cursor = get_database_connection();

    PAGE_SIZE = 15; 
    current_page = 0;

    while True:
        # Fetch all events ordered by most recent date
        cursor.execute(
            "SELECT id, date, event, client, valor, pay, estado "
            "FROM events ORDER BY date DESC"
        );
        all_events = cursor.fetchall();
        total_records = len(all_events);

        clear_screen();

        # Header
        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"
              f"\n\n   {'DATA':<12}{'EVENTO':<50}{'CLIENTE':<25}{'VALOR':<14}{'PAGO':<7}{'ESTADO':<3}");

        # Pagination slicing
        start_index = current_page * PAGE_SIZE;
        end_index = start_index + PAGE_SIZE;
        page_records = all_events[start_index:end_index];

        if not all_events:
            print("\n", " "*48, "Nenhum evento encontrado.");

        # Print current page records
        for event_id, date, event_name, client_name, price, paid, status in page_records:
            print(f"   {date:<12}{event_name:<50}{client_name:<25}"
                  f"{price:>10.2f}€{paid:^10}{status:^5}");

        print("\n   \33[35mLegenda:\033[0m "
              "M-Marcado | C-Capturado | E-A Editar | "
              "D-Editado | S-Enviado | R-Cancelado");

        # Financial summary
        total_revenue = sum(row[4] for row in all_events);
        page_revenue = sum(row[4] for row in page_records);

        # User options
        user_option = input(
            f"\n   \033[35mPágina {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1 if total_records else 1}\033[0m"
            f"{'\033[35mTotal Ganho:\033[0m ':>65}{total_revenue}€"
            f"\t\033[35mTotal da Página:\033[0m {page_revenue}€"
            "\n\n   \033[35m1.\033[0m Criar Evento"
            "   \033[35m2.\033[0m Editar Evento"
            "   \033[35m3.\033[0m Página Anterior"
            "   \033[35m4.\033[0m Página Seguinte"
            "   \033[35m5.\033[0m Menu Principal\n\n  > "
        );

        if user_option == "1": add_event();
        elif user_option == "2": edit_events.edit();
        elif user_option == "3":
            if current_page > 0: current_page -= 1;
        elif user_option == "4":
            if end_index < total_records: current_page += 1;
            else: current_page = 0;
        elif user_option == "5": return;
        else: continue;


# ==============================
# Add New Event
# ==============================

def add_event():
    """Collect user input and insert a new event into database."""
    connection, cursor = get_database_connection();

    clear_screen();
    print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");

    selected_client = select_client();
    if not selected_client: return;

    # Collect event date
    event_date = input("\n   Data do evento? (YYYY/MM/DD)\n  > ");
    if len(event_date) != 10: return;

    # Collect event name
    event_name = input("\n   Nome do evento?\n  > ");
    if not event_name or len(event_name) > 50: return;

    # Collect event price
    price_input = input("\n   Preço cobrado? (€)\n  > ");
    if not price_input: return;

    try: price_value = float(price_input);
    except ValueError: return;

    # Paid status
    paid_status = input("\n   Evento pago? (S/N)\n  > ").upper();
    if paid_status not in ("S", "N"): return;

    # Event state
    event_status = input(
        "\n   Estado do evento?\n   "
        "\33[35mLegenda:\033[0m "
        "M-Marcado | C-Capturado | E-A Editar | "
        "D-Editado | S-Enviado | R-Cancelado\n  > "
    ).upper();

    if event_status not in ("M","C","E","D","S","R"): return;

    # Insert into database
    cursor.execute(
        "INSERT INTO events (date, event, client, valor, pay, estado) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (event_date, event_name, selected_client, price_value, paid_status, event_status)
    );

    connection.commit();
    connection.close();


# ==============================
# Client Selection
# ==============================

def select_client():
    """Allow user to select a client from paginated list."""
    connection, cursor = get_database_connection();

    PAGE_SIZE = 5; 
    current_page = 0;

    while True:
        cursor.execute("SELECT id, name FROM clients ORDER BY id DESC");
        clients = cursor.fetchall();
        total_clients = len(clients);

        if not clients:
            option = input(
                "\n   Nenhum cliente encontrado.\n"
                "   \033[35m1.\033[0m Criar cliente\n\n  > "
            );
            if option == "1": main_clients.add();
            else: return None;
        
            continue;

        clear_screen();
        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m\n\n   Nome do Cliente?");

        start_index = current_page * PAGE_SIZE;
        end_index = start_index + PAGE_SIZE;
        page_clients = clients[start_index:end_index];

        for index, (client_id, client_name) in enumerate(page_clients, start=1):
            print(f"   {index}. {client_name}");

        user_choice = input(
            f"\n   \033[35mPágina {current_page+1} / "
            f"{((total_clients-1)//PAGE_SIZE)+1}\033[0m"
            "   \033[35m6.\033[0m Página Anterior"
            "   \033[35m7.\033[0m Página Seguinte"
            "   \033[35m8.\033[0m Criar cliente"
            "   \033[35m9.\033[0m Menu Principal\n\n  > "
        );

        if user_choice == "6":
            if current_page > 0:
                current_page -= 1;
        elif user_choice == "7":
            if end_index < total_clients:
                current_page += 1;
            else:
                current_page = 0;
        elif user_choice == "8":
            main_clients.add();
        elif user_choice == "9":
            return None;
        elif user_choice.isdigit():
            selected_index = int(user_choice);
            if 1 <= selected_index <= len(page_clients):
                return page_clients[selected_index - 1][1];
        else:
            continue;