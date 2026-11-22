#!/usr/bin/env python3
"""One-page world news poster for Saturday 21 November 2026.

The picture is painted pixel by pixel with nothing outside the
standard library.  Running the program always yields the same file:
there is no clock reading, no random source and no network access
anywhere in the drawing path.
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

# Palette, kept as plain RGB triples.
INK = (238, 234, 222)
PAPER = (17, 20, 26)
PANEL = (27, 32, 42)
RULE = (96, 108, 128)
ACCENT = (232, 176, 75)
MUTED = (168, 176, 190)
TAG = (120, 200, 215)

# A tiny typeface.  Each letter is seven rows of five marks;
# a filled cell is written with the letter x, an empty one with a dot.
GLYPHS = {
    "A": (".xxx.", "x...x", "x...x", "xxxxx", "x...x", "x...x", "x...x"),
    "B": ("xxxx.", "x...x", "x...x", "xxxx.", "x...x", "x...x", "xxxx."),
    "C": (".xxxx", "x....", "x....", "x....", "x....", "x....", ".xxxx"),
    "D": ("xxxx.", "x...x", "x...x", "x...x", "x...x", "x...x", "xxxx."),
    "E": ("xxxxx", "x....", "x....", "xxxx.", "x....", "x....", "xxxxx"),
    "F": ("xxxxx", "x....", "x....", "xxxx.", "x....", "x....", "x...."),
    "G": (".xxxx", "x....", "x....", "x..xx", "x...x", "x...x", ".xxx."),
    "H": ("x...x", "x...x", "x...x", "xxxxx", "x...x", "x...x", "x...x"),
    "I": ("xxxxx", "..x..", "..x..", "..x..", "..x..", "..x..", "xxxxx"),
    "J": ("..xxx", "...x.", "...x.", "...x.", "...x.", "x..x.", ".xx.."),
    "K": ("x...x", "x..x.", "x.x..", "xx...", "x.x..", "x..x.", "x...x"),
    "L": ("x....", "x....", "x....", "x....", "x....", "x....", "xxxxx"),
    "M": ("x...x", "xx.xx", "x.x.x", "x.x.x", "x...x", "x...x", "x...x"),
    "N": ("x...x", "xx..x", "x.x.x", "x..xx", "x...x", "x...x", "x...x"),
    "O": (".xxx.", "x...x", "x...x", "x...x", "x...x", "x...x", ".xxx."),
    "P": ("xxxx.", "x...x", "x...x", "xxxx.", "x....", "x....", "x...."),
    "Q": (".xxx.", "x...x", "x...x", "x...x", "x.x.x", "x..x.", ".xx.x"),
    "R": ("xxxx.", "x...x", "x...x", "xxxx.", "x.x..", "x..x.", "x...x"),
    "S": (".xxxx", "x....", "x....", ".xxx.", "....x", "....x", "xxxx."),
    "T": ("xxxxx", "..x..", "..x..", "..x..", "..x..", "..x..", "..x.."),
    "U": ("x...x", "x...x", "x...x", "x...x", "x...x", "x...x", ".xxx."),
    "V": ("x...x", "x...x", "x...x", "x...x", "x...x", ".x.x.", "..x.."),
    "W": ("x...x", "x...x", "x...x", "x.x.x", "x.x.x", "xx.xx", "x...x"),
    "X": ("x...x", ".x.x.", "..x..", "..x..", "..x..", ".x.x.", "x...x"),
    "Y": ("x...x", "x...x", ".x.x.", "..x..", "..x..", "..x..", "..x.."),
    "Z": ("xxxxx", "....x", "...x.", "..x..", ".x...", "x....", "xxxxx"),
    "0": (".xxx.", "x..xx", "x.x.x", "xx..x", "x...x", "x...x", ".xxx."),
    "1": ("..x..", ".xx..", "..x..", "..x..", "..x..", "..x..", ".xxx."),
    "2": (".xxx.", "x...x", "....x", "...x.", "..x..", ".x...", "xxxxx"),
    "3": ("xxxx.", "....x", "....x", ".xxx.", "....x", "....x", "xxxx."),
    "4": ("...x.", "..xx.", ".x.x.", "x..x.", "xxxxx", "...x.", "...x."),
    "5": ("xxxxx", "x....", "xxxx.", "....x", "....x", "x...x", ".xxx."),
    "6": (".xxx.", "x....", "x....", "xxxx.", "x...x", "x...x", ".xxx."),
    "7": ("xxxxx", "....x", "...x.", "..x..", "..x..", "..x..", "..x.."),
    "8": (".xxx.", "x...x", "x...x", ".xxx.", "x...x", "x...x", ".xxx."),
    "9": (".xxx.", "x...x", "x...x", ".xxxx", "....x", "....x", ".xxx."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".xx..", ".xx.."),
    ",": (".....", ".....", ".....", ".....", ".xx..", ".xx..", ".x..."),
    ":": (".....", ".xx..", ".xx..", ".....", ".xx..", ".xx..", "....."),
    ";": (".....", ".xx..", ".xx..", ".....", ".xx..", ".xx..", ".x..."),
    "'": ("..x..", "..x..", "..x..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "xxxxx", ".....", ".....", "....."),
    "/": ("....x", "....x", "...x.", "..x..", ".x...", "x....", "x...."),
    "(": ("...xx", "..x..", ".x...", ".x...", ".x...", "..x..", "...xx"),
    ")": ("xx...", "..x..", "...x.", "...x.", "...x.", "..x..", "xx..."),
    "&": (".xx..", "x..x.", "x.x..", ".x...", "x.x.x", "x..x.", ".xx.x"),
    "+": (".....", "..x..", "..x..", "xxxxx", "..x..", "..x..", "....."),
    "!": ("..x..", "..x..", "..x..", "..x..", "..x..", ".....", "..x.."),
    "?": (".xxx.", "x...x", "....x", "...x.", "..x..", ".....", "..x.."),
}


class Canvas:
    """A flat RGB buffer with a few rectangle and text helpers."""

    def __init__(self, width, height, colour):
        self.width = width
        self.height = height
        self.data = bytearray(colour) * (width * height)

    def put(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            at = (y * self.width + x) * 3
            self.data[at:at + 3] = bytes(colour)

    def fill(self, left, top, right, bottom, colour):
        for y in range(max(top, 0), min(bottom, self.height)):
            start = (y * self.width + max(left, 0)) * 3
            stop = (y * self.width + min(right, self.width)) * 3
            self.data[start:stop] = bytes(colour) * ((stop - start) // 3)

    def line(self, left, top, length, colour, thick=2):
        self.fill(left, top, left + length, top + thick, colour)

    def text(self, x, y, wording, colour, scale=2):
        cursor = x
        for ch in wording.upper():
            rows = GLYPHS.get(ch, GLYPHS["?"])
            for row_no, row in enumerate(rows):
                for col_no, mark in enumerate(row):
                    if mark == "x":
                        self.fill(cursor + col_no * scale,
                                  y + row_no * scale,
                                  cursor + (col_no + 1) * scale,
                                  y + (row_no + 1) * scale,
                                  colour)
            cursor += 6 * scale
        return cursor - x

    def text_width(self, wording, scale=2):
        return len(wording) * 6 * scale


def wrap(wording, limit):
    """Greedy word wrap returning a list of lines no longer than limit."""
    lines = []
    current = ""
    for word in wording.split():
        trial = word if not current else current + " " + word
        if len(trial) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# Each item: section label, headline, short standfirst.
ITEMS = [
    ("CLIMATE",
     "COP31 TALKS STALL IN ANTALYA",
     "Negotiators deadlocked over fossil fuel language as the "
     "summit ran past its deadline with no final deal agreed."),
    ("MIDDLE EAST",
     "IRAN STRIKES SITE IN BAHRAIN",
     "Tehran hit an industrial site and rejected new terms, "
     "raising fears of a wider regional escalation."),
    ("DIPLOMACY",
     "ZELENSKYY OPEN TO G20 TALKS",
     "Ukraine's leader said he was open to a Trump-Putin meeting "
     "on the margins of the December G20 summit."),
    ("BALTIC",
     "DRONE HITS RUSSIAN CARGO SHIP",
     "The Sparta II was struck in the Baltic Sea. The crew were "
     "reported safe and an inquiry was opened."),
    ("SECURITY",
     "FBI PROBES DATABASE INTRUSION",
     "Agents investigated a suspected hack of a national crime "
     "database after unusual access was detected."),
    ("SCIENCE",
     "RIEMANN CLAIM SHAKES MARKETS",
     "A researcher said Claude had solved the Riemann hypothesis; "
     "the claim was checked as an IPO stumble followed."),
    ("MEXICO",
     "CARTEL LEADER HELD IN SINALOA",
     "El Chapo Isidro was captured in Sinaloa in an operation "
     "in which eleven people were killed, officials said."),
    ("DISASTER",
     "M6.7 QUAKE IN CENTRAL PERU",
     "A magnitude 6.7 earthquake struck central Peru. Teams "
     "checked remote towns for damage and injuries."),
]


def paint():
    page = Canvas(WIDTH, HEIGHT, PAPER)

    # Masthead.
    title = "THE WORLD IN ONE PAGE"
    page.text((WIDTH - page.text_width(title, 4)) // 2, 28, title, INK, 4)
    page.line(36, 92, WIDTH - 72, ACCENT, 4)
    date_line = "SATURDAY 21 NOVEMBER 2026"
    page.text((WIDTH - page.text_width(date_line, 2)) // 2, 108,
              date_line, ACCENT, 2)
    sub = "EIGHT STORIES FROM AROUND THE GLOBE - UTC EDITION"
    page.text((WIDTH - page.text_width(sub, 2)) // 2, 134, sub, MUTED, 2)

    # Story grid: two columns, four rows.
    grid_top = 176
    grid_left = 28
    cell_w = 476
    cell_h = 190
    gap = 14
    for index, (label, headline, body) in enumerate(ITEMS):
        col = index % 2
        row = index // 2
        left = grid_left + col * (cell_w + gap)
        top = grid_top + row * (cell_h + gap)
        page.fill(left, top, left + cell_w, top + cell_h, PANEL)
        page.fill(left, top, left + 6, top + cell_h, ACCENT)
        inner = left + 22
        page.text(inner, top + 14, label, TAG, 2)
        y = top + 42
        for ln in wrap(headline, 30):
            page.text(inner, y, ln, INK, 2)
            y += 20
        y += 6
        for ln in wrap(body, 36):
            page.text(inner, y, ln, MUTED, 2)
            y += 20

    # Footer.
    foot_y = grid_top + 4 * cell_h + 3 * gap + 12
    page.line(36, foot_y, WIDTH - 72, RULE, 2)
    foot = "SOURCES: REUTERS - AP - BBC - AL JAZEERA"
    page.text((WIDTH - page.text_width(foot, 2)) // 2, foot_y + 12,
              foot, MUTED, 2)
    return page


def encode_png(page):
    """Serialise the canvas as a PNG with a fixed compression level."""
    raw = bytearray()
    stride = page.width * 3
    for y in range(page.height):
        raw.append(0)
        start = y * stride
        raw.extend(page.data[start:start + stride])
    packed = zlib.compress(bytes(raw), level=9)

    def chunk(kind, payload):
        body = kind + payload
        return (struct.pack(">I", len(payload)) + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", page.width, page.height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", packed)
            + chunk(b"IEND", b""))


def main():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    blob = encode_png(paint())
    with open(target, "wb") as handle:
        handle.write(blob)
    os.chmod(target, 0o644)
    print("wrote", target, len(blob), "bytes")


if __name__ == "__main__":
    main()
