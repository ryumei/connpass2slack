from main import _seq_days
from main import _date_str

def test_seq_days_default():
    seq_d = _seq_days()
    for i in range(7):
        next(seq_d)

def test_seq_days_1d():
    seq_d = _seq_days(max_offset=1)
    next(seq_d)

def test_date_str():
    assert "01/01 00:00" == _date_str("2018-01-01T00:00:00+09:00")
    assert "02/01 00:00" == _date_str("2018-02-01T00:00:00+00:00")

    assert "01/01 00:00" == _date_str("2018-01-01T00:00:00+0900")
    