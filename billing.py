import os
import csv
from decimal import Decimal
from tariff import Tariff

DEBUG = os.environ.get('DEBUG', 'off').lower() == 'on'


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


class WrongRecordType(Exception):
    pass


class Billing:
    def __init__(self, a_tariff: Tariff):
        self.__tariff = a_tariff

        self.free_seconds_left = self.__tariff.free_minutes * 60
        self.free_sms_left = self.__tariff.free_sms_count

        self.paid_seconds_same_operator = 0
        self.paid_seconds_different_operator = 0
        self.paid_sms_count_same_operator = 0
        self.paid_sms_count_different_operator = 0

    @staticmethod
    def get_first_minute_full_duration(raw_duration: str):
        duration = int(raw_duration)
        return duration if duration > 60 else 60

    def spend_free_seconds(self, raw_duration: int) -> int:
        duration = self.__class__.get_first_minute_full_duration(raw_duration)
        """
        :param duration:
        :return: how many seconds not covered by free seconds
        """

        if self.free_seconds_left <= 0:
            return duration

        if self.free_seconds_left > duration:
            self.free_seconds_left -= duration
            return 0

        if self.free_sms_left < duration:
            not_covered_by_free_seconds = duration - self.free_seconds_left
            self.free_seconds_left = 0
            return not_covered_by_free_seconds

    def call_same_operator(self, record):
        debug("Calling same operator")
        paid_seconds = self.spend_free_seconds(record['duration'])
        self.paid_seconds_same_operator += paid_seconds

    def call_different_operator(self, record):
        debug("Calling different operator")
        paid_seconds = self.spend_free_seconds(record['duration'])
        self.paid_seconds_different_operator += paid_seconds

    def sms_same_operator(self, record):
        debug("SMS same operator")
        if self.free_sms_left > 0:
            self.free_sms_left -= 1
        else:
            self.paid_sms_count_same_operator += 1

    def sms_different_operator(self, record):
        debug("SMS different operator")
        if self.free_sms_left > 0:
            self.free_sms_left -= 1
        else:
            self.paid_sms_count_different_operator += 1

    def add_record(self, record):
        debug("Adding record:", record)
        if record['phone_num'] in self.__tariff.numbers_free_of_charge:
            debug("It is FREE of charge number - skipping billing")
        else:
            methods = {
                'VS': self.call_same_operator,
                'VM': self.call_different_operator,
                'SS': self.sms_same_operator,
                'SM': self.sms_different_operator,
            }
            method = methods.get(record['record_type'], None)
            if method:
                method(record)
            else:
                raise WrongRecordType("Please check the record type is correct")

    def add_records_from_csv_file(self, data_filename: str):
        row_column_names = (
            'datetime',
            'phone_num',
            'duration',
            'record_type',
        )

        debug("Importing {filename}".format(filename=data_filename))
        with open(data_filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile, fieldnames=row_column_names, delimiter=';', quotechar='"')
            for key, row in enumerate(csv_reader):
                if key == 0:
                    debug("Header:", '| '.join(row))
                else:
                    self.add_record(row)

    @property
    def paid_minutes_same_operator(self) -> Decimal:
        return Decimal(self.paid_seconds_same_operator) / 60

    @property
    def paid_minutes_different_operator(self) -> Decimal:
        return Decimal(self.paid_seconds_different_operator) / 60


    @property
    def charged_for_minutes_same_operator(self) -> Decimal:
        return self.paid_minutes_same_operator * self.__tariff.fee_for_minute_same_operator

    @property
    def charged_for_minutes_different_operator(self) -> Decimal:
        return self.paid_minutes_different_operator * self.__tariff.fee_for_minute_different_operator

    @property
    def charged_for_sms_same_operator(self) -> Decimal:
        return self.paid_sms_count_same_operator * self.__tariff.fee_for_sms_same_operator

    @property
    def charged_for_sms_different_operator(self) -> Decimal:
        return self.paid_sms_count_different_operator * self.__tariff.fee_for_sms_different_operator


    @property
    def charged_total(self) -> Decimal:
        return self.charged_for_minutes_same_operator + self.charged_for_minutes_different_operator + \
               self.charged_for_sms_same_operator + self.charged_for_sms_different_operator

    def __str__(self):
        return """
* Whole charged sum (monthly fee, calls, SMSs): {charged_total:.2f}
* Number of airtime minutes within operator‘s network: {paid_minutes_same_operator:.2f} and their charged sum: {charged_for_seconds_same_operator:.2f}
* Number of sent SMSs within operator‘s network: {paid_sms_count_same_operator} and their charged sum: {charged_for_sms_same_operator:.2f}
* Number of airtime minutes out of operator‘s network: {paid_minutes_different_operator:.2f} and their charged sum {charged_for_seconds_different_operator:.2f}
* Number of sent SMSs out of operator‘s network: {paid_sms_count_different_operator} and their charged sum: {charged_for_sms_different_operator:.2f}
        """.format(
            charged_total=self.charged_total,

            paid_minutes_same_operator=self.paid_minutes_same_operator,
            charged_for_seconds_same_operator=self.charged_for_minutes_same_operator,

            paid_sms_count_same_operator=self.paid_sms_count_same_operator,
            charged_for_sms_same_operator=self.charged_for_sms_same_operator,

            paid_minutes_different_operator=self.paid_minutes_different_operator,
            charged_for_seconds_different_operator=self.charged_for_minutes_different_operator,

            paid_sms_count_different_operator=self.paid_sms_count_different_operator,
            charged_for_sms_different_operator=self.charged_for_sms_different_operator,
        )


if __name__ == '__main__':
    tariff = Tariff(
        monthly_fee=900,
        free_minutes=100,
        numbers_free_of_charge={'+420732563345', '+420707325673'},
        fee_for_minute_same_operator=Decimal(1.50),
        fee_for_minute_different_operator=Decimal(3.50),
        free_sms_count=10,
        fee_for_sms_same_operator=Decimal(1.0),
        fee_for_sms_different_operator=Decimal(2.0),
    )

    billing = Billing(tariff)
    billing.add_records_from_csv_file('data.csv')
    print(billing)
