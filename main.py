import argparse


def parse_csv_files(file_path: str) -> tuple[list[str], list[list[str]]]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.read().split("\n")
        header = lines[0].split(",")
        elements = [i.split(",") for i in lines[1:]]

        return header, elements
    except FileNotFoundError:
        raise FileNotFoundError("File no exists!")


def generate_payload(header: list[str], elements: list[list[str]]) -> list[tuple]:
    payload_data = []
    dict_data = []

    rate = None
    rate_value = None
    for i in elements:
        row = dict(zip(header, i))

        for key in ("hourly_rate", "rate", "salary"):
            if key in row:
                rate = int(row[key])
                rate_value = rate

        hours = int(row["hours_worked"])
        get_payload = rate * hours

        dict_data.append(row)
        payload_data.append(
            (row["department"],
             row["name"],
             hours,
             rate_value,
             get_payload)
        )

    return payload_data


def print_payload(data: list[tuple]) -> None:
    current_department = None

    sorted_data = sorted(data)
    print('PAYOUT REPORT')
    print(f"{'':<14} {'Name':<15} {'Hours':<5} {'Rate':<4} {'Payout':>3}")

    for dept, name, hours, rate, payout in sorted_data:
        if dept != current_department:
            current_department = dept
            print(f"{current_department:<20}")

        print(f"{"-" * 14} {name:<15} {hours:<5} {rate:<4} ${payout:>4}")
        print("")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    if args.report != 'payout':
        raise ValueError("Only 'payout' report is supported.")

    all_data = []
    for file in args.files:
        header, elements = parse_csv_files(file)
        all_data.extend(generate_payload(header, elements))
    print_payload(all_data)


if __name__ == "__main__":
    main()
