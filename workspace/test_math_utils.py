from math_utils import average

def test_average_numbers():
    assert average([2,4,6])==4

def test_average_empty():
    assert average([])==0
    