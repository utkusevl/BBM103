import sys

#Creates the table.
def CREATE_TABLE(table_name, columns):
    try:
        if table_name in database:
            raise ValueError(f"Table '{table_name}' already exists.")
        if not columns:
            raise ValueError("Columns must be provided.")
        database[table_name] = {"columns": columns, "rows": []}
        print()
        print(f"###################### CREATE #########################")
        print(f"Table '{table_name}' created with columns: {columns}")
        print(f"#######################################################")
    except ValueError as e:
        print(f"Error: {e}")

# This function inserts values into the specified table in the database.
def INSERT(table_name, values):
    try:
        if table_name not in database:
            raise ValueError(f"Table '{table_name}' does not exist.")
        table = database[table_name]
        columns = table["columns"]

        for value in values:
            if value is None or value == "":
                raise ValueError("None or empty values are not allowed.")

        if len(values) > len(columns):
            for i in range(len(columns), len(values)):
                columns.append(f"column_{i + 1}")
        table["rows"].append(values)
        print()
        print(f"###################### INSERT #########################")
        print(f"Inserted into '{table_name}': {tuple(values)}")
        print()
        PRINT_TABLE(table_name)
        print(f"#######################################################")
    except ValueError as e:
        print()
        print(f"###################### INSERT #########################")
        print(f"Table {table_name} not found")
        print(f"Inserted into '{table_name}': {tuple(values)}")
        print(f"#######################################################")

# This function selects rows from the specified table in the database based on given columns and conditions.
def SELECT(table_name, columns=None, conditions=None):
    try:
        if table_name not in database:
            raise ValueError(f"Table {table_name} not found")
        table = database[table_name]
        rows = table["rows"]
        headers = table["columns"]
        filtered_rows = []

        if conditions:
            for row in rows:
                match = True
                for key, value in conditions.items():
                    if key not in headers:
                        raise ValueError(f"Column {key} does not exist")
                    if str(row[headers.index(key)]) != str(value):
                        match = False
                        break
                if match:
                    filtered_rows.append(row)
        else:
            filtered_rows = rows

        selected_rows = []
        if columns is columns ==["*"]:
            selected_rows = [tuple(row) for row in filtered_rows]
        else:
            for col in columns:
                if col not in headers:
                    raise ValueError(f"Column {col} does not exist")
            for row in filtered_rows:
                selected_row = tuple(row[headers.index(col)] for col in columns)
                selected_rows.append(selected_row)

        print()
        print(f"###################### SELECT #########################")
        print(f"Condition: {conditions}")
        print(f"Select result from '{table_name}': {selected_rows}")
        print(f"#######################################################")

    except ValueError as e:
        print()
        print(f"###################### SELECT #########################")
        print(e)
        print(f"Condition: {conditions}")
        print(f"Select result from '{table_name}': None")
        print(f"#######################################################")

# This function updates rows in the specified table in the database based on given updates and conditions.
def UPDATE(table_name, updates, conditions):
    try:
        if table_name not in database:
            print()
            print(f"###################### UPDATE #########################")
            print(f"Updated '{table_name}' with {updates} where {conditions}")
            print(f"Table {table_name} not found")
            print(f"0 rows updated.")
            print(f"#######################################################")
            return

        table = database[table_name]
        rows = table["rows"]
        headers = table["columns"]

        updated_count = 0

        for update_key in updates.keys():
            if update_key not in headers:
                print()
                print(f"###################### UPDATE #########################")
                print(f"Updated '{table_name}' with {updates} where {conditions}")
                print(f"Column {update_key} does not exist")
                print(f"0 rows updated.\n")
                PRINT_TABLE(table_name)
                print(f"#######################################################")
                return


        for key in conditions.keys():
            if key not in headers:
                print()
                print(f"###################### UPDATE #########################")
                print(f"Updated '{table_name}' with {updates} where {conditions}")
                print(f"Column {key} does not exist")
                print(f"0 rows updated.\n")
                PRINT_TABLE(table_name)
                print(f"#######################################################")
                return

        for row in rows:
            match = True
            for key, value in conditions.items():
                if key not in headers:
                    print()
                    print(f"###################### UPDATE #########################")
                    print(f"Updated '{table_name}' with {updates} where {conditions}")
                    print(f"Column {key} does not exist")
                    print(f"0 rows updated.\n")
                    print()
                    PRINT_TABLE(table_name)
                    print(f"#######################################################")
                    return
                if str(row[headers.index(key)]) != str(value):
                    match = False
                    break
            if match:
                for update_key, update_value in updates.items():
                    if update_key in headers:
                        row[headers.index(update_key)] = update_value
                updated_count += 1
        print()
        print(f"###################### UPDATE #########################")
        print(f"Updated '{table_name}' with {updates} where {conditions}")
        print(f"{updated_count} rows updated.")
        print()
        PRINT_TABLE(table_name)
        print(f"#######################################################")
    except ValueError as e:
        print()
        print(f"###################### UPDATE #########################")
        print(f"Error: {e}")
        print(f"Updated '{table_name}' with {updates} where {conditions}")
        print(f"0 rows updated.\n")
        PRINT_TABLE(table_name)
        print(f"#######################################################")

