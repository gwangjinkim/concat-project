def write_output(output_path, base_path, files, tree_string):
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(";;;; FILE STRUCTURE\n")
        out.write("tree_string + "\n\n")
        
        for rel_path, abs_path in files:
            out.write(f";;;; {rel_path}\n")
            with open(abs_path, "r", encoding="utf-8") as f:
                out.write(f.read())
            out.write("\n\n")
