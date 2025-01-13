def load_file(path, loader):
  """
  Loads a file using the specified loader function (e.g., YAML or JSON).

  Args:
      path (str): The file path to load.
      loader (callable): The function to use for loading the file.

  Returns:
      dict: The loaded content.

  Raises:
      FileNotFoundError: If the file does not exist.
      ValueError: If there is an error parsing the file.
  """
  try:
    with open(path, "r") as file:
      return loader(file)
  except FileNotFoundError:
    raise FileNotFoundError(f"File not found: {path}")
  except Exception as e:
    raise ValueError(f"Error loading file {path}: {e}")
