import datetime
from typing import List


class Table:
    def __init__(self, table_number: int, capacity: int,) -> None:
        self.table_number: int = table_number
        self.capacity: int = capacity
        self.reserved_by: str = None

    def is_free(self):
        return self.reserved_by is None

    def reserve(self, name: str):
        self.reserved_by = name

    def get_status(self) -> str:
        if self.is_free():
            return f"Table {self.table_number} - [{ self.capacity} ppl] - free"
        else:
            return f"Table {self.table_number} - [{ self.capacity} ppl] - reserved by {self.reserved_by}, {time}."


class Reservation:
    def __init__(self, name: str, time: datetime) -> None:
        self.name = name
        self.time = time


class Meniu:
    pass


class Order:
    pass


class Cafeteria:
    def __init__(self) -> List:
        self.tables = [
            Table(1, 2),
            Table(2, 2),
            Table(3, 4),
            Table(4, 4),
            Table(5, 6),
            Table(6, 6)
        ]

        self.reservations: List = []

    def get_free_tables(self) -> List:
        return [table for table in self.tables if table.is_free()]

    def show_table_status(self) -> None:
        free_tables = self.get_free_tables()
        occupied_tables = [
            table for table in self.tables if not table.is_free()]

        print("Free tables:")
        for table in free_tables:
            print(table.get_status())

        print("\nOccupied tables:")
        for table in occupied_tables:
            print(table.get_status())

    def reserve_table(self, name: str, capacity: int, time: datetime) -> None:
        available_tables = [table for table in self.tables if table.is_free(
        ) and table.capacity >= capacity]

        if len(available_tables) == 0:
            print("Sorry, there are no available tables.")
            return

        print("Available tables:")
        for _, table in enumerate(available_tables):
            print(f"{_+1}. {table.get_status()}")

        choice = int(input("Enter table number to reserve: "))
        table = available_tables[choice]
        table.reserve(name)
        reservation = Reservation(name, time)
        self.reservations.append(reservation)
        print(f"Table {table.table_number} reserved for {name} at {time}.")


cafeteria = Cafeteria()

print("Welcome to our Cafeteria!")
name = input("Please enter your name: ")


while True:
    print("\nWhat would you like to do?")
    print("1. Reserve a table")
    print("2. View table status")
    print("3. Quit")

    choice = int(input("Enter your choice (1-3): "))

    if choice == 1:
        capacity = int(input("How many people in your group? "))
        time = input(
            "What time would you like to reserve? Enter time in HH:MM ")
        cafeteria.reserve_table(name, capacity, time)

    elif choice == 2:
        cafeteria.show_table_status()

    elif choice == 3:
        break
