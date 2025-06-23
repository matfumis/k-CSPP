import os

def truncate_after_marker(root_dir, marker="Time complete formulation"):
    
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            file_path = os.path.join(dirpath, fname)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                for idx, line in enumerate(lines):
                    if marker in line:
                        new_lines = lines[:idx]
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        print(f"Truncated '{file_path}' at line {idx+1}.")
                        break
                else:
                    pass
            except Exception as e:
                print(f"Errore su '{file_path}': {e}")

if __name__ == "__main__":
    ROOT_RESULTS = "results"
    truncate_after_marker(ROOT_RESULTS)
