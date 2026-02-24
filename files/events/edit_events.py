import sqlite3; 
import os;

from events import main_events;


# ==============================
# Utility Functions
# ==============================

def clear_screen():
    """Clear console screen (Windows)."""
    os.system("cls");


def get_database_connection():
    """Create database folder if needed and return connection + cursor."""
    db_folder = "./bin";
    os.makedirs(db_folder, exist_ok=True);
    db_path = os.path.join(db_folder, "database.db");
    connection = sqlite3.connect(db_path);
    cursor = connection.cursor();
    return connection, cursor;


# ==============================
# Main Edit Menu
# ==============================

def edit():
    """Main edit entry point."""
    while True:
        clear_screen();
        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");

        user_option = input(
            "\n   Pesquisar por?\n\n"
            "   \033[35m1.\033[0m Data\n"
            "   \033[35m2.\033[0m Evento\n"
            "   \033[35m3.\033[0m Cliente\n"
            "   \033[35m4.\033[0m Menu Principal\n\n  > "
        );

        if user_option == "1":
            event_id = search_event("date");
        elif user_option == "2":
            event_id = search_event("event");
        elif user_option == "3":
            event_id = search_event("client");
        elif user_option == "4":
            return;
        else:
            continue;

        if event_id:
            edit_event_by_id(event_id);


# ==============================
# Event Search Engine
# ==============================

def search_event(search_type):
    """
    Generic search handler.
    search_type: 'date', 'event', or 'client'
    Returns selected event ID.
    """
    connection, cursor = get_database_connection();

    if search_type == "date":
        search_value = input("\n   Qual data quer pesquisar? (YYYY/MM/DD)\n\n  > ");
        if len(search_value) != 10:
            return None;
        cursor.execute("SELECT * FROM events WHERE date = ?", (search_value,));

    elif search_type == "event":
        search_value = input("\n   Qual evento quer pesquisar?\n\n  > ");
        if not search_value or len(search_value) > 50:
            return None;
        cursor.execute("SELECT * FROM events WHERE event = ?", (search_value,));

    elif search_type == "client":
        search_value = main_events.select_client();
        if not search_value:
            return None;
        cursor.execute("SELECT * FROM events WHERE client = ?", (search_value,));

    results = cursor.fetchall();

    if not results:
        input("\n   Nenhum evento encontrado. Prima Enter para continuar.");
        return None;

    PAGE_SIZE = 15;
    current_page = 0;
    total_records = len(results);

    while True:
        clear_screen();
        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m"
              f"\n\n   {'  ':<3}{'DATA':<12}{'EVENTO':<50}{'CLIENTE':<25}");

        start_index = current_page * PAGE_SIZE;
        end_index = start_index + PAGE_SIZE;
        page_records = results[start_index:end_index];

        for index, (event_id, date, event_name, client_name, price, paid, status) in enumerate(page_records, start=1):
            print(f"   \033[35m{index}. \033[0m{date:<12}{event_name:<50}{client_name:<25}");

        user_choice = input(
            f"\n   \033[35mPágina {current_page+1} / {((total_records-1)//PAGE_SIZE)+1}\033[0m"
            "\n\n   \033[35m6.\033[0m Página Anterior"
            "   \033[35m7.\033[0m Página Seguinte"
            "   \033[35m8.\033[0m Cancelar\n\n  > "
        );

        if user_choice == "6":
            if current_page > 0:
                current_page -= 1;
        elif user_choice == "7":
            if end_index < total_records:
                current_page += 1;
            else:
                current_page = 0;
        elif user_choice == "8":
            return None;
        elif user_choice.isdigit():
            selected_index = int(user_choice);
            if 1 <= selected_index <= len(page_records):
                return page_records[selected_index - 1][0];
        else:
            continue;


# ==============================
# Event Editor
# ==============================

def edit_event_by_id(event_id):
    """Allow user to edit a specific event field."""
    connection, cursor = get_database_connection();

    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,));
    result = cursor.fetchone();

    if not result:
        return;

    id_, date, event_name, client_name, price, paid, status = result;

    clear_screen();
    print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m\n");

    print(f"   {'DATA':<12}{'EVENTO':<50}{'CLIENTE':<25}"
          f"{'VALOR':<14}{'PAGO':<7}{'ESTADO':<3}");
    print(f"   {date:<12}{event_name:<50}{client_name:<25}"
          f"{price:>10.2f}€{paid:^10}{status:^5}");

    confirm = input("\n   Confirmar evento para editar? (S/N)\n  > ").upper();
    if confirm != "S":
        return;

    # Ask which field to edit
    field_option = choose_field_to_edit();
    if not field_option:
        return;

    # Update only selected field
    if field_option == "client":
        new_value = main_events.select_client();
    elif field_option == "date":
        new_value = input("\n   Nova data (YYYY/MM/DD)\n  > ");
        if len(new_value) != 10:
            return;
    elif field_option == "event":
        new_value = input("\n   Novo nome do evento\n  > ");
        if not new_value:
            return;
    elif field_option == "valor":
        try:
            new_value = float(input("\n   Novo preço (€)\n  > "));
        except ValueError:
            return;
    elif field_option == "pay":
        new_value = input("\n   Pago? (S/N)\n  > ").upper();
        if new_value not in ("S","N"):
            return;
    elif field_option == "estado":
        new_value = input(
            "\n   Novo estado (M,C,E,D,S,R)\n  > "
        ).upper();
        if new_value not in ("M","C","E","D","S","R"):
            return;
    else:
        return;

    cursor.execute(
        f"UPDATE events SET {field_option}=? WHERE id=?",
        (new_value, event_id)
    );

    connection.commit();
    connection.close();


# ==============================
# Field Selector
# ==============================

def choose_field_to_edit():
    """Return database field name selected by user."""
    while True:
        clear_screen();
        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mEVENTOS\033[0m");

        option = input(
            "\n   O que pretende editar?\n\n"
            "   \033[35m1.\033[0m Cliente\n"
            "   \033[35m2.\033[0m Data\n"
            "   \033[35m3.\033[0m Evento\n"
            "   \033[35m4.\033[0m Preço\n"
            "   \033[35m5.\033[0m Pago?\n"
            "   \033[35m6.\033[0m Estado\n"
            "   \033[35m7.\033[0m Cancelar\n\n  > "
        );

        if option == "1":
            return "client";
        elif option == "2":
            return "date";
        elif option == "3":
            return "event";
        elif option == "4":
            return "valor";
        elif option == "5":
            return "pay";
        elif option == "6":
            return "estado";
        elif option == "7":
            return None;
        else:
            continue;