# This function deletes rows from the specified table in the database based on given conditions.
def DELETE(table_name, conditions):
    try:
        if table_name not in database:
            print()
            print(f"###################### DELETE #########################")
            print(f"Deleted from '{table_name}' where {conditions}")
            print(f"Table {table_name} not found")
            print(f"0 rows deleted.")
            print(f"#######################################################")
            return

        table = database[table_name]
        rows = table["rows"]
        headers = table["columns"]
        initial_count = len(rows)

        if conditions is None:
            table["rows"] = []
            print(f"###################### DELETE #########################")
            print(f"Deleted all rows from '{table_name}'")
            print(f"{initial_count} rows deleted.\n")
            print(f"#######################################################")
            return

        for key in conditions.keys():
            if key not in headers:
                print()
                print(f"###################### DELETE #########################")
                print(f"Deleted from '{table_name}' where {conditions}")
                print(f"Column {key} does not exist")
                print(f"0 rows deleted.")
                print()
                PRINT_TABLE(table_name)
                print(f"#######################################################")
                return


        updated_rows = []
        for row in rows:
            match = True
            for key, value in conditions.items():
                if str(row[headers.index(key)]) != str(value):
                    match = False
                    break
            if not match:
                updated_rows.append(row)


        table["rows"] = updated_rows
        deleted_count = initial_count - len(updated_rows)

        print()
        print(f"###################### DELETE #########################")
        print(f"Deleted from '{table_name}' where {conditions}")
        print(f"{deleted_count} rows deleted.")
        print()
        if updated_rows:
            PRINT_TABLE(table_name)
        print(f"#######################################################")
    except ValueError as e:
        print()
        print(f"###################### DELETE #########################")
        print(f"Deleted from '{table_name}' where {conditions}")
        print(f"Error: {e}")
        print(f"0 rows deleted.")
        print(f"#######################################################")

# This function counts the number of rows in the specified table in the database based on given conditions.
def COUNT(table_name, conditions=None):
    try:
        if table_name not in database:
            print()
            print(f"###################### COUNT #########################")
            print(f"Table {table_name} not found")
            print(f"Total number of entries in '{table_name}' is 0")
            print(f"#######################################################")
            return

        table = database[table_name]
        rows = table["rows"]
        headers = table["columns"]

        count = 0
        for row in rows:
            if conditions:
                match = True
                for key, value in conditions.items():
                    if key not in headers:
                        print()
                        print(f"###################### COUNT #########################")
                        print(f"Column {key} does not exist")
                        print(f"Total number of entries in '{table_name}' is 0")
                        print(f"#######################################################")
                        return
                    if str(row[headers.index(key)]) != str(value):
                        match = False
                        break
                if match:
                    count += 1
            else:
                count += 1
        print()
        print(f"###################### COUNT #########################")
        print(f"Count: {count}")
        print(f"Total number of entries in '{table_name}' is {count}")
        print(f"#######################################################")
    except ValueError as e:
        print()
        print(f"###################### COUNT #########################")
        print(f"Error: {e}")
        print(f"#######################################################")

# This function joins two tables in the database based on a common key.
def JOIN(database, table1_name, table2_name, key):
    try:
        if table1_name not in database:
            print()
            print(f"####################### JOIN ##########################")
            print(f"Join tables {table1_name} and {table2_name}")
            print(f"Table {table1_name} does not exist")
            print("#######################################################")
            return
        if table2_name not in database:
            print()
            print(f"####################### JOIN ##########################")
            print(f"Join tables {table1_name} and {table2_name}")
            print(f"Table {table2_name} does not exist")
            print("#######################################################")
            return

        table1 = database[table1_name]
        table2 = database[table2_name]
        headers1 = table1["columns"]
        headers2 = table2["columns"]
        rows1 = table1["rows"]
        rows2 = table2["rows"]

        if key not in headers1:
            print()
            print(f"####################### JOIN ##########################")
            print(f"Join tables {table1_name} and {table2_name}")
            print(f"Column {key} does not exist")
            print("#######################################################")
            return
        if key not in headers2:
            print()
            print(f"####################### JOIN ##########################")
            print(f"Join tables {table1_name} and {table2_name}")
            print(f"Column {key} does not exist")
            print("#######################################################")
            return

        key1_index = headers1.index(key)
        key2_index = headers2.index(key)

        join_headers = headers1 + headers2
        joined_rows = []
        for row1 in rows1:
            for row2 in rows2:
                if row1[key1_index] == row2[key2_index]:
                    joined_rows.append(row1 + row2)
        print()
        print(f"####################### JOIN ##########################")
        print(f"Join tables {table1_name} and {table2_name}")
        print(f"Join result ({len(joined_rows)} rows):")
        print()
        print("Table: Joined Table")
        print(format_table(joined_rows, join_headers))
        print(f"#######################################################")
    except ValueError as e:
        print()
        print(f"###################### JOIN #########################")
        print(f"Error: {e}")
        print(f"#######################################################")

