import csv

def get_value_from_csv(csv_filepath, key_column, year, value_column):
  """
  Retrieves a value from a CSV file where a specified key matches.

  Args:
    csv_filepath: Path to the CSV file.
    key_column: Name of the column to check for the key.
    key_value: Value to match in the key column.
    value_column: Name of the column containing the desired value.

  Returns:
    The value from the value_column where the key_column matches the key_value, 
    or None if no match is found.
  """
  with open(csv_filepath, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
      if row[key_column] == year:
        return row[value_column]
  return None