import sqlite3;
import os;


# ==============================
# Utility Functions
# ==============================

def clear_screen():
    """Clear console screen (Windows only)."""
    os.system("cls");


def get_database_connection():
    """Ensure database exists and return connection + cursor."""
    db_folder = "./bin";
    os.makedirs(db_folder, exist_ok=True);
    db_path = os.path.join(db_folder, "database.db");
    connection = sqlite3.connect(db_path);
    cursor = connection.cursor();
    return connection, cursor;


# ==============================
# Public Entry Point
# ==============================

def edit():
    """Main entry point for editing clients."""
    client_id = search_client();
    if client_id:
        edit_client_by_id(client_id);


# ==============================
# Client Search Engine
# ==============================

def search_client():
    """
    Allow user to select a client using pagination.
    Returns selected client ID or None.
    """
    connection, cursor = get_database_connection();

    cursor.execute(
        "SELECT id, name, local FROM clients ORDER BY name ASC"
    );

    results = cursor.fetchall();

    if not results:
        connection.close();
        input("\n   Nenhum cliente encontrado. Prima Enter para continuar.");
        return None;

    PAGE_SIZE = 15;
    current_page = 0;
    total_records = len(results);

    while True:
        clear_screen();

        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mCLIENTES\033[0m"
              f"\n\n   {'  ':<3}{'NOME':<22}{'LOCAL':<25}");

        start_index = current_page * PAGE_SIZE;
        end_index = start_index + PAGE_SIZE;
        page_records = results[start_index:end_index];

        for index, (client_id, name, local) in enumerate(page_records, start=1):
            print(f"   \033[35m{index}. \033[0m{name:<22}{local:<25}");

        user_option = input(
            f"\n   \033[35mPágina {current_page+1} / "
            f"{((total_records-1)//PAGE_SIZE)+1}\033[0m"
            "\n\n   \033[35m6.\033[0m Página Anterior"
            "   \033[35m7.\033[0m Página Seguinte"
            "   \033[35m8.\033[0m Cancelar\n\n  > "
        );

        if user_option == "6":
            if current_page > 0:
                current_page -= 1;
        elif user_option == "7":
            if end_index < total_records:
                current_page += 1;
            else:
                current_page = 0;
        elif user_option == "8":
            connection.close();
            return None;
        elif user_option.isdigit():
            selected_index = int(user_option);
            if 1 <= selected_index <= len(page_records):
                connection.close();
                return page_records[selected_index - 1][0];
        else:
            continue;


# ==============================
# Client Editor
# ==============================

def edit_client_by_id(client_id):
    """
    Edit a specific client field.
    Only updates the selected column.
    """
    connection, cursor = get_database_connection();

    cursor.execute(
        "SELECT id, name, local, phone, email FROM clients WHERE id = ?",
        (client_id,)
    );

    result = cursor.fetchone();

    if not result:
        connection.close();
        return;

    id_, name, local, phone, email = result;

    clear_screen();

    print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mCLIENTES\033[0m\n");
    print(f"   Nome: {name}");
    print(f"   Local: {local}");
    print(f"   Telemóvel: {phone}");
    print(f"   Email: {email}");

    confirm = input("\n   Confirmar cliente para editar? (S/N)\n  > ").upper();

    if confirm != "S":
        connection.close();
        return;

    selected_field = choose_field_to_edit();

    if not selected_field:
        connection.close();
        return;

    new_value = collect_new_value(selected_field);

    if new_value is None:
        connection.close();
        return;

    cursor.execute(
        f"UPDATE clients SET {selected_field}=? WHERE id=?",
        (new_value, client_id)
    );

    connection.commit();
    connection.close();


# ==============================
# Field Selection
# ==============================

def choose_field_to_edit():
    """Return selected database column name."""
    while True:
        clear_screen();

        print("─"*58,"•","─"*58,"\n"," "*54,"\033[35mCLIENTES\033[0m");

        option = input(
            "\n   O que pretende editar?\n\n"
            "   \033[35m1.\033[0m Nome\n"
            "   \033[35m2.\033[0m Localidade\n"
            "   \033[35m3.\033[0m Telemóvel\n"
            "   \033[35m4.\033[0m Email\n"
            "   \033[35m5.\033[0m Cancelar\n\n  > "
        );

        if option == "1":
            return "name";
        elif option == "2":
            return "local";
        elif option == "3":
            return "phone";
        elif option == "4":
            return "email";
        elif option == "5":
            return None;
        else:
            continue;


# ==============================
# Input Validation Layer
# ==============================

def collect_new_value(field):
    """
    Collect and validate new value based on selected field.
    Returns validated value or None.
    """

    if field == "name":
        value = input("\n   Novo nome\n  > ");
        if not value or len(value) > 25:
            return None;

    elif field == "local":
        value = input("\n   Nova localidade\n  > ");
        if len(value) > 25:
            return None;

    elif field == "phone":
        value = input("\n   Novo contacto\n  > ");
        if len(value) > 15:
            return None;

    elif field == "email":
        value = input("\n   Novo email\n  > ");
        if len(value) > 30:
            return None;

    else:
        return None;

    return value;