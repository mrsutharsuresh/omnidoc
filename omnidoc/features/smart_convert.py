import re
from typing import Tuple, List, Optional

# Smart feature handlers always accept and return markdown text

def convert_ascii_tables_to_markdown(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # detect a space/pipe separated header row
        if re.search(r"\S\s{2,}\S", line):
            # collect block until blank line
            block = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].startswith('#'):
                block.append(lines[j])
                j += 1
            # turn into markdown table by splitting on 2+ spaces
            cols = [c.strip() for c in re.split(r"\s{2,}", block[0].strip())]
            if len(cols) > 1:
                out.append("| " + " | ".join(cols) + " |")
                out.append("| " + " | ".join(['---'] * len(cols)) + " |")
                for row in block[1:]:
                    cells = [c.strip() for c in re.split(r"\s{2,}", row.strip())]
                    out.append("| " + " | ".join(cells) + " |")
                i = j
                continue
        out.append(line)
        i += 1
    return "\n".join(out)

SIP_METHODS = {"INVITE","ACK","BYE","CANCEL","REGISTER","OPTIONS","PRACK","SUBSCRIBE","NOTIFY","PUBLISH","INFO","REFER","MESSAGE","UPDATE"}

RESP_CODE_RE = re.compile(r"^(1|2|3|4|5|6)\d\d\b")


def _looks_like_program_code(text: str) -> bool:
    # Heuristic to avoid converting C/CPP/Java snippets, etc.
    code_tokens = [";", "=", "++", "--", "{", "}", "return ", "for ", "while ", "if ("]
    score = sum(text.count(tok) for tok in code_tokens)
    return score >= 3


def _heading_before(md: str, start_idx: int) -> str:
    # Find nearest preceding Markdown heading within ~10 lines
    up_to = md[:start_idx]
    lines = up_to.splitlines()
    for line in reversed(lines[-12:]):
        if line.strip().startswith('#'):
            return line.strip().lower()
    return ""


def _has_sip_context(heading: str) -> bool:
    if not heading:
        return False
    keywords = ["sip", "signaling", "signal", "sequence", "call flow", "message flow", "flow"]
    return any(k in heading for k in keywords)


def _block_has_sip_markers(text: str) -> bool:
    arrows = text.count("->") + text.count("=>")
    has_method = any(m in text for m in SIP_METHODS)
    has_code = bool(RESP_CODE_RE.search(text))
    return arrows >= 2 and (has_method or has_code)


def _has_marker(md: str, start_idx: int, key: str) -> bool:
    window = md[max(0, start_idx-400):start_idx]
    return f"<!-- dv:block={key} -->" in window


def convert_sip_signaling_to_mermaid(md: str) -> str:
    """Convert fenced code blocks that look like SIP signaling into Mermaid sequence diagrams.
    Only converts when:
      - The nearest preceding heading suggests signaling/flow context, AND
      - The block contains SIP methods or response codes and at least 2 arrows, AND
      - The block does not look like programming code, AND
      - The block is not explicitly a programming language (c, cpp, java, go, rust, js, ts, py)
    """
    code_fence_re = re.compile(r"```(?P<lang>[^\n]*)\n(?P<body>.*?)\n```", re.DOTALL)
    out = []
    last = 0

    for m in code_fence_re.finditer(md):
        out.append(md[last:m.start()])
        lang = (m.group('lang') or '').strip().lower()
        body = m.group('body')

        # Skip obvious programming languages
        skip_langs = {"c", "cpp", "c++", "java", "go", "rust", "js", "ts", "javascript", "typescript", "python", "py", "json", "xml"}
        if lang in skip_langs:
            out.append(m.group(0))
            last = m.end()
            continue

        heading = _heading_before(md, m.start())
        # Skip conversion if explicitly marked as code-only
        if _has_marker(md, m.start(), 'code-only'):
            out.append(m.group(0))
            last = m.end()
            continue

        # If we have a candidate-sip marker, we can relax heading requirement
        has_candidate_marker = _has_marker(md, m.start(), 'candidate-sip')
        if not has_candidate_marker and not _has_sip_context(heading):
            out.append(m.group(0))
            last = m.end()
            continue

        if _looks_like_program_code(body) or not _block_has_sip_markers(body):
            out.append(m.group(0))
            last = m.end()
            continue

        lines = [l for l in body.splitlines() if l.strip()]
        # require at least one message with a SIP method/response
        has_sip_message = any(any(mn in l for mn in SIP_METHODS) or RESP_CODE_RE.search(l) for l in lines)
        if not has_sip_message:
            out.append(m.group(0))
            last = m.end()
            continue

        mer = ["```mermaid", "sequenceDiagram"]
        participants: List[str] = []
        edge_re = re.compile(r"^\s*([A-Za-z0-9_.-]{2,})\s*(?:->|=>)\s*([A-Za-z0-9_.-]{2,})\s*:?\s*(.*)")

        for l in lines:
            mm = edge_re.findall(l)
            if mm:
                a, b, _msg = mm[0]
                if a not in participants:
                    participants.append(a)
                if b not in participants:
                    participants.append(b)

        # sanity: participants count reasonable
        if not (2 <= len(participants) <= 8):
            out.append(m.group(0))
            last = m.end()
            continue

        for p in participants:
            mer.append(f"participant {p}")

        for l in lines:
            mm = edge_re.findall(l)
            if mm:
                a, b, msg = mm[0]
                mer.append(f"{a}->>{b}: {msg}")
        mer.append("```")
        out.append("\n".join(mer))
        last = m.end()

    out.append(md[last:])
    return "".join(out)


def detect_network_topology(md: str) -> bool:
    return any(ch in md for ch in ["+---","|","---+"]) and "->" not in md


def convert_topology_to_mermaid(md: str) -> str:
    if not detect_network_topology(md):
        return md
    # placeholder: wrap in flowchart graph TB
    lines = [l for l in md.splitlines() if l.strip()]
    mer = ["```mermaid","flowchart LR"]
    # naive: list unique words as nodes
    nodes = set()
    for l in lines:
        for w in re.findall(r"[A-Za-z0-9_]{3,}", l):
            nodes.add(w)
    nodes = list(nodes)[:8]
    for n in nodes:
        mer.append(f"    {n}[{n}]")
    mer.append("```")
    return "\n".join(mer)
