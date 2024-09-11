import csv


def write_to_csv(json_data: list[dict]) -> None:
    csv_file_path = 'output.csv'

    # Extract the header from the keys of the first JSON object
    header = json_data[0].keys()

    # Write JSON data to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)

        # Write the header
        writer.writeheader()

        # Write the rows
        writer.writerows(json_data)