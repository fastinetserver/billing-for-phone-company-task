from typing import Set
from decimal import Decimal


class Tariff:
    def __init__(
            self,
            monthly_fee: Decimal,
            free_minutes: int,
            numbers_free_of_charge: Set[str],
            fee_for_minute_same_operator: Decimal,
            fee_for_minute_different_operator: Decimal,
            free_sms_count: int,
            fee_for_sms_same_operator: Decimal,
            fee_for_sms_different_operator: Decimal,
    ):
        self.monthly_fee = monthly_fee
        self.free_minutes = free_minutes
        self.numbers_free_of_charge = numbers_free_of_charge
        self.fee_for_minute_same_operator = fee_for_minute_same_operator
        self.fee_for_minute_different_operator = fee_for_minute_different_operator
        self.free_sms_count = free_sms_count
        self.fee_for_sms_same_operator = fee_for_sms_same_operator
        self.fee_for_sms_different_operator = fee_for_sms_different_operator
