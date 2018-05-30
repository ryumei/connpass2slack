from main import _seq_days

def test_seq_days_default():
    seq_d = _seq_days()
    for i in range(7):
        next(seq_d)

def test_seq_days_1d():
    seq_d = _seq_days(max_offset=1)
    next(seq_d)
