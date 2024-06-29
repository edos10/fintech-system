import numpy_financial
from datetime import timedelta
from models import Agreements
import numpy


def calculating_payments(agreement: Agreements):
    month_int = agreement.interest / 12 /100
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
            "principal_payment": principal_payment,
            "interest_payment": interest_payment,
            "status": "FUTURE",
            "period": period,
        })
    return payments