# This function prints the contents of the specified table in the database.
def PRINT_TABLE(table_name):
    table = database[table_name]
    print(f"Table: {table_name}")
    print(format_table(table["rows"], table["columns"]))

# This function formats a table by adjusting column widths based on the longest value in each column and assembles the table with headers and rows.
def format_table(rows, headers):
    column_widths = [len(header) for header in headers]
    for row in rows:
        for i, value in enumerate(row):
            if i < len(column_widths):
                column_widths[i] = max(column_widths[i], len(str(value)))
            else:
                column_widths.append(len(str(value)))


    header_row = " | ".join(f"{header:{column_widths[i]}}" for i, header in enumerate(headers))

    separator = "+".join("-" * (width + 2) for width in column_widths)

    formatted_rows = [
        " | ".join(f"{str(value):{column_widths[i]}}" for i, value in enumerate(row))
        for row in rows
    ]

    # Assemble the table
    table_output = (
            f"+{separator}+\n"
            f"| {header_row} |\n"
            f"+{separator}+\n"
            + "\n".join(f"| {row} |" for row in formatted_rows)
            + f"\n+{separator}+"
    )

    return table_output

# This function processes an input file containing database commands and executes them accordingly.
def process_input_file(file_path):
    with open(file_path, 'r') as file:
        input_data = file.read()

    for command in input_data.splitlines():
        command_parts = command.split(maxsplit=1)

        if not command_parts:
            continue

        command_name = command_parts[0].upper()
        args = command_parts[1] if len(command_parts) > 1 else ""

        # CREATE_TABLE
        if command_name == "CREATE_TABLE":
            table_name, columns = args.split(maxsplit=1)
            columns = columns.split(',')
            CREATE_TABLE(table_name, columns)

        # INSERT
        elif command_name == "INSERT":
            table_name, values = args.split(maxsplit=1)
            values = values.split(',')
            INSERT(table_name, values)

        # SELECT
        elif command_name == "SELECT":
            if " WHERE " in args:
                table_info, conditions_part = args.split(" WHERE ", 1)
                conditions = eval(conditions_part)
            else:
                table_info = args
                conditions = None

            table_info_parts = table_info.split()
            table_name = table_info_parts[0]
            columns = table_info_parts[1].split(',') if len(table_info_parts) > 1 else None

            SELECT(table_name, columns, conditions)

        # UPDATE
        elif command_name == "UPDATE":
            if " WHERE " in args:
                updates_part, conditions_part = args.split(" WHERE ", 1)
                conditions = eval(conditions_part)
            else:
                updates_part = args
                conditions = None

            table_name, updates_str = updates_part.split(maxsplit=1)
            updates = eval(updates_str)

            UPDATE(table_name, updates, conditions)

        # DELETE
        elif command_name == "DELETE":
            if " WHERE " in args:
                table_name, conditions_part = args.split(" WHERE ", 1)
                conditions = eval(conditions_part)
            else:
                table_name = args
                conditions = None

            DELETE(table_name, conditions)

        # COUNT
        elif command_name == "COUNT":
            if " WHERE " in args:
                table_name, conditions_part = args.split(" WHERE ", 1)
                conditions = eval(conditions_part)
            else:
                table_name = args
                conditions = None

            COUNT(table_name, conditions)

        # JOIN
        elif command_name == "JOIN":
            if " ON " in args:
                tables_part, key = args.split(" ON ", 1)
                table1_name, table2_name = tables_part.split(',')
                JOIN(database, table1_name.strip(), table2_name.strip(), key.strip())
            else:
                print("Invalid JOIN syntax. Expected format: JOIN table1,table2 ON key")

        else:
            print(f"Unknown command: {command_name}")

# This function processes the input file and executes the database commands accordingly.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
    else:
        input_file = sys.argv[1]
        database = {}
        process_input_file(input_file)