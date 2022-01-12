from pathlib import Path
import re
from textwrap import wrap

# This is free and unencumbered software released into the public domain
# under the terms of the Unlicense: https://unlicense.org/

def load(anvl: str | Path) -> list[dict[str, str]]:
    with open(anvl, "r", encoding="utf8") as fh:
        return decode(fh)


def loads(anvl: str) -> list[dict[str, str]]:
    return decode(anvl.split("\n"))


def dump(
    dicts: list[dict],
    anvl_file: str | Path,
    width: int = 80,
    indent: str = "\t",
    line_end: str = "\r\n",
):
    anvl = encode(dicts, width, indent, line_end)
    with open(anvl_file, "w", encoding="utf8", newline="") as fh:
        fh.write(anvl)


def dumps(
    dicts: list[dict], width: int = 80, indent: str = "\t", line_end: str = "\r\n"
) -> str:
    return encode(dicts, width, indent, line_end)


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


def encode(
    dicts: list[dict], width: int = 80, indent: str = "\t", line_end: str = "\r\n"
) -> str:

    anvl_rows = []
    for d in dicts:
        for k, v in d.items():
            row = f"{str(k)}: {str(v)}"
            if len(row) <= width:
                anvl_rows.append(row)
            else:
                anvl_rows.append(
                    line_end.join(wrap(row, width=width, subsequent_indent=indent))
                )
        anvl_rows.append("")

    return line_end.join(anvl_rows)
