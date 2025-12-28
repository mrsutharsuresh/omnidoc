import re
from typing import List, Tuple


def _slugify(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip('-')
    return s


def _is_title_case(text: str) -> bool:
    words = [w for w in re.split(r"\s+", text) if w]
    if not words or len(words) > 15:
        return False
    cap = sum(1 for w in words if w[0].isalpha() and w[0].isupper())
    return cap / max(1, len(words)) >= 0.6


def _is_all_caps(text: str) -> bool:
    letters = re.findall(r"[A-Za-z]", text)
    if not letters:
        return False
    return all(ch.isupper() for ch in letters)


def _numeric_heading_level(text: str) -> int:
    m = re.match(r"^\s*(\d+(?:\.\d+)*|[IVXLCDM]+|[A-Z])(?:[\.)])?\s+", text)
    if not m:
        return 0
    part = m.group(1)
    if re.match(r"^\d+(?:\.\d+)*$", part):
        return part.count('.') + 1
    return 1


def normalize_headings(md: str) -> str:
    lines = md.splitlines()
    n = len(lines)
    in_code = False
    used_slugs = {}

    def uniq_slug(text: str) -> str:
        base = _slugify(text) or "section"
        count = used_slugs.get(base, 0) + 1
        used_slugs[base] = count
        return base if count == 1 else f"{base}-{count}"

    # collect existing heading slugs
    for line in lines:
        if re.match(r"^```", line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)(?:\s*\{#([A-Za-z0-9_-]+)\})?\s*$", line)
        if m:
            text = m.group(2).strip()
            slug = m.group(3) or _slugify(text)
            used_slugs[slug] = max(used_slugs.get(slug, 0), 1)

    in_code = False
    out: List[str] = []
    i = 0
    while i < n:
        line = lines[i]
        if re.match(r"^```", line):
            in_code = not in_code
            out.append(line)
            i += 1
            continue
        if in_code:
            out.append(line)
            i += 1
            continue

        m_atx = re.match(r"^(#{1,6})\s+(.*?)(\s*\{#([A-Za-z0-9_-]+)\})?\s*$", line)
        if m_atx:
            level = len(m_atx.group(1))
            text = m_atx.group(2).strip()
            if m_atx.group(4):
                out.append(line)
            else:
                slug = uniq_slug(text)
                out.append(f"{'#' * level} {text} {{#{slug}}}")
            i += 1
            continue

        if i + 1 < n and re.match(r"^[=]{3,}\s*$", lines[i + 1]):
            text = line.strip()
            # Skip if text is empty (avoid blank headings)
            if text:
                slug = uniq_slug(text)
                out.append(f"# {text} {{#{slug}}}")
                i += 2
                continue
        # Skip setext-style --- if it looks like a horizontal rule (blank line above or below)
        if i + 1 < n and re.match(r"^-{3,}\s*$", lines[i + 1]):
            text = line.strip()
            # Only treat as heading if:
            # 1. Text is not empty
            # 2. Not preceded by blank line (which makes --- a horizontal rule)
            # 3. Has actual content that looks like a heading
            prev_line_blank = (i == 0) or (lines[i - 1].strip() == "")
            if text and not prev_line_blank and len(text) <= 100:
                slug = uniq_slug(text)
                out.append(f"## {text} {{#{slug}}}")
                i += 2
                continue

        prev_blank = (i == 0) or (lines[i - 1].strip() == "")
        next_blank = (i + 1 >= n) or (lines[i + 1].strip() == "")
        is_list_like = bool(re.match(r"^\s*([*\-+]\s+|\d+[\.)]\s+)", line))
        is_table_like = '|' in line and re.match(r"^\s*\|", line)
        is_quote = line.strip().startswith('>')
        is_rule = re.match(r"^\s*([-*_])\1{2,}\s*$", line) is not None
        is_link_like = ('http://' in line or 'https://' in line or re.search(r"\[[^\]]+\]\([^\)]+\)", line))
        short_enough = len(line.strip()) <= 80
        no_terminal_period = not line.strip().endswith('.')

        title_like = (_is_title_case(line.strip()) or _is_all_caps(line.strip()))
        num_level = _numeric_heading_level(line)

        STOPWORDS = {"the","a","an","and","or","but","if","then","than","because","as","of","at","by","for","with","about","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under"}
        AUX_VERBS = {"is","are","was","were","be","being","been","have","has","had","do","does","did","will","shall","can","should","may","might","must"}
        words = [w.lower() for w in re.findall(r"[A-Za-z']+", line)]
        stop_ratio = (sum(1 for w in words if w in STOPWORDS) / max(1, len(words))) if words else 0.0
        has_aux = any(w in AUX_VERBS for w in words)

        if prev_blank and next_blank and not is_list_like and not is_table_like and not is_quote and not is_rule and not is_link_like and short_enough and no_terminal_period and (title_like or num_level > 0) and stop_ratio <= 0.5 and not has_aux:
            level = 2
            if num_level > 0:
                level = min(6, 1 + num_level)
            text = re.sub(r"^\s*(\d+(?:\.\d+)*|[IVXLCDM]+|[A-Z])(?:[\.)])?\s+", "", line).strip()
            slug = uniq_slug(text)
            out.append(f"{'#' * level} {text} {{#{slug}}}")
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def sanitize_attr_tokens(md: str) -> str:
    lines = md.splitlines()
    out: List[str] = []
    in_code = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^```", line):
            in_code = not in_code
            out.append(line)
            i += 1
            continue
        if in_code:
            out.append(line)
            i += 1
            continue
        # Keep proper heading lines with attr IDs intact - these will be processed by attr_list extension
        if re.match(r"^(#{1,6})\s+.*\{#[A-Za-z0-9_-]+\}\s*$", line):
            # Ensure proper format for attr_list extension: must have space before {#
            cleaned_heading = re.sub(r"\s*\{#([A-Za-z0-9_-]+)\}\s*$", r" {#\1}", line)
            out.append(cleaned_heading.rstrip())
            i += 1
            continue
        # Preserve setext headings by passing both lines as-is
        if i + 1 < len(lines) and re.match(r"^[=-]{3,}\s*$", lines[i + 1]):
            out.append(line)
            i += 1
            out.append(lines[i])
            i += 1
            continue
        # Strip attr-like tokens globally in non-heading content (tables, paragraphs)
        # Matches {#slug} or {slug} composed of alnum, dash, underscore
        cleaned = re.sub(r"\s*\{#?[A-Za-z0-9_-]+\}", "", line)
        out.append(cleaned)
        i += 1
    return "\n".join(out)


def build_toc(md: str) -> str:
    lines = md.splitlines()
    headings: List[Tuple[int, str, int]] = []
    first_h1_idx = None
    first_heading_idx = None
    in_code = False

    for idx, line in enumerate(lines):
        # Track code blocks to skip headings inside them
        if re.match(r"^```", line):
            in_code = not in_code
            continue
        if in_code:
            continue
            
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append((level, text, idx))
            if level == 1 and first_h1_idx is None:
                first_h1_idx = idx
            if first_heading_idx is None:
                first_heading_idx = idx

    if not headings:
        return md

    # Ensure explicit IDs
    for level, text, idx in headings:
        if re.search(r"\{#([A-Za-z0-9_-]+)\}\s*$", lines[idx]):
            continue
        anchor = _slugify(text)
        lines[idx] = f"{'#' * level} {text} {{#{anchor}}}"

    # Build hierarchical structure using actual heading levels
    # This creates a proper tree structure regardless of whether document uses H1+H2 or H2 as main sections
    def build_hierarchy_tree(headings_data):
        """Build a tree structure from flat heading list based on levels."""
        if not headings_data:
            return []
        
        # Convert headings to node format
        nodes = []
        for level, text, idx in headings_data:
            display_text = re.sub(r"\s*\{#[^}]+\}\s*$", "", text).strip()
            if not display_text:  # Skip blank headings
                continue
            # Strip numeric/lettered prefixes from heading text (e.g., "1.", "2.1", "A.", "I.")
            # since the algorithm assigns its own section numbers
            display_text = re.sub(r"^\s*(?:\d+\.)+\s*|\s*^[IVXLCDMivxlcdm]+\.\s*|^\s*[A-Z]\.\s*", "", display_text).strip()
            # Strip markdown formatting from TOC text (bold, italic, code, etc.)
            # Remove **bold**, __bold__, *italic*, _italic_
            display_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", display_text)  # **bold**
            display_text = re.sub(r"__([^_]+)__", r"\1", display_text)      # __bold__
            display_text = re.sub(r"\*([^*]+)\*", r"\1", display_text)      # *italic*
            display_text = re.sub(r"_([^_]+)_", r"\1", display_text)        # _italic_
            display_text = re.sub(r"`([^`]+)`", r"\1", display_text)        # `code`
            display_text = re.sub(r"~~([^~]+)~~", r"\1", display_text)      # ~~strikethrough~~
            display_text = display_text.strip()
            m_id = re.search(r"\{#([A-Za-z0-9_-]+)\}\s*$", lines[idx])
            anchor = m_id.group(1) if m_id else _slugify(display_text)
            nodes.append({
                'level': level,
                'text': display_text,
                'anchor': anchor,
                'children': [],
                'number': ''  # Will be assigned during tree traversal
            })
        
        if not nodes:
            return []
        
        # Build tree structure
        root_level = min(node['level'] for node in nodes)
        tree = []
        stack = []  # Stack of (node, level) to track hierarchy
        
        for node in nodes:
            # Pop stack until we find the parent level
            while stack and stack[-1]['level'] >= node['level']:
                stack.pop()
            
            if not stack:
                # Top-level node
                tree.append(node)
                stack.append(node)
            else:
                # Add as child to parent
                parent = stack[-1]
                parent['children'].append(node)
                stack.append(node)
        
        return tree
    
    # Build tree and assign numbers
    def assign_numbers(tree, parent_number='', counters=None):
        """Recursively assign section numbers to tree nodes."""
        if counters is None:
            counters = {}
        
        for node in tree:
            level = node['level']
            
            # Initialize counter for this level if needed
            if level not in counters:
                counters[level] = 0
            
            # Reset counters for deeper levels
            deeper_levels = [l for l in counters.keys() if l > level]
            for l in deeper_levels:
                counters[l] = 0
            
            # Increment counter for current level
            counters[level] += 1
            
            # Assign number
            if parent_number:
                node['number'] = f"{parent_number}.{counters[level]}"
            else:
                node['number'] = str(counters[level])
            
            # Recurse into children
            if node['children']:
                assign_numbers(node['children'], node['number'], counters)
    
    # Build tree and flatten for TOC rendering
    tree = build_hierarchy_tree(headings)
    assign_numbers(tree)
    
    # Flatten tree to list for TOC rendering
    def flatten_tree(tree):
        """Convert tree structure back to flat list with all nodes."""
        result = []
        for node in tree:
            result.append(node)
        return result
    
    sections = flatten_tree(tree)

    # Build properly nested HTML structure from tree
    def build_nested_toc_items(nodes, depth=0):
        """Recursively build nested TOC HTML from tree structure."""
        if not nodes:
            return []
        
        result = []
        result.append(f'<ol class="toc-ol toc-depth-{depth}">')
        
        for node in nodes:
            has_children = len(node['children']) > 0
            toggle = '<button class="toc-toggle" aria-expanded="true" title="Collapse section"></button>' if has_children else ''
            
            # Determine item class based on depth
            item_class = f"toc-item toc-l{node['level']}" if depth > 0 else "toc-item toc-section"
            if has_children:
                item_class += " toc-collapsible"
            
            result.append(
                f'<li class="{item_class}"><span class="toc-num">{node["number"]}</span>'
                f'<span class="toc-main">{toggle}<a href="#{node["anchor"]}" class="toc-link">{node["text"]}</a></span>'
            )
            
            if has_children:
                # Recursively build children
                result.extend(build_nested_toc_items(node['children'], depth + 1))
            
            result.append('</li>')
        
        result.append('</ol>')
        return result
    
    rows = []
    rows.append('<div class="generated-toc" role="navigation" aria-label="Table of contents">')
    rows.append('<div class="toc-title">Contents</div>')
    rows.append('<div class="toc-list">')
    
    # Build nested structure from tree
    rows.extend(build_nested_toc_items(tree, depth=0))
    
    rows.append('</div>')
    rows.append('</div>')
    toc_html = "\n".join(rows)

    # Determine where to insert TOC:
    # Priority 1: After first H1 if it's in the first 50 lines (typical document structure)
    # Priority 2: At the very top if first H1 is far down (conversational/log documents)
    # Priority 3: At the very top if no H1 exists
    insert_at = 0
    if first_h1_idx is not None and first_h1_idx < 50:
        # Insert after first H1 if it's near the top
        insert_at = first_h1_idx + 1
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
    # else: insert_at remains 0 (top of document)

    # Use a placeholder that markdown won't process
    # The placeholder will be replaced with actual HTML after markdown rendering
    toc_placeholder = f"<!--TOC_PLACEHOLDER_START-->{toc_html}<!--TOC_PLACEHOLDER_END-->"
    
    new_lines = lines[:insert_at] + [toc_placeholder, ""] + lines[insert_at:]
    return "\n".join(new_lines)


def annotate_blocks(md: str) -> str:
    def looks_like_program_code(text: str) -> bool:
        tokens = [";", "=", "++", "--", "{", "}", "return ", "for ", "while ", "if ("]
        return sum(text.count(t) for t in tokens) >= 3

    def has_topology(text: str) -> bool:
        return ("+---" in text or any(ch in text for ch in ["┌","─","┐","│","└","┘"])) and "->" not in text

    def has_sip(text: str) -> bool:
        sip_methods = {"INVITE","ACK","BYE","CANCEL","REGISTER","OPTIONS","PRACK","SUBSCRIBE","NOTIFY","PUBLISH","INFO","REFER","MESSAGE","UPDATE"}
        has_method = any(m in text for m in sip_methods)
        has_code = re.search(r"^(1|2|3|4|5|6)\d\d\b", text, flags=re.MULTILINE) is not None
        arrows = text.count("->") + text.count("=>")
        return arrows >= 2 and (has_method or has_code)

    def has_flowchart(text: str) -> bool:
        arrows = re.findall(r"\b[A-Za-z0-9_.-]{2,}\s*->\s*[A-Za-z0-9_.-]{2,}\b", text)
        return len(arrows) >= 2

    fence = re.compile(r"```(?P<lang>[^\n]*)\n(?P<body>.*?)\n```", re.DOTALL)
    out = []
    last = 0
    for m in fence.finditer(md):
        out.append(md[last:m.start()])
        body = m.group('body')

        marker = None
        if looks_like_program_code(body):
            marker = "code-only"
        elif has_sip(body):
            marker = "candidate-sip"
        elif has_topology(body):
            marker = "candidate-topology"
        elif has_flowchart(body):
            marker = "candidate-flowchart"
        else:
            marker = "code-block"

        out.append(f"<!-- dv:block={marker} -->\n")
        out.append(m.group(0))
        last = m.end()

    out.append(md[last:])
    return "".join(out)
