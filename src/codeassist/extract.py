from .get_content import save 
# fn = r"C:\Users\Khan Kibria\Downloads\rust_pitch_corrector_design (1).md"

# c = get_file_content(fn)

def md2files(md_container, file_tag = "**File:**"):
    for i in md_container.split("---"):
        j = i.strip().split("\n")
        hdr = j[0].split(" ")
        if len(hdr) == 1:
            fn = hdr[0].replace(r"\_", "_")
        elif len(hdr) == 2 and hdr[0] == file_tag:
            fn = hdr[1].replace(r"\_", "_")
        else:
            continue

        cntl = []
        for line in j[1:]:
            if line[0:3] == "```":
                continue
            cntl.append(line)

        cnt = "\n".join(cntl).strip()
        if len(cnt) > 0:
            save(f'./{fn}', cnt)
