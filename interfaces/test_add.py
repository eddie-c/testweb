import pytest
import time

@pytest.mark.parametrize("userdict",[(1,2,3),(3,4,5)])
def test_add(userdict):
    time.sleep(2)
    assert userdict[0]+userdict[1] == userdict[2]


def test_fail():
    a = "asdf" 
    assert a == "asdf"