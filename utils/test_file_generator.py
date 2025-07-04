import os
from pathlib import Path
import random
import string


def random_token() -> str:
    digits = "".join(random.choices(string.digits, k=3))
    letters = "".join(random.choices(string.ascii_uppercase, k=5))
    return f"<Tkn{digits}{letters}Tkn>"


def generate_test_file(file_path: str, num_lines: int = 10000, token_frequency: int = 100) -> None:
    """
    Generates a dummy text file where 1 in `token_frequency` lines contains a token.

    :param file_path: Path where the test file will be written
    :param num_lines: Total number of lines to write
    :param token_frequency: How often to include a token line (e.g., every 100 lines)
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for i in range(num_lines):
            if i % token_frequency == 0:
                token = random_token()
                f.write(f"This line contains a token: {token}\n")
            else:
                f.write("This is a normal dummy line without a token.\n")


if __name__ == "__main__":
    app_root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    test_files_dir = app_root_dir / "analyzer" / "test_files/"
    file_name = f"test_file_{random.randint(1000, 9999)}.txt"
    file_path = test_files_dir / file_name
    generate_test_file(file_path=file_path, num_lines=1000000, token_frequency=100)
