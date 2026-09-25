import binascii
import json
import re
import struct
import tempfile
import unittest
import zlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STYLESHEET = ROOT / "css" / "style.css"
CANONICAL_URL = "https://flypig23.github.io/"

EXPECTED_SECTIONS = [
    "about-me",
    "news",
    "publications",
    "projects",
]

EXPECTED_INTEREST_SENTENCE = (
    "My research interests center on Agent System, Data Mining, "
    "and AI for Science."
)

EXPECTED_NEWS = [
    "2026 — SciImpact accepted to Findings of ACL 2026.",
    (
        "2026 — MemeBridge accepted to KDD 2026, "
        "Datasets and Benchmarks Track."
    ),
]

# year, machine-readable status, exact linked title, visible status
EXPECTED_PUBLICATIONS = [
    (
        "2026",
        "peer-reviewed",
        "MemeBridge: A Dataset for Benchmarking and Mitigating the "
        "Bidirectional Cultural Gap in Meme Interpretation.",
        "KDD 2026, Datasets and Benchmarks Track",
    ),
    (
        "2026",
        "peer-reviewed",
        "SciImpact: A Multi-Dimensional, Multi-Field Benchmark for "
        "Scientific Impact Prediction.",
        "Findings of ACL 2026",
    ),
    (
        "2026",
        "preprint",
        "Inference-Time Control for Trustworthy Large Language Models.",
        "Working paper / preprint",
    ),
    (
        "2026",
        "preprint",
        "Beyond Semantic Similarity: Rethinking Retrieval for Agentic "
        "Search via Direct Corpus Interaction.",
        "arXiv preprint",
    ),
    (
        "2025",
        "preprint",
        "Survivors, Complainers, and Borderliners: Upward Bias in Online "
        "Discussions of Academic Conference Reviews.",
        "arXiv preprint",
    ),
    (
        "2025",
        "peer-reviewed",
        "TutorUp: What If Your Students Were Simulated? Training Tutors "
        "to Address Engagement Challenges in Online Learning.",
        "CHI 2025",
    ),
    (
        "2025",
        "peer-reviewed",
        "From Text to Trust: Empowering AI-assisted Decision Making with "
        "Adaptive LLM-powered Analysis.",
        "CHI 2025",
    ),
    (
        "2024",
        "thesis",
        "Mending Trust in AI: Trust Repair Policy Interventions for Large "
        "Language Models in Visual Data Journalism.",
        "Washington University in St. Louis master's thesis",
    ),
    (
        "2023",
        "peer-reviewed",
        "Synthetic Data Generation with Large Language Models for Text "
        "Classification: Potential and Limitations.",
        "EMNLP 2023",
    ),
]

EXPECTED_AUTHORS = [
    (
        "Hangxiao Zhu, Suliu Qin, Zhuoyan Li, Ming Jiang, Yu Zhang, "
        "Meng Xia"
    ),
    "Hangxiao Zhu, Yuyu Zhang, Ping Nie, Yu Zhang",
    (
        "Yuyang Bai, Zheyuan Liu, Han Yan, Zhangchen Xu, Yixin Wan, "
        "Canyu Chen, Zehong Wang, Xiangchi Yuan, Yue Huang, Guangyao "
        "Dou, Yuji Zhang, Hangxiao Zhu, Zhuofeng Li, Manling Li, "
        "Xiangliang Zhang, Mohit Bansal, Sanmi Koyejo, Kai-Wei Chang, "
        "Yu Zhang, Meng Jiang"
    ),
    (
        "Zhuofeng Li, Haoxiang Zhang, Cong Wei, Pan Lu, Ping Nie, Yi Lu, "
        "Yuyang Bai, Shangbin Feng, Hangxiao Zhu, Ming Zhong, Yuyu Zhang, "
        "Jianwen Xie, Yejin Choi, James Zou, Jiawei Han, Wenhu Chen, "
        "Jimmy Lin, Dongfu Jiang, Yu Zhang"
    ),
    "Hangxiao Zhu, Yian Yin, Yu Zhang",
    (
        "Sitong Pan, Robin Schmucker, Bernardo Garcia Bulle Bueno, "
        "Salome Aguilar Llanes, Fernanda Albo Alarcón, Hangxiao Zhu, "
        "Adam Teo, Meng Xia"
    ),
    "Zhuoyan Li, Hangxiao Zhu, Zhuoran Lu, Ziang Xiao, Ming Yin",
    "Hangxiao Zhu",
    "Zhuoyan Li, Hangxiao Zhu, Zhuoran Lu, Ming Yin",
]

EXPECTED_PUBLICATION_LINKS = [
    "https://doi.org/10.1145/3770854.3785691",
    "https://aclanthology.org/2026.findings-acl.1445/",
    "https://www.preprints.org/manuscript/202605.1041",
    "https://arxiv.org/abs/2605.05242",
    "https://arxiv.org/abs/2509.16831",
    "https://doi.org/10.1145/3706598.3713589",
    "https://doi.org/10.1145/3706598.3713133",
    "https://openscholarship.wustl.edu/eng_etds/1013/",
    "https://aclanthology.org/2023.emnlp-main.647/",
]

EXPECTED_PUBLICATION_AUXILIARY_LINKS = [
    [
        (
            "Project",
            "Project for MemeBridge",
            "https://flypig23.github.io/memebridge-homepage/",
        ),
        (
            "Dataset",
            "Dataset for MemeBridge",
            "https://drive.google.com/drive/folders/152AN3iREfi71WThArmr8OcUWM5cV8YZy",
        ),
    ],
    [
        (
            "Project",
            "Project for SciImpact",
            "https://flypig23.github.io/sciimpact-homepage/",
        ),
        (
            "Dataset and Code",
            "Dataset and Code for SciImpact",
            "https://github.com/FlyPig23/SciImpact",
        ),
    ],
    [
        (
            "Project",
            "Project for Inference-Time Control for Trustworthy "
            "Large Language Models",
            "https://leopoldwhite.github.io/"
            "Awesome-Inference-Time-Trustworthiness/",
        ),
        (
            "Code",
            "Code for Inference-Time Control for Trustworthy "
            "Large Language Models",
            "https://github.com/leopoldwhite/"
            "Awesome-Inference-Time-Trustworthiness",
        ),
    ],
    [
        (
            "Code",
            "Code for Beyond Semantic Similarity",
            "https://github.com/vvjohn/DCI",
        ),
    ],
    [],
    [],
    [],
    [],
    [],
]

PRESERVED_AND_USED_ASSETS = {
    "images/prof_pic.jpg",
    "images/tamu.png",
    "images/rev.jpg",
    "images/bears.png",
    "images/buckeye.png",
    "assets/CV_Hangxiao Zhu_2024.pdf",
}

RETAINED_BUT_UNUSED_ASSETS = {
    "images/text_to_trust.png",
    "images/tutorup.png",
    "images/syn_data.png",
}

EXPECTED_LOGO_ASSETS = {
    "images/zhu-logo.png": (210, 210),
    "images/zhu-logo-nav.png": (37, 37),
    "images/zhu-logo-nav@2x.png": (74, 74),
    "images/favicon-16.png": (16, 16),
    "images/favicon-32.png": (32, 32),
    "images/favicon-dark-16.png": (16, 16),
    "images/favicon-dark-32.png": (32, 32),
}

MAX_PNG_FILE_BYTES = 8 * 1024 * 1024
MAX_PNG_PIXELS = 1_000_000

VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

ASCII_LOWER_TABLE = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
)


def normalize_text(value):
    return " ".join(value.replace("\u00a0", " ").split())


def ascii_lower(value):
    return value.translate(ASCII_LOWER_TABLE)


