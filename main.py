class Table:
    def __init__(self, type: str,  number: int, capacity: int):
        self._number: int = number
        self._capacity: int = capacity
        self._reserved_by = None
        self._type: str = type

    def is_free(self):
        return self._reserved_by is None

    def reserve(self, name):
        self._reserved_by = name

    def unreserve(self):
        self._reserved_by = None

    def get_status(self):
        if self.is_free():
            return f"Table {self._number} [{self._type} - { self._capacity} ppl] - free"
        else:
            return f"Table {self._number} [{self._type} - { self._capacity} ppl] - reserved by {self._reserved_by}"


class Reservation:
    def __init__(self, name, table, time):
        self._name = name
        self._table = table
        self._time = time

    def info(self):
        if self._table.is_free():
            return f"Table {self._table._number} is free."
        else:
            return f"{self._table.get_status()} at {self._time}"


class Restaurant:
    def __init__(self):
        self._tables = [
            Table("Single", 1, 2),
            Table("Single", 2, 2),
            Table("Double", 3, 4),
            Table("Double", 4, 4),
            Table("Family", 5, 6),
            Table("Family", 6, 6)
        ]
        self._reservations = []

    def get_free_tables(self):
        return [table for table in self._tables if table.is_free()]

    def show_table_status(self):
        free_tables = self.get_free_tables()
        occupied_tables = [
            table for table in self._tables if not table.is_free()]

        print("Free tables:")
        for table in free_tables:
            print(table.get_status())

        print("\nOccupied tables:")
        for table in occupied_tables:
            print(table.get_status())

    def reserve_table(self, name, capacity, time):
        available_tables = [table for table in self._tables if table.is_free(
        ) and table._capacity >= capacity]

        if len(available_tables) == 0:
            print("Sorry, there are no available tables.")
            return

        print("Available tables:")
        for i, table in enumerate(available_tables):
            print(f"{i+1}. {table.get_status()}")

        choice = int(input("Enter table number to reserve: "))
        table = available_tables[choice]
        table.reserve(name)
        reservation = Reservation(name, table, time)
        self._reservations.append(reservation)
        print(f"Table {table._number} reserved for {name} at {time}.")

    def show_reservation(self, number):
        table = self._tables[number - 1]
        if table.is_free():
            print(f"Table {table._number} is free.")
        else:
            reservation = next(
                (r for r in self._reservations if r._table == table), None)
            if reservation:
                print(reservation.info())
            else:
                print(f"Table {table._number} is reserved.")


restaurant = Restaurant()

print("Welcome to our Cafeteria!")
name = input("Please enter your name: ")

while True:
    print("\nWhat would you like to do?")
    print("1. Reserve a table")
    print("2. View table status")
    print("3. View reservation information")
    print("4. Quit")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        capacity = int(input("How many people in your group? "))
        time = input(
            "What time would you like to reserve? Enter time in HH:MM ")
        restaurant.reserve_table(name, capacity, time)

    elif choice == 2:
        restaurant.show_table_status()

    elif choice == 3:
        number = int(input("Enter table number: "))
        restaurant.show_reservation(number)

    elif choice == 4:
        break
