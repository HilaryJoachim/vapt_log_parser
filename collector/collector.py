import os

def collect_logs_from_folder(folder_path: str):
    """
    Reads all log files from a folder and returns lines.
    Only .log and .txt files are processed.
    """
    collected_lines = []

    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder not found: {folder_path}")
        return []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".log") or file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    collected_lines.extend(lines)
                print(f"[OK] Loaded {file_name}")
            except Exception as e:
                print(f"[ERROR] Could not read {file_name}: {e}")

    return collected_lines