class Element:
    """A deliberately small DOM element for semantic contract checks."""

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = {}
        self.duplicate_attrs = []
        for name, value in attrs or []:
            normalized_name = ascii_lower(name)
            if normalized_name in self.attrs:
                self.duplicate_attrs.append(normalized_name)
                continue
            self.attrs[normalized_name] = "" if value is None else value
        self.parent = parent
        self._content = []

    def attr(self, name, default=None):
        return self.attrs.get(ascii_lower(name), default)

    @property
    def classes(self):
        return set((self.attr("class") or "").split())

    @property
    def children(self):
        return [item for item in self._content if isinstance(item, Element)]

    @property
    def text(self):
        return normalize_text(self.raw_text())

    @property
    def visible_text(self):
        return normalize_text(self.visible_raw_text())

    def is_hidden(self):
        element = self
        while element is not None:
            if "hidden" in element.attrs:
                return True
            if (
                (element.attr("aria-hidden") or "").strip().lower()
                == "true"
            ):
                return True
            element = element.parent
        return False

    def raw_text(self):
        return "".join(
            item.raw_text() if isinstance(item, Element) else item
            for item in self._content
        )

    def visible_raw_text(self):
        if self.is_hidden():
            return ""
        return "".join(
            item.visible_raw_text() if isinstance(item, Element) else item
            for item in self._content
        )

    def descendants(self):
        for child in self.children:
            yield child
            yield from child.descendants()


class DOMParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.document = Element("#document")
        self._stack = [self.document]
        self.duplicate_attributes = []

    def append_element(self, tag, attrs, push):
        element = Element(
            ascii_lower(tag),
            attrs,
            self._stack[-1],
        )
        self._stack[-1]._content.append(element)
        self.duplicate_attributes.extend(
            (element, name) for name in element.duplicate_attrs
        )
        if push and element.tag not in VOID_ELEMENTS:
            self._stack.append(element)

    def handle_starttag(self, tag, attrs):
        self.append_element(tag, attrs, push=True)

    def handle_startendtag(self, tag, attrs):
        self.append_element(tag, attrs, push=False)

    def handle_endtag(self, tag):
        tag = ascii_lower(tag)
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data):
        self._stack[-1]._content.append(data)


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def json_types(node):
    value = node.get("@type", [])
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {item for item in value if isinstance(item, str)}
    return set()


def strip_css_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def has_css_import(css):
    css = strip_css_comments(css)
    quote = None
    escaped = False
    position = 0
    while position < len(css):
        character = css[position]
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif quote is not None:
            if character == quote:
                quote = None
        elif character in {"'", '"'}:
            quote = character
        elif character == "@" and re.match(
            r"@import\b",
            css[position:],
            re.IGNORECASE,
        ):
            return True
        position += 1
    return False


def has_visible_focus_declaration(body):
    declarations = re.finditer(
        r"(?:^|;)\s*(outline|box-shadow)\s*:\s*([^;}]+)",
        body,
        re.IGNORECASE,
    )
    for declaration in declarations:
        value = re.sub(
            r"\s*!important\s*$",
            "",
            declaration.group(2),
            flags=re.IGNORECASE,
        ).strip()
        lowered = value.lower()
        if "transparent" in lowered and "," not in value:
            continue
        if not value or lowered == "none":
            continue

        lengths = re.findall(
            r"(?<![\w.-])-?(?:\d+(?:\.\d+)?|\.\d+)(?:[a-z%]+)?",
            value,
            re.IGNORECASE,
        )
        if lengths and all(
            float(re.match(r"-?(?:\d+(?:\.\d+)?|\.\d+)", item).group())
            == 0
            for item in lengths
        ):
            continue
        return True
    return False


def matching_delimiter(value, opening, open_character, close_character):
    depth = 0
    quote = None
    escaped = False
    for index in range(opening, len(value)):
        character = value[index]
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if quote is not None:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
            continue
        if character == open_character:
            depth += 1
        elif character == close_character:
            depth -= 1
            if depth == 0:
                return index
    return -1


def css_blocks(css):
    position = 0
    statement_start = 0
    quote = None
    escaped = False
    parentheses = 0
    brackets = 0

    while position < len(css):
        character = css[position]
        if escaped:
            escaped = False
            position += 1
            continue
        if character == "\\":
            escaped = True
            position += 1
            continue
        if quote is not None:
            if character == quote:
                quote = None
            position += 1
            continue
        if character in {"'", '"'}:
            quote = character
            position += 1
            continue
        if character == "(":
            parentheses += 1
        elif character == ")" and parentheses:
            parentheses -= 1
        elif character == "[":
            brackets += 1
        elif character == "]" and brackets:
            brackets -= 1
        elif character == ";" and not parentheses and not brackets:
            statement_start = position + 1
        elif character == "{" and not parentheses and not brackets:
            closing = matching_delimiter(css, position, "{", "}")
            if closing < 0:
                return
            prelude = css[statement_start:position].strip()
            body = css[position + 1:closing]
            if prelude:
                yield prelude, body
                if prelude.lstrip().startswith("@"):
                    yield from css_blocks(body)
            position = closing
            statement_start = closing + 1
        position += 1


def split_top_level_commas(value):
    parts = []
    start = 0
    quote = None
    escaped = False
    parentheses = 0
    brackets = 0

    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if quote is not None:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == "(":
            parentheses += 1
        elif character == ")" and parentheses:
            parentheses -= 1
        elif character == "[":
            brackets += 1
        elif character == "]" and brackets:
            brackets -= 1
        elif character == "," and not parentheses and not brackets:
            parts.append(value[start:index].strip())
            start = index + 1

    parts.append(value[start:].strip())
    return [part for part in parts if part]


def without_not_pseudo_classes(selector):
    result = []
    position = 0
    pattern = re.compile(r":not\s*\(", re.IGNORECASE)

    while True:
        match = pattern.search(selector, position)
        if match is None:
            result.append(selector[position:])
            return "".join(result)
        result.append(selector[position:match.start()])
        opening = selector.find("(", match.start())
        closing = matching_delimiter(selector, opening, "(", ")")
        if closing < 0:
            return "".join(result)
        position = closing + 1


def has_positive_focus_visible(selector):
    return bool(
        re.search(
            r":focus-visible\b",
            without_not_pseudo_classes(selector),
            re.IGNORECASE,
        )
    )


def rightmost_selector_compound(selector):
    start = 0
    quote = None
    escaped = False
    parentheses = 0
    brackets = 0

    for index, character in enumerate(selector):
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
            continue
        if quote is not None:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
        elif character == "(":
            parentheses += 1
        elif character == ")" and parentheses:
            parentheses -= 1
        elif character == "[":
            brackets += 1
        elif character == "]" and brackets:
            brackets -= 1
        elif not parentheses and not brackets and (
            character.isspace() or character in {">", "+", "~"}
        ):
            start = index + 1

    return selector[start:].strip()


def has_forbidden_position(body):
    return bool(
        re.search(
            r"(?:^|;)\s*position\s*:\s*(?:fixed|absolute)\b",
            body,
            re.IGNORECASE,
        )
    )


def is_reduced_motion_media(prelude):
    return bool(
        re.match(r"@media\b", prelude, re.IGNORECASE)
        and not re.match(r"@media\s+not\b", prelude, re.IGNORECASE)
        and re.search(
            r"\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)",
            prelude,
            re.IGNORECASE,
        )
    )


def srcset_urls(value):
    """Return URL tokens while keeping commas inside data URLs intact."""
    position = 0
    length = len(value)

    while position < length:
        while position < length and (
            value[position].isspace() or value[position] == ","
        ):
            position += 1
        if position >= length:
            return

        start = position
        is_data_url = value[position:].lower().startswith("data:")
        while position < length and not value[position].isspace():
            if value[position] == "," and not is_data_url:
                break
            position += 1

        candidate = value[start:position]
        if candidate:
            yield candidate

        while position < length and value[position] != ",":
            position += 1
        if position < length:
            position += 1


