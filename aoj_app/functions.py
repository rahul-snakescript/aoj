import hmac
import hashlib
import time

from django.conf import settings


def calculate_fp_hash(x_login, x_fp_sequence, x_amount, x_currency_code):
    x_fp_timestamp = int(time.time())
    digest_maker = hmac.new(settings.EXACT_TRANSACTION_KEY, '', hashlib.md5)
    _format = '%(x_login)s^%(x_fp_sequence)s^%(x_fp_timestamp)s^%(x_amount)s^%(x_currency)s'
    data = _format % {'x_login': x_login,
                      'x_fp_sequence': x_fp_sequence,
                      'x_fp_timestamp': x_fp_timestamp,
                      'x_amount': x_amount,
                      'x_currency': x_currency_code}
    digest_maker.update(data)
    x_fp_hash = digest_maker.hexdigest()
    return x_fp_timestamp, x_fp_hash
