import sys

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as f:
            return f"\n--- {file_path} ---\n" + f.read()
    except Exception as e:
        return f"\n--- {file_path} ---\n[Error reading file: {e}]"

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        files = [line.strip() for line in f if line.strip()]
    for file_path in files:
        print(get_file_content(file_path))