def png_info(path):
    path = Path(path)
    invalid_message = f"Invalid PNG data: {path}"

    try:
        with path.open("rb") as source:
            data = source.read(MAX_PNG_FILE_BYTES + 1)
    except OSError as error:
        raise AssertionError(invalid_message) from error

    if (
        len(data) > MAX_PNG_FILE_BYTES
        or data[:8] != b"\x89PNG\r\n\x1a\n"
    ):
        raise AssertionError(invalid_message)

    width = height = color_type = bytes_per_pixel = None
    palette_entries = None
    transparency = None
    idat_parts = []
    seen_ihdr = False
    seen_idat = False
    idat_ended = False
    seen_iend = False
    offset = 8
    chunk_index = 0

    while offset < len(data):
        if len(data) - offset < 12:
            raise AssertionError(invalid_message)

        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        chunk_end = data_end + 4
        if length > MAX_PNG_FILE_BYTES or chunk_end > len(data):
            raise AssertionError(invalid_message)
        if any(
            not (65 <= byte <= 90 or 97 <= byte <= 122)
            for byte in chunk_type
        ) or 97 <= chunk_type[2] <= 122:
            raise AssertionError(invalid_message)

        payload = data[data_start:data_end]
        stored_crc = struct.unpack(">I", data[data_end:chunk_end])[0]
        calculated_crc = binascii.crc32(chunk_type)
        calculated_crc = binascii.crc32(payload, calculated_crc) & 0xFFFFFFFF
        if stored_crc != calculated_crc:
            raise AssertionError(invalid_message)

        if chunk_index == 0 and chunk_type != b"IHDR":
            raise AssertionError(invalid_message)

        if chunk_type == b"IHDR":
            if seen_ihdr or chunk_index != 0 or length != 13:
                raise AssertionError(invalid_message)
            (
                width,
                height,
                bit_depth,
                color_type,
                compression_method,
                filter_method,
                interlace_method,
            ) = struct.unpack(">IIBBBBB", payload)
            if (
                not width
                or not height
                or width * height > MAX_PNG_PIXELS
                or bit_depth != 8
                or color_type not in {0, 2, 3, 4, 6}
                or compression_method != 0
                or filter_method != 0
                or interlace_method != 0
            ):
                raise AssertionError(invalid_message)
            bytes_per_pixel = {
                0: 1,
                2: 3,
                3: 1,
                4: 2,
                6: 4,
            }[color_type]
            seen_ihdr = True
        elif not seen_ihdr:
            raise AssertionError(invalid_message)
        elif chunk_type == b"PLTE":
            if (
                seen_idat
                or palette_entries is not None
                or transparency is not None
                or color_type in {0, 4}
                or not length
                or length % 3
                or length > 768
            ):
                raise AssertionError(invalid_message)
            palette_entries = length // 3
        elif chunk_type == b"tRNS":
            if seen_idat or transparency is not None:
                raise AssertionError(invalid_message)
            if color_type == 0:
                if length != 2 or struct.unpack(">H", payload)[0] > 255:
                    raise AssertionError(invalid_message)
            elif color_type == 2:
                if length != 6 or any(
                    sample > 255
                    for sample in struct.unpack(">HHH", payload)
                ):
                    raise AssertionError(invalid_message)
            elif color_type == 3:
                if (
                    palette_entries is None
                    or not length
                    or length > palette_entries
                ):
                    raise AssertionError(invalid_message)
            else:
                raise AssertionError(invalid_message)
            transparency = payload
        elif chunk_type == b"IDAT":
            if idat_ended or (color_type == 3 and palette_entries is None):
                raise AssertionError(invalid_message)
            idat_parts.append(payload)
            seen_idat = True
        elif chunk_type == b"IEND":
            if length or not seen_idat:
                raise AssertionError(invalid_message)
            seen_iend = True
        elif chunk_type[0] <= 90:
            raise AssertionError(invalid_message)

        offset = chunk_end
        chunk_index += 1
        if seen_iend:
            break
        if seen_idat and chunk_type != b"IDAT":
            idat_ended = True

    if (
        not seen_ihdr
        or not seen_idat
        or not seen_iend
        or offset != len(data)
        or (color_type == 3 and palette_entries is None)
    ):
        raise AssertionError(invalid_message)

    row_bytes = width * bytes_per_pixel
    expected_size = height * (row_bytes + 1)
    compressed = b"".join(idat_parts)
    try:
        decompressor = zlib.decompressobj()
        scanlines = decompressor.decompress(compressed, expected_size + 1)
        if decompressor.unconsumed_tail or len(scanlines) > expected_size:
            raise AssertionError(invalid_message)
        scanlines += decompressor.flush(expected_size + 1 - len(scanlines))
    except zlib.error as error:
        raise AssertionError(invalid_message) from error

    if (
        len(scanlines) != expected_size
        or not decompressor.eof
        or decompressor.unused_data
        or decompressor.unconsumed_tail
    ):
        raise AssertionError(invalid_message)

    pixels = bytearray()
    previous = bytearray(row_bytes)
    position = 0
    for _ in range(height):
        filter_type = scanlines[position]
        position += 1
        filtered = scanlines[position:position + row_bytes]
        position += row_bytes
        current = bytearray(row_bytes)

        for index, value in enumerate(filtered):
            left = current[index - bytes_per_pixel] if (
                index >= bytes_per_pixel
            ) else 0
            above = previous[index]
            upper_left = previous[index - bytes_per_pixel] if (
                index >= bytes_per_pixel
            ) else 0

            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                estimate = left + above - upper_left
                left_distance = abs(estimate - left)
                above_distance = abs(estimate - above)
                upper_left_distance = abs(estimate - upper_left)
                if left_distance <= above_distance and (
                    left_distance <= upper_left_distance
                ):
                    predictor = left
                elif above_distance <= upper_left_distance:
                    predictor = above
                else:
                    predictor = upper_left
            else:
                raise AssertionError(invalid_message)

            current[index] = (value + predictor) & 0xFF

        pixels.extend(current)
        previous = current

    if color_type == 6:
        has_transparency = any(
            pixels[index] < 255
            for index in range(3, len(pixels), 4)
        )
    elif color_type == 4:
        has_transparency = any(
            pixels[index] < 255
            for index in range(1, len(pixels), 2)
        )
    elif color_type == 3:
        if any(index >= palette_entries for index in pixels):
            raise AssertionError(invalid_message)
        alpha_values = transparency or b""
        has_transparency = any(
            index < len(alpha_values) and alpha_values[index] < 255
            for index in pixels
        )
    elif color_type == 2 and transparency is not None:
        transparent_pixel = struct.unpack(">HHH", transparency)
        has_transparency = any(
            tuple(pixels[index:index + 3]) == transparent_pixel
            for index in range(0, len(pixels), 3)
        )
    elif color_type == 0 and transparency is not None:
        transparent_sample = struct.unpack(">H", transparency)[0]
        has_transparency = transparent_sample in pixels
    else:
        has_transparency = False

    return width, height, has_transparency


class SiteContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not INDEX.is_file():
            raise AssertionError(f"Missing homepage: {INDEX}")
        if not STYLESHEET.is_file():
            raise AssertionError(f"Missing stylesheet: {STYLESHEET}")

        cls.html = INDEX.read_text(encoding="utf-8")
        cls.css = STYLESHEET.read_text(encoding="utf-8")

        parser = DOMParser()
        parser.feed(cls.html)
        parser.close()
        cls.dom = parser.document

    def elements(self, root=None, tag=None):
        root = self.dom if root is None else root
        nodes = list(root.descendants())
        if tag is not None:
            nodes = [node for node in nodes if node.tag == tag]
        return nodes

    def with_class(self, root, class_name, tag=None):
        return [
            node
            for node in self.elements(root, tag)
            if class_name in node.classes
        ]

    def one(self, nodes, label):
        self.assertEqual(
            len(nodes),
            1,
            f"Expected exactly one {label}; found {len(nodes)}",
        )
        return nodes[0]

    def by_id(self, element_id):
        return self.one(
            [
                node
                for node in self.elements()
                if node.attr("id") == element_id
            ],
            f"element with id={element_id!r}",
        )

    def publication_rows(self):
        section = self.by_id("publications")
        rows = self.with_class(self.dom, "publication", tag="article")
        for row in rows:
            ancestor = row.parent
            while ancestor is not None and ancestor is not section:
                ancestor = ancestor.parent
            self.assertIs(
                ancestor,
                section,
                "Every article.publication must belong to #publications",
            )
        return rows

    def publication_title_link(self, row):
        title = self.one(
            self.with_class(row, "publication-title"),
            "publication title",
        )
        title_links = []
        if title.tag == "a":
            title_links.append(title)
        title_links.extend(self.elements(title, tag="a"))
        return self.one(title_links, "linked publication title")

    def section_list_items(self, section_id, container_class):
        section = self.by_id(section_id)
        container = self.one(
            self.with_class(section, container_class),
            f".{container_class} container",
        )
        self.assertIn(container.tag, {"ul", "ol"})
        self.assertTrue(
            all(child.tag == "li" for child in container.children),
            f".{container_class} may only have li element children",
        )

        for item in self.elements(section, tag="li"):
            ancestor = item.parent
            while ancestor not in {None, section, container}:
                ancestor = ancestor.parent
            self.assertIs(
                ancestor,
                container,
                f"Every #{section_id} list item must belong to the "
                f".{container_class} container",
            )

        return section, container, container.children

    def html_references(self):
        for node in self.elements():
            for attribute in ("href", "src"):
                if attribute in node.attrs:
                    yield (
                        f"<{node.tag}> {attribute}",
                        node.attr(attribute),
                        ROOT,
                    )

            if "srcset" in node.attrs:
                values = list(srcset_urls(node.attr("srcset")))
                if not values:
                    yield f"<{node.tag}> srcset", "", ROOT
                for value in values:
                    yield f"<{node.tag}> srcset", value, ROOT

    def stylesheet_sources(self):
        seen_files = {STYLESHEET.resolve()}
        seen_inline = set()

        yield "css/style.css", self.css, STYLESHEET.parent

        for link in self.elements(tag="link"):
            rel = set((link.attr("rel") or "").lower().split())
            if "stylesheet" not in rel:
                continue

            href = link.attr("href") or ""
            resolved = self.local_path(href, ROOT)
            if resolved is None:
                continue

            path, relative_path = resolved
            if path in seen_files:
                continue
            seen_files.add(path)

            try:
                css = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                raise AssertionError(
                    f"Unable to read local stylesheet: {relative_path}"
                ) from error
            yield f"stylesheet {relative_path}", css, path.parent

        inline_sources = [
            (f"<style> block {index}", style.raw_text())
            for index, style in enumerate(
                self.elements(tag="style"),
                start=1,
            )
        ]
        inline_sources.extend(
            (f"<{node.tag}> style attribute", node.attr("style") or "")
            for node in self.elements()
            if "style" in node.attrs
        )

        for source, css in inline_sources:
            key = (css, ROOT.resolve())
            if key in seen_inline:
                continue
            seen_inline.add(key)
            yield source, css, ROOT

    def all_references(self):
        yield from self.html_references()

        pattern = r"url\(\s*(['\"]?)(.*?)\1\s*\)"
        for source, css, base_dir in self.stylesheet_sources():
            css = strip_css_comments(css)
            for match in re.finditer(pattern, css, re.IGNORECASE):
                yield f"{source} url()", match.group(2), base_dir

    def local_path(self, raw_url, base_dir):
        raw_url = raw_url.strip()
        if not raw_url:
            raise AssertionError("Local reference must not be empty")

        try:
            parsed = urlsplit(raw_url)
        except ValueError as error:
            raise AssertionError(
                f"Reference is not a valid URL: {raw_url!r}"
            ) from error

        if parsed.scheme or parsed.netloc or not parsed.path:
            return None

        decoded_path = unquote(parsed.path)
        if decoded_path.startswith("/"):
            candidate = ROOT / decoded_path.lstrip("/")
        else:
            candidate = base_dir / decoded_path

        candidate = candidate.resolve()
        try:
            relative = candidate.relative_to(ROOT.resolve()).as_posix()
        except ValueError as error:
            raise AssertionError(
                f"Local reference escapes repository root: {raw_url!r}"
            ) from error

        return candidate, relative

    def test_landmarks_and_major_section_order(self):
        hero = self.by_id("hero")
        main = self.by_id("main-content")

        self.assertEqual(hero.tag, "header")
        self.assertEqual(main.tag, "main")
        self.assertEqual(
            [
                child.attr("id")
                for child in main.children
                if child.tag == "section"
            ],
            EXPECTED_SECTIONS,
        )

        document_order = self.elements()
        self.assertLess(
            document_order.index(hero),
            document_order.index(main),
            "header#hero must appear before main#main-content",
        )

    def test_html_has_no_duplicate_attributes(self):
        duplicates = [
            f"<{element.tag}> {name}"
            for element in self.elements()
            for name in element.duplicate_attrs
        ]
        self.assertEqual(
            duplicates,
            [],
            f"Duplicate HTML attributes are not allowed: {duplicates}",
        )

    def test_html_has_no_base_element(self):
        self.assertEqual(
            len(self.elements(tag="base")),
            0,
            "The site must not use a base element",
        )

    def test_primary_navigation_targets_sections_in_order(self):
        expected = [f"#{section_id}" for section_id in EXPECTED_SECTIONS]
        candidates = []
        for nav in self.elements(tag="nav"):
            hrefs = [
                anchor.attr("href")
                for anchor in self.elements(nav, tag="a")
            ]
            if any(href in expected for href in hrefs):
                candidates.append(nav)

        nav = self.one(candidates, "primary navigation")
        actual = [
            anchor.attr("href")
            for anchor in self.elements(nav, tag="a")
            if (anchor.attr("href") or "").startswith("#")
        ]
        self.assertEqual(actual, expected)

    def test_research_interests_are_integrated_into_about_copy(self):
        about = self.by_id("about-me")
        about_copy = self.one(
            self.with_class(about, "about-copy"),
            "About copy",
        )
        paragraphs = [
            element
            for element in self.elements(about_copy, tag="p")
            if EXPECTED_INTEREST_SENTENCE in element.visible_text
        ]

        self.one(paragraphs, "About paragraph containing the interests sentence")
        self.assertEqual(
            about_copy.visible_text.count(EXPECTED_INTEREST_SENTENCE),
            1,
        )

    def test_no_standalone_research_interest_markup_or_styles_remain(self):
        self.assertEqual(
            [
                element
                for element in self.elements()
                if element.attr("id") == "research-interests"
            ],
            [],
        )
        research_interest_elements = [
            element
            for element in self.elements()
            if any(
                class_name.startswith("research-interest")
                for class_name in element.classes
            )
        ]
        self.assertEqual(research_interest_elements, [])
        self.assertNotRegex(
            strip_css_comments(self.css),
            r"\.research-interest(?:-[a-z0-9_-]+)?",
        )

    def test_section_indices_match_section_order(self):
        actual = []
        for section_id in EXPECTED_SECTIONS:
            section = self.by_id(section_id)
            index = self.one(
                self.with_class(section, "section-index"),
                f"section index for #{section_id}",
            )
            actual.append(index.text)

        self.assertEqual(actual, ["01", "02", "03", "04"])

    def test_news_contains_only_the_approved_items(self):
        section, _, items = self.section_list_items("news", "news-list")
        self.assertEqual(
            self.with_class(section, "news-item", tag="li"),
            items,
        )
        self.assertEqual(
            [item.text for item in items],
            EXPECTED_NEWS,
        )

    def test_publication_contract_and_exact_order(self):
        rows = self.publication_rows()
        self.assertEqual(len(rows), len(EXPECTED_PUBLICATIONS))

        actual = []
        for row in rows:
            self.assertIn("data-status", row.attrs)
            year = self.one(
                self.with_class(row, "publication-year"),
                "publication year",
            )
            self.one(
                self.with_class(row, "publication-authors"),
                "publication authors",
            )
            status = self.one(
                self.with_class(row, "publication-status"),
                "publication status",
            )
            title_link = self.publication_title_link(row)
            self.assertTrue(title_link.attr("href"))

            actual.append(
                (
                    year.text,
                    row.attr("data-status"),
                    title_link.text,
                    status.text,
                )
            )

        self.assertEqual(actual, EXPECTED_PUBLICATIONS)

    def test_publication_primary_links_are_exact_and_ordered(self):
        actual = [
            self.publication_title_link(row).attr("href")
            for row in self.publication_rows()
        ]
        self.assertEqual(actual, EXPECTED_PUBLICATION_LINKS)

    def test_publication_auxiliary_links_are_exact_and_useful(self):
        actual = []
        for row in self.publication_rows():
            publication_bodies = [
                child
                for child in row.children
                if child.tag == "div"
                and "publication-body" in child.classes
            ]
            publication_body = self.one(
                publication_bodies,
                "publication body",
            )
            links_lists = [
                child
                for child in publication_body.children
                if child.tag == "ul"
                and "publication-links" in child.classes
            ]
            links_list = self.one(
                links_lists,
                "publication links list",
            )
            actual.append(
                (
                    self.publication_title_link(row).text,
                    [
                        (
                            link.visible_text,
                            link.attr("aria-label"),
                            link.attr("href"),
                        )
                        for link in self.elements(links_list, tag="a")
                    ],
                )
            )

        expected = [
            (publication[2], links)
            for publication, links in zip(
                EXPECTED_PUBLICATIONS,
                EXPECTED_PUBLICATION_AUXILIARY_LINKS,
            )
        ]
        self.assertEqual(actual, expected)
        flattened = [link for _, links in actual for link in links]
        self.assertNotIn(
            "DOI",
            [visible_text for visible_text, _, _ in flattened],
        )
        self.assertNotIn(
            "https://www.xiameng.org/KDD_Meme_Bridge.pdf",
            [href for _, _, href in flattened],
        )

    def test_each_publication_emphasizes_hangxiao_in_author_line(self):
        actual_authors = []
        for row in self.publication_rows():
            authors = self.one(
                self.with_class(row, "publication-authors"),
                "publication authors",
            )
            actual_authors.append(authors.text)
            emphasized_names = [
                strong.text
                for strong in self.elements(authors, tag="strong")
            ]
            self.assertIn("Hangxiao Zhu", emphasized_names)

        self.assertEqual(actual_authors, EXPECTED_AUTHORS)

    def test_exactly_three_publications_are_preprints(self):
        preprints = [
            row
            for row in self.publication_rows()
            if row.attr("data-status") == "preprint"
        ]
        self.assertEqual(len(preprints), 3)

        for row in preprints:
            status = self.one(
                self.with_class(row, "publication-status"),
                "preprint status",
            ).text.lower()
            self.assertRegex(status, r"\b(preprint|working paper)\b")
            self.assertNotIn("accepted", row.text.lower())

    def test_preserved_assets_exist_and_usage_is_correct(self):
        required_files = (
            PRESERVED_AND_USED_ASSETS | RETAINED_BUT_UNUSED_ASSETS
        )
        for relative_path in sorted(required_files):
            with self.subTest(asset=relative_path):
                self.assertTrue(
                    (ROOT / relative_path).is_file(),
                    f"Missing preserved asset: {relative_path}",
                )

        referenced = set()
        for _, raw_url, base_dir in self.html_references():
            resolved = self.local_path(raw_url, base_dir)
            if resolved is not None:
                referenced.add(resolved[1])

        self.assertFalse(
            PRESERVED_AND_USED_ASSETS - referenced,
            "Required assets are not all referenced by index.html",
        )
        self.assertTrue(
            RETAINED_BUT_UNUSED_ASSETS.isdisjoint(referenced),
            "Legacy publication thumbnails must stay on disk but must "
            "not be referenced by index.html",
        )

    def test_compact_zhu_brand_lockup_and_favicons(self):
        for relative_path, expected_dimensions in EXPECTED_LOGO_ASSETS.items():
            with self.subTest(asset=relative_path):
                path = ROOT / relative_path
                self.assertTrue(
                    path.is_file(),
                    f"Missing compact Zhu logo asset: {relative_path}",
                )
                width, height, has_transparency = png_info(path)
                self.assertEqual((width, height), expected_dimensions)
                self.assertTrue(
                    has_transparency,
                    "Compact Zhu logo asset needs transparency: "
                    f"{relative_path}",
                )

        brand = self.one(
            self.with_class(self.dom, "brand", tag="a"),
            "a.brand",
        )
        self.assertEqual(
            brand.attr("aria-label"),
            "Hangxiao Zhu — back to top",
        )
        brand_label = self.one(
            self.with_class(brand, "brand-label"),
            ".brand-label inside a.brand",
        )
        self.assertEqual(brand_label.visible_text, "Research Index")

        lockup = self.one(
            self.with_class(brand, "brand-lockup"),
            ".brand-lockup inside a.brand",
        )
        personal_mark = self.one(
            self.with_class(lockup, "brand-mark", tag="img"),
            "img.brand-mark inside .brand-lockup",
        )
        institution_mark = self.one(
            self.with_class(lockup, "brand-institution-mark", tag="img"),
            "img.brand-institution-mark inside .brand-lockup",
        )

        self.assertEqual(personal_mark.attr("src"), "images/zhu-logo-nav.png")
        with self.subTest(contract="retina navigation logo source set"):
            self.assertEqual(
                personal_mark.attr("srcset"),
                "images/zhu-logo-nav.png 1x, images/zhu-logo-nav@2x.png 2x",
            )
        self.assertEqual(personal_mark.attr("width"), "37")
        self.assertEqual(personal_mark.attr("height"), "37")
        self.assertEqual(personal_mark.attr("alt"), "")
        self.assertEqual(institution_mark.attr("src"), "images/tamu.png")
        self.assertEqual(lockup.attr("aria-hidden"), "true")

        icon_links = [
            link
            for link in self.elements(tag="link")
            if "icon" in (link.attr("rel") or "").lower().split()
        ]
        icons = {
            (link.attr("media"), link.attr("sizes")): (
                link.attr("href"),
                link.attr("type"),
            )
            for link in icon_links
        }
        self.assertEqual(
            len(icon_links),
            len(icons),
            "Favicon (media, sizes) pairs must be unique",
        )
        self.assertEqual(
            icons,
            {
                ("(prefers-color-scheme: light)", "16x16"): (
                    "images/favicon-16.png",
                    "image/png",
                ),
                ("(prefers-color-scheme: light)", "32x32"): (
                    "images/favicon-32.png",
                    "image/png",
                ),
                ("(prefers-color-scheme: dark)", "16x16"): (
                    "images/favicon-dark-16.png",
                    "image/png",
                ),
                ("(prefers-color-scheme: dark)", "32x32"): (
                    "images/favicon-dark-32.png",
                    "image/png",
                ),
            },
        )

    def test_portrait_has_a_responsive_derivative_and_original_fallback(self):
        original = ROOT / "images/prof_pic.jpg"
        derivative = ROOT / "images/prof_pic-720.jpg"
        self.assertTrue(original.is_file(), "Original portrait must remain")
        self.assertTrue(
            derivative.is_file(),
            "Missing responsive portrait derivative",
        )

        picture = self.one(
            self.with_class(self.dom, "portrait-frame", tag="picture"),
            "picture.portrait-frame",
        )
        source = self.one(
            [child for child in picture.children if child.tag == "source"],
            "responsive portrait source",
        )
        self.assertEqual(source.attr("srcset"), "images/prof_pic-720.jpg")
        self.assertTrue(
            source.attr("media") or source.attr("sizes"),
            "Responsive portrait source needs a media or sizes contract",
        )

        fallback = self.one(
            [child for child in picture.children if child.tag == "img"],
            "original portrait fallback",
        )
        self.assertEqual(fallback.attr("src"), "images/prof_pic.jpg")
        self.assertEqual(fallback.attr("fetchpriority"), "high")

    def test_every_local_html_and_css_reference_resolves(self):
        for source, raw_url, base_dir in self.all_references():
            with self.subTest(source=source, reference=raw_url):
                resolved = self.local_path(raw_url, base_dir)
                if resolved is not None:
                    self.assertTrue(
                        resolved[0].exists(),
                        f"Broken local reference: {raw_url!r}",
                    )

    def test_heading_hierarchy(self):
        headings = [
            node
            for node in self.elements()
            if re.fullmatch(r"h[1-6]", node.tag)
        ]
        self.assertTrue(headings, "The page needs headings")
        self.assertEqual(
            len([heading for heading in headings if heading.tag == "h1"]),
            1,
        )

        levels = [int(heading.tag[1]) for heading in headings]
        self.assertEqual(levels[0], 1, "The first heading must be h1")
        for previous, current in zip(levels, levels[1:]):
            self.assertLessEqual(
                current,
                previous + 1,
                f"Heading level jumps from h{previous} to h{current}",
            )

        main = self.by_id("main-content")
        top_level_sections = [
            child for child in main.children if child.tag == "section"
        ]
        for section in top_level_sections:
            section_headings = [
                node
                for node in section.descendants()
                if re.fullmatch(r"h[1-6]", node.tag)
            ]
            self.assertTrue(
                section_headings,
                f"#{section.attr('id')} needs a heading",
            )
            self.assertEqual(section_headings[0].tag, "h2")

    def test_images_have_alt_dimensions_and_lazy_loading(self):
        images = self.elements(tag="img")
        self.assertTrue(images, "The page should contain images")

        for image in images:
            source = image.attr("src") or "<missing src>"
            with self.subTest(image=source):
                self.assertIn(
                    "alt",
                    image.attrs,
                    "Every image needs an alt attribute",
                )
                self.assertRegex(
                    image.attr("width") or "",
                    r"^[1-9]\d*$",
                )
                self.assertRegex(
                    image.attr("height") or "",
                    r"^[1-9]\d*$",
                )

                ancestor = image.parent
                inside_hero = False
                while ancestor is not None:
                    if (
                        ancestor.tag == "header"
                        and ancestor.attr("id") == "hero"
                    ):
                        inside_hero = True
                        break
                    ancestor = ancestor.parent

                if not inside_hero:
                    self.assertEqual(
                        (image.attr("loading") or "").lower(),
                        "lazy",
                    )

    def test_contact_links_are_exact_and_have_visible_text(self):
        anchors = self.elements(tag="a")
        parsed_anchors = []
        for anchor in anchors:
            href = anchor.attr("href") or ""
            try:
                parsed_anchors.append((anchor, urlsplit(href)))
            except ValueError as error:
                self.fail(f"Invalid link {href!r}: {error}")

        email = self.one(
            [
                anchor
                for anchor, parsed in parsed_anchors
                if parsed.scheme.lower() == "mailto"
            ],
            "Email link",
        )
        self.assertEqual(email.attr("href"), "mailto:hangxiao@tamu.edu")

        scholar = self.one(
            [
                anchor
                for anchor, parsed in parsed_anchors
                if parsed.netloc.lower() == "scholar.google.com"
                and parsed.path == "/citations"
            ],
            "Google Scholar link",
        )
        scholar_url = urlsplit(scholar.attr("href"))
        self.assertEqual(scholar_url.scheme.lower(), "https")
        self.assertEqual(scholar_url.netloc.lower(), "scholar.google.com")
        self.assertEqual(
            parse_qs(
                scholar_url.query,
                keep_blank_values=True,
            ).get("user"),
            ["fmDa4U4AAAAJ"],
        )

        cv_candidates = []
        for anchor, parsed in parsed_anchors:
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = self.local_path(anchor.attr("href"), ROOT)
            if (
                resolved is not None
                and resolved[1] == "assets/CV_Hangxiao Zhu_2024.pdf"
            ):
                cv_candidates.append(anchor)
        cv = self.one(cv_candidates, "CV link")
        cv_url = urlsplit(cv.attr("href"))
        self.assertFalse(cv_url.query or cv_url.fragment)

        for label, anchor in (
            ("Email", email),
            ("Google Scholar", scholar),
            ("CV", cv),
        ):
            with self.subTest(contact=label):
                self.assertTrue(
                    anchor.visible_text,
                    f"{label} link needs visible text",
                )

    def test_href_schemes_are_safe(self):
        allowed_schemes = {"", "http", "https", "mailto"}
        for node in self.elements():
            if "href" not in node.attrs:
                continue
            href = node.attr("href") or ""
            try:
                parsed = urlsplit(href)
            except ValueError as error:
                self.fail(f"Invalid href {href!r}: {error}")

            with self.subTest(element=node.tag, href=href):
                self.assertIn(parsed.scheme.lower(), allowed_schemes)
                self.assertFalse(
                    parsed.netloc and not parsed.scheme,
                    "Protocol-relative hrefs are not allowed",
                )

    def test_new_tab_external_links_use_safe_rel_values(self):
        for anchor in self.elements(tag="a"):
            href = anchor.attr("href") or ""
            try:
                parsed = urlsplit(href)
            except ValueError as error:
                self.fail(f"Invalid link {href!r}: {error}")

            is_external = (
                parsed.scheme in {"http", "https"} or bool(parsed.netloc)
            )
            opens_new_tab = (
                (anchor.attr("target") or "").lower() == "_blank"
            )
            if is_external and opens_new_tab:
                with self.subTest(href=href):
                    rel = set(
                        (anchor.attr("rel") or "").lower().split()
                    )
                    self.assertTrue(
                        {"noopener", "noreferrer"} <= rel,
                        "target=_blank external links need both "
                        "noopener and noreferrer",
                    )

    def test_description_canonical_and_open_graph_metadata(self):
        metas = self.elements(tag="meta")
        description = self.one(
            [
                meta
                for meta in metas
                if (meta.attr("name") or "").lower() == "description"
            ],
            "meta description",
        ).attr("content")
        self.assertIsNotNone(description)
        description = normalize_text(description)
        self.assertGreaterEqual(len(description), 50)
        self.assertLessEqual(len(description), 170)

        canonical = self.one(
            [
                link
                for link in self.elements(tag="link")
                if "canonical"
                in (link.attr("rel") or "").lower().split()
            ],
            "canonical link",
        ).attr("href")
        self.assertEqual(canonical, CANONICAL_URL)

        title = self.one(self.elements(tag="title"), "title").text

        open_graph = {}
        for property_name in ("og:title", "og:description", "og:url"):
            meta = self.one(
                [
                    candidate
                    for candidate in metas
                    if (candidate.attr("property") or "").lower()
                    == property_name
                ],
                property_name,
            )
            open_graph[property_name] = normalize_text(
                meta.attr("content") or ""
            )

        self.assertEqual(open_graph["og:title"], title)
        self.assertEqual(open_graph["og:description"], description)
        self.assertEqual(open_graph["og:url"], CANONICAL_URL)

    def test_json_ld_person_and_scholarly_articles(self):
        scripts = [
            script
            for script in self.elements(tag="script")
            if (script.attr("type") or "").lower()
            == "application/ld+json"
        ]
        self.assertTrue(scripts, "Expected JSON-LD structured data")

        objects = []
        for script in scripts:
            try:
                payload = json.loads(script.raw_text())
            except json.JSONDecodeError as error:
                self.fail(f"Invalid JSON-LD: {error}")
            objects.extend(walk_json(payload))

        people = [
            node for node in objects if "Person" in json_types(node)
        ]
        self.assertTrue(
            any(
                person.get("name") == "Hangxiao Zhu"
                and person.get("url") == CANONICAL_URL
                for person in people
            ),
            "JSON-LD needs a canonical Hangxiao Zhu Person",
        )

        scholarly_articles = [
            node
            for node in objects
            if "ScholarlyArticle" in json_types(node)
        ]
        self.assertEqual(
            len(scholarly_articles),
            8,
            "JSON-LD must contain exactly the eight non-thesis works as "
            "ScholarlyArticle nodes",
        )
        by_title = {
            normalize_text(
                str(article.get("headline") or article.get("name") or "")
            ): article
            for article in scholarly_articles
        }

        expected_articles = [
            publication
            for publication in EXPECTED_PUBLICATIONS
            if publication[1] != "thesis"
        ]
        for year, _, title, _ in expected_articles:
            with self.subTest(title=title):
                self.assertIn(
                    title,
                    by_title,
                    "Every non-thesis work needs a ScholarlyArticle",
                )
                self.assertTrue(
                    str(by_title[title].get("datePublished", "")).startswith(
                        year
                    ),
                    f"datePublished for {title!r} must start with {year}",
                )

    def test_skip_link_unique_ids_and_internal_fragments(self):
        ids = [
            node.attr("id")
            for node in self.elements()
            if node.attr("id")
        ]
        self.assertEqual(
            len(ids),
            len(set(ids)),
            "Element ids must be unique",
        )

        skip_link = self.one(
            [
                anchor
                for anchor in self.elements(tag="a")
                if "skip-link" in anchor.classes
            ],
            "skip link",
        )
        self.assertEqual(skip_link.attr("href"), "#main-content")

        known_ids = set(ids)
        for anchor in self.elements(tag="a"):
            href = anchor.attr("href") or ""
            try:
                parsed = urlsplit(href)
            except ValueError as error:
                self.fail(f"Invalid link {href!r}: {error}")

            same_document_paths = {
                "",
                ".",
                "./",
                "/",
                "index.html",
                "./index.html",
                "/index.html",
            }
            is_internal_fragment = href.startswith("#") or (
                bool(parsed.fragment)
                and not parsed.scheme
                and not parsed.netloc
                and parsed.path in same_document_paths
            )
            if is_internal_fragment:
                with self.subTest(href=href):
                    self.assertIn(unquote(parsed.fragment), known_ids)

    def test_css_focus_reduced_motion_and_flow_footer(self):
        footer = self.one(self.elements(tag="footer"), "footer")
        self.assertFalse(
            has_forbidden_position(footer.attr("style") or ""),
            "Footer inline styles must not use fixed or absolute position",
        )

        footer_tokens = {
            "footer",
            *(f".{class_name}" for class_name in footer.classes),
        }
        if footer.attr("id"):
            footer_tokens.add(f"#{footer.attr('id')}")

        focus_evidence = []
        motion_evidence = []
        motion_override = re.compile(
            r"(?<![\w-])(?:"
            r"scroll-behavior\s*:\s*auto\b|"
            r"animation(?:-duration)?\s*:\s*"
            r"(?:none\b|0(?:\.0+)?(?:m?s)?\b|0?\.0+1m?s\b)|"
            r"transition(?:-duration)?\s*:\s*"
            r"(?:none\b|0(?:\.0+)?(?:m?s)?\b|0?\.0+1m?s\b)"
            r")",
            re.IGNORECASE,
        )

        for source, raw_css, _ in list(self.stylesheet_sources()):
            css = strip_css_comments(raw_css)
            for prelude, body in css_blocks(css):
                if (
                    is_reduced_motion_media(prelude)
                    and motion_override.search(body)
                ):
                    motion_evidence.append(source)

                if prelude.lstrip().startswith("@"):
                    continue

                for selector in split_top_level_commas(prelude):
                    if (
                        has_positive_focus_visible(selector)
                        and has_visible_focus_declaration(body)
                    ):
                        focus_evidence.append((source, selector))

                    rightmost = without_not_pseudo_classes(
                        rightmost_selector_compound(selector)
                    )
                    if "::" in rightmost or re.search(
                        r":(?:before|after)\b",
                        rightmost,
                        re.IGNORECASE,
                    ):
                        continue

                    targets_footer = any(
                        re.search(
                            rf"(?<![\w-]){re.escape(token)}(?![\w-])",
                            rightmost,
                        )
                        for token in footer_tokens
                    )
                    if targets_footer:
                        with self.subTest(
                            source=source,
                            selector=selector,
                        ):
                            self.assertFalse(
                                has_forbidden_position(body),
                                "Footer must not use fixed or absolute "
                                "position",
                            )

        self.assertTrue(
            focus_evidence,
            "CSS needs a positive :focus-visible rule with a visible "
            "outline or shadow",
        )
        self.assertTrue(
            motion_evidence,
            "CSS needs a prefers-reduced-motion: reduce query with an "
            "effective override",
        )

    def test_hero_focus_visible_uses_warm_white_outline(self):
        hero_focus_bodies = []
        for prelude, body in css_blocks(strip_css_comments(self.css)):
            if prelude.lstrip().startswith("@"):
                continue
            for selector in split_top_level_commas(prelude):
                if re.fullmatch(
                    r"\.hero\s+:focus-visible",
                    selector.strip(),
                    re.IGNORECASE,
                ):
                    hero_focus_bodies.append(body)

        self.assertTrue(
            hero_focus_bodies,
            "Hero needs a focus-visible override for all descendants",
        )
        self.assertTrue(
            any(
                re.search(
                    r"(?:^|;)\s*outline-color\s*:\s*"
                    r"var\(\s*--color-hero-text\s*\)",
                    body,
                    re.IGNORECASE,
                )
                for body in hero_focus_bodies
            ),
            "Hero focus outline must use the warm-white hero text color",
        )

    def test_narrow_navigation_uses_valid_column_spacing(self):
        css = strip_css_comments(self.css)
        self.assertNotRegex(
            css,
            r"(?<![\w-])gap-inline\s*:",
            "gap-inline is not a valid CSS property",
        )

        narrow_navigation_bodies = []
        for prelude, body in css_blocks(css):
            if not re.fullmatch(
                r"@media\s*\(\s*max-width\s*:\s*22rem\s*\)",
                prelude.strip(),
                re.IGNORECASE,
            ):
                continue
            for selector_prelude, selector_body in css_blocks(body):
                if ".primary-nav" in split_top_level_commas(
                    selector_prelude
                ):
                    narrow_navigation_bodies.append(selector_body)

        self.assertTrue(
            any(
                re.search(
                    r"(?:^|;)\s*column-gap\s*:\s*\.65rem\b",
                    body,
                    re.IGNORECASE,
                )
                for body in narrow_navigation_bodies
            ),
            "The narrow primary navigation needs a .65rem column gap",
        )

    def test_stylesheets_do_not_use_import(self):
        for source, css, _ in self.stylesheet_sources():
            with self.subTest(source=source):
                self.assertFalse(
                    has_css_import(css),
                    "CSS @import is not allowed",
                )

    def test_no_external_script_or_stylesheet_dependencies(self):
        for script in self.elements(tag="script"):
            source = script.attr("src")
            if source:
                try:
                    parsed = urlsplit(source)
                except ValueError as error:
                    self.fail(f"Invalid script URL {source!r}: {error}")
                self.assertFalse(
                    parsed.scheme or parsed.netloc,
                    f"External script dependency: {source}",
                )

        for link in self.elements(tag="link"):
            rel = set((link.attr("rel") or "").lower().split())
            if "stylesheet" in rel:
                href = link.attr("href") or ""
                try:
                    parsed = urlsplit(href)
                except ValueError as error:
                    self.fail(f"Invalid stylesheet URL {href!r}: {error}")
                self.assertFalse(
                    parsed.scheme or parsed.netloc,
                    f"External stylesheet dependency: {href}",
                )


