from dataclasses import dataclass
from typing import List


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
class Menu:
    pass


@dataclass
class Order:
    pass


@dataclass
class Cafeteria:
    reservation_list = []

    def get_table_by_number(self, table_number: int) -> Table:
        for table in self.tables_list:
            if table.get_table_number() == table_number:
                return table
        return None

    def get_tables_list(self):
        return self.tables_list

    def reserve_table(
        self, reserved_by: str, table_number: int, reservation_time: str
    ) -> bool:
        table_object = self.get_table_by_number(table_number)
        if table_object is None:
            return False

        for reservarion in self.reservation_list:
            if reservarion.table.get_table_number() == table_number:
                return False

        self.reservation_list.append(
            Reservations(reserved_by, table_object, reservation_time)
        )
        return True

    def get_reservation_info(self, table_obj: Table) -> Reservations:
        for reserv in self.reservation_list:
            if reserv.table == table_obj:
                return reserv
        return None

    def get_free_tables_by_seats(self, seats: int):
        free_tables = []
        for table in self.tables_list:
            if table.table_seats >= seats:
                if self.get_reservation_info(table) is None:
                    free_tables.append(table)
        return free_tables

    def get_reservations(self) -> List[Reservations]:

        return self.reservation_list

    tables_list = [
        Table("Single", table_number=1, table_seats=1),
        Table("Single", table_number=2, table_seats=1),
        Table("Single", table_number=3, table_seats=1),
        Table("Double", table_number=4, table_seats=2),
        Table("Double", table_number=5, table_seats=2),
        Table("Double", table_number=6, table_seats=2),
        Table("Family", table_number=7, table_seats=6),
        Table("Family", table_number=8, table_seats=6),
        Table("Family", table_number=9, table_seats=6),
    ]


if __name__ == "__main__":
    cafeteria = Cafeteria()

    print("Welcome to our Cafeteria!")
    name = input("Please enter your name: ")

    while True:
        print("\nWhat would you like to do?")
        print("1. Check my reservation")
        print("2. Reserve a table")
        print("3. View all table status")
        print("4. Quit")

        choice = int(input("Enter your choice (1-4): "))
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
                print("no")

        elif choice == 3:
            for rest_table in cafeteria.get_tables_list():
                info = cafeteria.get_reservation_info(rest_table)
                if info is None:
                    print(
                        f"Table name: {rest_table.table_name}, Table number: {rest_table.table_number}, Seats: {rest_table.table_seats}"
                    )
                else:
                    print(
                        f"Table name: {rest_table.table_name}, Table number: {rest_table.table_number}, Seats: {rest_table.table_seats} [Reserved by: {info.reserved_by}]"
                    )

        elif choice == 4:
            break
