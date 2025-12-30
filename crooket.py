import sys
import os
import tempfile
import importlib.util
import importlib.abc

# Ensure current directory is importable
sys.path.insert(0, os.getcwd())

# Crooket keyword mappings → Python
KEYWORD_MAP = {
    "insert": "import",
    "get": "from",
    "function": "def",
    "cls": "class",
    "write": "print",
}

def translate_crooket(code: str) -> str:
    for crooket, python_kw in KEYWORD_MAP.items():
        code = code.replace(crooket, python_kw)
    return code


# -------------------------------
# Crooket Import System
# -------------------------------

class CrooketLoader(importlib.abc.Loader):
    def __init__(self, path):
        self.path = path

    def exec_module(self, module):
        with open(self.path, "r", encoding="utf-8") as f:
            crooket_code = f.read()

        python_code = translate_crooket(crooket_code)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as temp:
            temp.write(python_code)
            temp_path = temp.name

        try:
            exec(python_code, module.__dict__)
        finally:
            os.remove(temp_path)


class CrooketFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        module_name = fullname.split(".")[-1]
        search_paths = path or sys.path

        for directory in search_paths:
            crkt_file = os.path.join(directory, module_name + ".crkt")
            if os.path.isfile(crkt_file):
                loader = CrooketLoader(crkt_file)
                return importlib.util.spec_from_loader(fullname, loader)

        return None


sys.meta_path.insert(0, CrooketFinder())


# -------------------------------
# Runtime
# -------------------------------

# Persistent global runtime
RUNTIME_GLOBALS = {
    "__name__": "__main__",
    "__builtins__": __builtins__,
}

def run_code(code: str):
    try:
        translated = translate_crooket(code)
        exec(translated, RUNTIME_GLOBALS)
        print(":) | Everything perfectly ran")
    except SyntaxError as e:
        print(f":| | Paritally has ran, Error is here: {e}")
    except Exception as e:
        print(f":( | Couldnt run: {e}")


def repl():
    # Custom welcome message
    print("Crooket v1.0")
    print("     Crooket is a simple python based programming language")
    print("To learn about Crooket, go to crooket.github.io\n")

    buffer = ""
    while True:
        try:
            line = input("> ")

            # Ignore empty input
            if not line.strip():
                continue

            if line.strip() == "exit":
                break

            # Multi-line blocks
            if line.endswith(":") or buffer:
                buffer += line + "\n"
                if line.strip() == "":
                    run_code(buffer)
                    buffer = ""
            else:
                run_code(line)

        except KeyboardInterrupt:
            print("\nExited Crooket")
            break


def run_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            run_code(f.read())
    except FileNotFoundError:
        print(":( | Couldnt run: File not found")
    except Exception as e:
        print(f":( | Couldnt run: {e}")


def main():
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        repl()


if __name__ == "__main__":
    main()