class HarnessGuardTests(unittest.TestCase):
    def parse(self, markup):
        parser = DOMParser()
        parser.feed(markup)
        parser.close()
        return parser

    def png_chunk(self, chunk_type, payload, bad_crc=False):
        checksum = binascii.crc32(chunk_type + payload) & 0xFFFFFFFF
        if bad_crc:
            checksum ^= 1
        return (
            struct.pack(">I", len(payload))
            + chunk_type
            + payload
            + struct.pack(">I", checksum)
        )

    def png_fixture(
        self,
        scanlines,
        *,
        width=1,
        height=1,
        color_type=6,
        palette=None,
        transparency=None,
        include_idat=True,
        bad_idat_crc=False,
    ):
        ihdr = struct.pack(
            ">IIBBBBB",
            width,
            height,
            8,
            color_type,
            0,
            0,
            0,
        )
        chunks = [self.png_chunk(b"IHDR", ihdr)]
        if palette is not None:
            chunks.append(self.png_chunk(b"PLTE", palette))
        if transparency is not None:
            chunks.append(self.png_chunk(b"tRNS", transparency))
        if include_idat:
            chunks.append(
                self.png_chunk(
                    b"IDAT",
                    zlib.compress(scanlines),
                    bad_crc=bad_idat_crc,
                )
            )
        chunks.append(self.png_chunk(b"IEND", b""))
        return b"\x89PNG\r\n\x1a\n" + b"".join(chunks)

    def write_png(self, directory, name, payload):
        path = Path(directory) / name
        path.write_bytes(payload)
        return path

    def test_png_info_checks_pixels_not_just_alpha_channel(self):
        with tempfile.TemporaryDirectory() as directory:
            opaque = self.write_png(
                directory,
                "opaque-rgba.png",
                self.png_fixture(b"\x00\x10\x20\x30\xff"),
            )
            transparent = self.write_png(
                directory,
                "transparent-rgba.png",
                self.png_fixture(b"\x00\x10\x20\x30\x80"),
            )

            self.assertEqual(png_info(opaque), (1, 1, False))
            self.assertEqual(png_info(transparent), (1, 1, True))

    def test_png_info_rejects_missing_idat_and_bad_crc(self):
        with tempfile.TemporaryDirectory() as directory:
            fixtures = {
                "missing-idat.png": self.png_fixture(
                    b"",
                    include_idat=False,
                ),
                "bad-crc.png": self.png_fixture(
                    b"\x00\x10\x20\x30\x80",
                    bad_idat_crc=True,
                ),
            }

            for name, payload in fixtures.items():
                with self.subTest(fixture=name):
                    path = self.write_png(directory, name, payload)
                    with self.assertRaisesRegex(
                        AssertionError,
                        re.escape(str(path)),
                    ):
                        png_info(path)

    def test_png_info_handles_required_transparency_encodings(self):
        palette = b"\x10\x20\x30\x40\x50\x60"
        cases = {
            "grayscale-alpha-transparent.png": (
                self.png_fixture(
                    b"\x00\x20\x80",
                    color_type=4,
                ),
                True,
            ),
            "grayscale-alpha-opaque.png": (
                self.png_fixture(
                    b"\x00\x20\xff",
                    color_type=4,
                ),
                False,
            ),
            "indexed-transparent.png": (
                self.png_fixture(
                    b"\x00\x00",
                    color_type=3,
                    palette=palette,
                    transparency=b"\x00\xff",
                ),
                True,
            ),
            "indexed-opaque.png": (
                self.png_fixture(
                    b"\x00\x01",
                    color_type=3,
                    palette=palette,
                    transparency=b"\x00\xff",
                ),
                False,
            ),
            "truecolor-transparent.png": (
                self.png_fixture(
                    b"\x00\x10\x20\x30",
                    color_type=2,
                    transparency=struct.pack(">HHH", 0x10, 0x20, 0x30),
                ),
                True,
            ),
            "truecolor-opaque.png": (
                self.png_fixture(
                    b"\x00\x10\x20\x30",
                    color_type=2,
                    transparency=struct.pack(">HHH", 0x10, 0x20, 0x31),
                ),
                False,
            ),
            "grayscale-transparent.png": (
                self.png_fixture(
                    b"\x00\x20",
                    color_type=0,
                    transparency=struct.pack(">H", 0x20),
                ),
                True,
            ),
            "grayscale-opaque.png": (
                self.png_fixture(
                    b"\x00\x20",
                    color_type=0,
                    transparency=struct.pack(">H", 0x21),
                ),
                False,
            ),
        }

        with tempfile.TemporaryDirectory() as directory:
            for name, (payload, expected) in cases.items():
                with self.subTest(fixture=name):
                    path = self.write_png(directory, name, payload)
                    self.assertEqual(png_info(path), (1, 1, expected))

    def test_png_info_rejects_palette_after_transparency(self):
        ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
        payload = b"\x89PNG\r\n\x1a\n" + b"".join(
            [
                self.png_chunk(b"IHDR", ihdr),
                self.png_chunk(
                    b"tRNS",
                    struct.pack(">HHH", 0x10, 0x20, 0x30),
                ),
                self.png_chunk(b"PLTE", b"\x10\x20\x30"),
                self.png_chunk(
                    b"IDAT",
                    zlib.compress(b"\x00\x10\x20\x30"),
                ),
                self.png_chunk(b"IEND", b""),
            ]
        )

        with tempfile.TemporaryDirectory() as directory:
            path = self.write_png(directory, "bad-order.png", payload)
            with self.assertRaisesRegex(
                AssertionError,
                re.escape(str(path)),
            ):
                png_info(path)

    def test_png_info_reconstructs_all_standard_filters(self):
        previous = b"\x0a\xff\x14\xff"
        current = b"\x0f\xff\x19\xff"
        cases = {
            "none.png": b"\x00" + current,
            "sub.png": b"\x01\x0f\xff\x0a\x00",
            "up.png": b"\x00" + previous + b"\x02\x05\x00\x05\x00",
            "average.png": (
                b"\x00" + previous + b"\x03\x0a\x80\x08\x00"
            ),
            "paeth.png": b"\x00" + previous + b"\x04\x05\x00\x05\x00",
        }

        with tempfile.TemporaryDirectory() as directory:
            for name, scanlines in cases.items():
                with self.subTest(fixture=name):
                    height = 1 if name in {"none.png", "sub.png"} else 2
                    path = self.write_png(
                        directory,
                        name,
                        self.png_fixture(
                            scanlines,
                            width=2,
                            height=height,
                            color_type=4,
                        ),
                    )
                    self.assertEqual(png_info(path), (2, height, False))

    def test_parser_records_case_insensitive_duplicate_attributes(self):
        parser = self.parse(
            '<div DATA-X="first" data-x="second"></div>'
            '<input HREF="first" href="second" />'
        )
        self.assertEqual(
            [name for _, name in parser.duplicate_attributes],
            ["data-x", "href"],
        )
        elements = list(parser.document.descendants())
        self.assertEqual(elements[0].attr("data-x"), "first")
        self.assertEqual(elements[1].attr("href"), "first")

    def test_base_fixture_is_detected(self):
        parser = self.parse(
            '<base href="https://evil.example/" target="_blank">'
        )
        self.assertEqual(
            [
                element.tag
                for element in parser.document.descendants()
                if element.tag == "base"
            ],
            ["base"],
        )

    def test_css_import_detector_ignores_comments_and_case(self):
        self.assertFalse(has_css_import("/* @import 'ignored.css'; */"))
        self.assertFalse(has_css_import(".x::before{content:'@import'}"))
        self.assertTrue(has_css_import('@ImPoRt "blocked.css";'))


if __name__ == "__main__":
    unittest.main()
