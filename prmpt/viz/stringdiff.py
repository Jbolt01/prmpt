from difflib import ndiff

class StringDiff:
    def __init__(self):
        """
        Initializes a StringDiff object with the original and compressed strings.
        """
        pass
        
    def __call__(self, original: str, compressed: str) -> None:
        """
        Prints the visualized difference between the original and compressed strings.
        Deletions are shown in red, insertions in green, and unchanged parts in default color.

        Args:
            original (str): The original string.
            compressed (str): The compressed string.
        """
        original = str(original)
        compressed = str(compressed)

        diff = list(ndiff(original, compressed))
        output = ""
        for op, _, value in diff:
            if op == "-":
                output += f"\033[91m{value}\033[0m"  # Red color for deletions
            elif op == "+":
                output += f"\033[92m{value}\033[0m"  # Green color for insertions
            else:
                output += value
        print(output)