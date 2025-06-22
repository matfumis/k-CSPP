import os

def truncate_after_marker(root_dir, marker="Time complete formulation"):
    
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            file_path = os.path.join(dirpath, fname)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                # cerca il marker
                for idx, line in enumerate(lines):
                    if marker in line:
                        # tronca tutto da idx in poi
                        new_lines = lines[:idx]
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)
                        print(f"Truncated '{file_path}' at line {idx+1}.")
                        break
                else:
                    # marker non trovato: lascia il file invariato
                    pass
            except Exception as e:
                print(f"Errore su '{file_path}': {e}")

if __name__ == "__main__":
    # cartella radice contenente tutte le sottocartelle di results
    ROOT_RESULTS = "results"
    truncate_after_marker(ROOT_RESULTS)
