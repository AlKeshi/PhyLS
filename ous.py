import os

def extract_python_code(root_folder, output_file="codes.txt"):
    with open(output_file, "w", encoding="utf-8") as out_file:
        for dirpath, _, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, root_folder)
                    try:
                        with open(file_path, "r", encoding="utf-8") as py_file:
                            code = py_file.read()
                        out_file.write(f"# {relative_path}\n")
                        out_file.write(code + "\n\n")
                    except Exception as e:
                        print(f"Could not read {file_path}: {e}")

if __name__ == "__main__":
    current_folder = os.getcwd()  # folder where script is run
    extract_python_code(current_folder)
