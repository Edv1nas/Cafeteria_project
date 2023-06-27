# pylint: disable=all
from Utilities.database import connect_db
from Utilities.schemas import reservations_schema, tables_schema
from dataclasses import dataclass
from pymongo.errors import OperationFailure, PyMongoError
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
class Cafeteria:
    def __init__(self) -> None:
        self.database = connect_db()
        self.reservations_collection = self.database["reservations"]
        self.tables_collection = self.database["tables"]

    def _enable_schema_validation(self) -> None:
        validation_rules = reservations_schema

        try:
            self.database.command(
                'collMod', self.reservations_collection.name, **validation_rules)
            print("Reservation collection schema validation enabled.")
        except OperationFailure as e:
            print(
                f"Failed to enable reservation collection schema validation: {e.details['errmsg']}")

        validation_rules = tables_schema

        try:
            self.database.command(
                'collMod', self.tables_collection.name, **validation_rules)
            print("Tables collection schema validation enabled.")
        except OperationFailure as e:
            print(
                f"Failed to enable tables collection schema validation: {e.details['errmsg']}")

    def get_table_by_number(self, table_number: int) -> Table:
        try:
            table_data = self.tables_collection.find_one(
                {'table_number': table_number})
            if table_data:
                return Table(table_data['table_name'], table_data['table_number'], table_data['table_seats'])
        except OperationFailure as e:
            print(f"Failed to get table by number: {e.details['errmsg']}")
        return None

    def get_tables_list(self) -> List[Table]:
        try:
            tables_data = self.tables_collection.find()
            tables_list = [Table(table_data['table_name'], table_data['table_number'], table_data['table_seats'])
                           for table_data in tables_data]
            return tables_list
        except OperationFailure as e:
            print(f"Failed to get tables list: {e.details['errmsg']}")
            raise e

    def reserve_table(self, reserved_by: str, table_number: int, reservation_time: str) -> bool:
        table_object = self.get_table_by_number(table_number)
        if table_object is None:
            return False

        existing_reservation = self.reservations_collection.find_one(
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
        try:
            self.reservations_collection.insert_one(reservation_data)
        except OperationFailure as e:
            print(f"Failed to reserve table: {e.details['errmsg']}")
            return False
        return True

    def get_reservation_info(self, table_obj: Table) -> Reservations:
        try:
            reservation_data = self.reservations_collection.find_one(
                {'table.table_number': table_obj.table_number})
            return reservation_data
        except PyMongoError as err:
            print("Basic error: ", str(err))
            return None

    def get_free_tables_by_seats(self, seats: int) -> List[Table]:
        try:
            return [
                Table(table_data['table_name'],
                      table_data['table_number'], table_data['table_seats'])
                for table_data in self.tables_collection.find({'table_seats': {'$gte': seats}})
                if not self.reservations_collection.find_one({'table.table_number': table_data['table_number']})
            ]
        except OperationFailure as e:
            print(f"Failed to get free tables: {e.details['errmsg']}")

    def get_reservations(self):
        try:
            reservation_data = list(self.reservations_collection.find(
                {"reserved_by": {"$ne": " "}}))
            return reservation_data
        except OperationFailure as e:
            print(f"Failed to get reservations: {e.details['errmsg']}")
            raise e

    def check_reservation_by_name(self, name: str, number: int) -> bool:
        try:
            reservation_data = self.reservations_collection.find_one(
                {"reserved_by": name, "table.table_number": number})
            return reservation_data is not None
        except OperationFailure as e:
            print(f"Failed to check reservation: {e.details['errmsg']}")
            return False

    def delete_resevation_by_name(self, name: str, time: str) -> bool:
        try:
            delete_reservation = self.reservations_collection.delete_one(
                {"reserved_by": name, "reservation_time": time})
            return delete_reservation.deleted_count > 0
        except OperationFailure as e:
            print(f"Failed to delete reservation: {e.details['errmsg']}")
            return False

    def update_reservation_time(self, name: str, new_time: str) -> bool:
        try:
            update_reservation = self.reservations_collection.update_one(
                {"reserved_by": name}, {"$set": {"reservation_time": new_time}})
            return update_reservation.modified_count > 0
        except OperationFailure as e:
            print(f"Failed to update reservation time: {e.details['errmsg']}")
            return False
