from up_cafeteria import Cafeteria

if __name__ == "__main__":
    cafeteria = Cafeteria()
    cafeteria._enable_schema_validation()

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")
    number = int(input("Please enter table number to check: "))
    if cafeteria.check_reservation_by_name(name, number):
        reservation_info = cafeteria.get_reservation_info(
            cafeteria.get_table_by_number(number))
        print(
            f"A reservation exists for {name}, Table {number} at {reservation_info['reservation_time']}.")
    else:
        print(
            f"No reservation found for {name} at table {number}. Please make reservation if you want to stay inside!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check reservations")
        print("2. Reserve a table")
        print("3. View all table status")
        print("4. Delete reservation")
        print("5. Update reservation time")
        print("6. Quit")

        choice = int(input("Enter your choice (1-6): "))
        if choice == 1:
            print("LIST OF RESERVATIONS: ")
            customers_reservations = cafeteria.get_reservations()
            for reservation in customers_reservations:
                print(
                    f"Reserved by: {reservation['reserved_by']}, time: {reservation['reservation_time']}, table number: {reservation['table']['table_number']}"
                )

        elif choice == 2:
            seats = int(input("How many people in your group? "))
            if seats >= 7:
                print(
                    "\nMax number of ppl per table is 6, please try to reserve table again or reserve to separate tables.")
                continue

            time = input(
                "What time would you like to reserve? Enter time in HH:MM ")
            for free_tables in cafeteria.get_free_tables_by_seats(seats=seats):
                print(
                    f"Table name: {free_tables.table_name}, Table number: {free_tables.table_number}, Seats: {free_tables.table_seats}"
                )
            selected_table = int(input("Selected table number: "))
            if cafeteria.reserve_table(name, selected_table, time):
                print(
                    f"Table {selected_table} - [{seats} ppl] - Reserved by {name}, {time}")
            else:
                print("There isn't free tables.")

        elif choice == 3:
            for reserved_table in cafeteria.get_tables_list():
                info = cafeteria.get_reservation_info(reserved_table)
                if info is None:
                    print(
                        f"Table name: {reserved_table['table_name']}, Table number: {reserved_table['table_number']}, Seats: {reserved_table['table_seats']}"
                    )
                else:
                    print(
                        f"Table name: {reserved_table['table_name']}, Table number: {reserved_table['table_number']}, Seats: {reserved_table['table_seats']} [Reserved by: {info['reserved_by']}]"
                    )

        elif choice == 4:
            client_name = input("Enter the name for reservation deletion: ")
            reservation_time = input("Enter the new reservation time: ")
            if cafeteria.delete_resevation_by_name(client_name, reservation_time):
                print(f"Successfully deleted reservation for: {client_name}")
            else:
                print(f"No reservation found for: {client_name}")

        elif choice == 5:
            reservation_name = input(
                "Enter the name of the reservation to update: ")
            new_time = input("Enter the new reservation time (HH:MM): ")
            if cafeteria.update_reservation_time(reservation_name, new_time):
                print(
                    f"Successfully updated reservation time for: {reservation_name}")
            else:
                print(f"No reservation found for: {reservation_name}")

        elif choice == 6:
            break
