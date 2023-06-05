from dataclasses import dataclass
from typing import List
from pymongo import MongoClient


# pylint: disable=all


client = MongoClient('mongodb://localhost:27017/')
db = client['Cafeteria']
tables_collection = db['tables']
reservations_collection = db['reservations']


@dataclass
class Table:
    table_name: str
    table_number: int
    table_seats: int

    def get_table_number(self) -> int:
        return self.table_number


@dataclass
class Reservations:
    reserved_by: str
    table: Table
    reservation_time: str


@dataclass
class Cafeteria:
    def get_table_by_number(self, table_number: int) -> Table:
        table_data = tables_collection.find_one({'table_number': table_number})
        if table_data:
            return Table(table_data['table_name'], table_data['table_number'], table_data['table_seats'])
        return None

    def get_tables_list(self) -> List[Table]:
        tables_data = tables_collection.find()
        tables_list = []
        for table_data in tables_data:
            table = Table(
                table_data['table_name'], table_data['table_number'], table_data['table_seats'])
            tables_list.append(table)
        return tables_list

    def reserve_table(self, reserved_by: str, table_number: int, reservation_time: str) -> bool:
        table_object = self.get_table_by_number(table_number)
        if table_object is None:
            return False

        existing_reservation = reservations_collection.find_one(
            {'table.table_number': table_number})
        if existing_reservation:
            return False

        reservation_data = {
            'reserved_by': reserved_by,
            'table': {
                'table_name': table_object.table_name,
                'table_number': table_object.table_number,
                'table_seats': table_object.table_seats
            },
            'reservation_time': reservation_time
        }
        reservations_collection.insert_one(reservation_data)
        return True

    def get_reservation_info(self, table_obj: Table) -> Reservations:
        reservation_data = reservations_collection.find_one(
            {'table.table_number': table_obj.table_number})
        if reservation_data:
            return Reservations(reservation_data["reserved_by"], table_obj, reservation_data["reservation_time"])
        return None

    def get_free_tables_by_seats(self, seats: int) -> List[Table]:
        free_tables = []
        tables_data = tables_collection.find({'table_seats': {'$gte': seats}})
        for table_data in tables_data:
            table = Table(
                table_data['table_name'], table_data['table_number'], table_data['table_seats'])
            if self.get_reservation_info(table) is None:
                free_tables.append(table)
        return free_tables

    def get_reservations(self) -> List[Reservations]:
        reservations_data = reservations_collection.find()
        reservations_list = []
        for reservation_data in reservations_data:
            table_data = reservation_data['table']
            table = Table(
                table_data['table_name'], table_data['table_number'], table_data['table_seats'])
            reservation = Reservations(
                reservation_data['reserved_by'], table, reservation_data['reservation_time'])
            reservations_list.append(reservation)
        return reservations_list

    def check_reservation_by_name(self, name: str, number: int) -> bool:
        reservation_data = reservations_collection.find_one(
            {"reserved_by": name, "table.table_number": number})
        return reservation_data is not None

    def delete_resevation_by_name(self, name: str) -> bool:
        delete_reservation = reservations_collection.delete_one(
            {"reserved_by": name})
        return delete_reservation.deleted_count > 0

    def update_reservation_time(self, name: str, new_time: str) -> bool:
        update_reservation = reservations_collection.update_one(
            {"reserved_by": name}, {"$set": {"reservation_time": new_time}})
        return update_reservation.modified_count > 0


if __name__ == "__main__":
    cafeteria = Cafeteria()

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")
    number = int(input("Please enter table number to check: "))
    if cafeteria.check_reservation_by_name(name, number):
        print(
            f"A reservation exists for {name} at table {number}.")
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
            for reservation in cafeteria.get_reservations():
                print(
                    f"Reserved by: {reservation.reserved_by}, time: {reservation.reservation_time}, table number: {reservation.table.get_table_number()}"
                )

        elif choice == 2:
            seats = int(input("How many people in your group? "))
            if seats >= 7:
                print(
                    "\nMax number of ppl per table is 6, please try to reserve table again or reserve to separate tables.")
                continue

            time = input(
                "What time would you like to reserve? Enter time in HH:MM ")
            for free_table in cafeteria.get_free_tables_by_seats(seats=seats):
                print(
                    f"Table name: {free_table.table_name}, Table number: {free_table.table_number}, Seats: {free_table.table_seats}"
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
                        f"Table name: {reserved_table.table_name}, Table number: {reserved_table.table_number}, Seats: {reserved_table.table_seats}"
                    )
                else:
                    print(
                        f"Table name: {reserved_table.table_name}, Table number: {reserved_table.table_number}, Seats: {reserved_table.table_seats} [Reserved by: {info.reserved_by}]"
                    )

        elif choice == 4:
            client_name = input("Enter the name for reservation deletion: ")
            if cafeteria.delete_resevation_by_name(client_name):
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
