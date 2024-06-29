import numpy_financial
import numpy
from datetime import timedelta
from models.model_orm import Agreements

MONTHS = 12
PERCENTS = 100


def calculating_payments(agreement: Agreements):
    month_int = agreement.interest / MONTHS / PERCENTS
    payments = []
    for period in range(1, agreement.term + 1):
        principal_payment = numpy_financial.ppmt(rate=month_int, per=period, nper=agreement.term,
                                                 pv=agreement.principal)
        
        date_payment = agreement.datetime_activation + timedelta(days=(period * 30))
        interest_payment = numpy_financial.ipmt(rate=month_int, per=period, nper=agreement.term,
                                                pv=agreement.principal)
        if type(date_payment) == numpy.ndarray:
            date_payment = float(date_payment)

        if type(interest_payment) == numpy.ndarray:
            interest_payment = float(interest_payment)

        payments.append({
            "agreement_id": id,
            "payment_date": date_payment.date(),
            "payment_for_base": principal_payment,
            "payment_for_percents": interest_payment,
            "payment_status": "FUTURE",
            "number_payment": period,
        })
    return payments
