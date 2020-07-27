import pytest
from decimal import Decimal
from tariff import Tariff
from billing import Billing, WrongRecordType


def test_free_tariff():
    tariff = Tariff(
        monthly_fee=900,
        free_minutes=100,
        numbers_free_of_charge={'+420732563345', '+420707325673'},
        fee_for_minute_same_operator=Decimal(0),
        fee_for_minute_different_operator=Decimal(0),
        free_sms_count=0,
        fee_for_sms_same_operator=Decimal(0),
        fee_for_sms_different_operator=Decimal(0),
    )

    billing = Billing(tariff)
    billing.add_records_from_csv_file('test_billing_csvs/test_free_tariff.csv')
    print(billing)
    assert billing.charged_total == 0
    assert pytest.approx(billing.paid_minutes_same_operator, 39.32)
    assert billing.charged_for_minutes_same_operator == 0
    assert pytest.approx(billing.paid_minutes_different_operator, 79.78)
    assert billing.charged_for_minutes_different_operator == 0
    assert billing.paid_sms_count_same_operator == 13
    assert billing.paid_sms_count_different_operator == 15

def test_wrong_record_type():
    tariff = Tariff(
        monthly_fee=900,
        free_minutes=100,
        numbers_free_of_charge={'+420732563345', '+420707325673'},
        fee_for_minute_same_operator=Decimal(0),
        fee_for_minute_different_operator=Decimal(0),
        free_sms_count=0,
        fee_for_sms_same_operator=Decimal(0),
        fee_for_sms_different_operator=Decimal(0),
    )

    billing = Billing(tariff)
    with pytest.raises(WrongRecordType):
        billing.add_records_from_csv_file('test_billing_csvs/test_wrong_record_type.csv')
