import pytest
from main import splitter, compare, get_filtred_data, aggregate, get_col_number, get_agg_data

# Пример данных для тестов
header = ["id", "value"]
data = [
    ["1", "10"],
    ["2", "20"],
    ["3", "15"],
    ["4", "5"],
]

# Тесты для функции splitter
def test_splitter():
    assert splitter("value>10") == ("value", "10", ">")
    assert splitter("id=1") == ("id", "1", "=")
    with pytest.raises(ValueError):
        splitter("invalid_condition")

# Тесты для функции compare
def test_compare():
    assert compare(10, ">", 5) is True
    assert compare(5, "<", 10) is True
    assert compare(10, "=", 10) is True
    assert compare(10, "<=", 10) is True
    assert compare(10, ">=", 10) is True
    assert compare(5, "<", 5) is False
    with pytest.raises(ValueError):
        compare(5, "!", 5)

# Тесты для фильтрации данных
def test_get_filtred_data():
    test_header = ["id", "value"]
    test_data = [["1", "10"], ["2", "20"], ["3", "15"], ["4", "5"]]
    test_filter_cortege = ("value", "10", ">")
    result = get_filtred_data(test_data, test_header, test_filter_cortege)
    assert result == [["2", "20"], ["3", "15"]]

# Тесты для агрегирования данных
def test_aggregate():
    assert aggregate("min", [10, 20, 15]) == 10
    assert aggregate("max", [10, 20, 15]) == 20
    assert aggregate("avg", [10, 20, 15]) == pytest.approx(15.0)
    with pytest.raises(ValueError):
        aggregate("sum", [10, 20, 15])

def test_get_col_number():
    test_header = ["a", "b", "c", "d"]
    col_name = "b"
    assert get_col_number(test_header, col_name)
    with pytest.raises(ValueError):
        get_col_number(header, "e")

def test_get_agg_data():
    assert get_agg_data(data, header, ("value", "min")) == [[5]]
    