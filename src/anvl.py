from pathlib import Path
import re
from textwrap import wrap


def load(anvl: str | Path) -> list[dict[str, str]]:
    with open(anvl, "r", encoding="utf8") as fh:
        return decode(fh)


def loads(anvl: str) -> list[dict[str, str]]:
    return decode(anvl.split("\n"))


def dump(dicts: list[dict], anvl_file: str | Path, width: int = 80):
    anvl = encode(dicts, width)
    with open(anvl_file, "w", encoding="utf8") as fh:
        fh.write(anvl)


def dumps(dicts: list[dict], width: int = 80) -> str:
    return encode(dicts, width)


def decode(lines: list[str]) -> list[dict[str, str]]:
    records = []
    indented = re.compile(r"^\s+\S")
    current_record = {}

    for line in lines:
        if line.startswith("#"):
            continue
        elif ":" in line:
            k, v = line.split(":", 1)
            current_record[k.strip()] = v.strip()
        elif re.match(indented, line):
            last_key = list(current_record.keys())[-1]
            current_record[last_key] = " ".join(
                [current_record[last_key], line.strip()]
            )
        elif line.strip() == "":
            if len(current_record) > 0:
                records.append(dict(current_record))
                current_record = {}

    if len(current_record) > 0:
        records.append(current_record)

    return records


def encode(dicts: list[dict], width: int = 80) -> str:
    anvl_rows = []
    for d in dicts:
        for k, v in d.items():
            row = f"{str(k)}: {str(v)}"
            if len(row) <= width:
                anvl_rows.append(row)
            else:
                anvl_rows.append(
                    "\n".join(wrap(row, width=width, subsequent_indent="\t"))
                )
        anvl_rows.append("")

    return "\n".join(anvl_rows)
