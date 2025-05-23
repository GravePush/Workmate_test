import pytest

from main import parse_csv_files, generate_payload


@pytest.mark.parametrize(
    "file_path, should_succeed", [
        ("test_files/data1.csv", True),
        ("test_files/noexist.csv", False),
    ]
)
def test_parse_csv_files(file_path, should_succeed):
    if should_succeed:
        header, elements = parse_csv_files(file_path)
        assert isinstance(header, list)
        assert isinstance(elements, list)
        assert len(header) > 0
        assert len(elements) > 0
    else:
        with pytest.raises(FileNotFoundError):
            parse_csv_files(file_path)


@pytest.mark.parametrize(
    "header, elements, expected_result",
    [
        (
            ["department", "name", "hours_worked", "rate"],
            [["IT", "Alice", "10", "100"]],
            [("IT", "Alice", 10, 100, 1000)]
        ),
        (
            ["department", "name", "hours_worked", "hourly_rate"],
            [["HR", "Bob", "20", "50"]],
            [("HR", "Bob", 20, 50, 1000)]
        ),
        (
            ["department", "name", "hours_worked", "salary"],
            [["Finance", "John", "15", "200"]],
            [("Finance", "John", 15, 200, 3000)]
        ),
    ]
)
def test_generate_payload(header, elements, expected_result):
    result = generate_payload(header, elements)
    assert result == expected_result