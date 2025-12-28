from typing import List, Callable
import markdown
import re

# Baseline/standard rendering: just Markdown -> HTML with extensions

def render_baseline(md_text: str) -> str:
    # Extract TOC HTML from placeholder comments before markdown processing
    toc_html = ""
    toc_match = re.search(r'<!--TOC_PLACEHOLDER_START-->(.*?)<!--TOC_PLACEHOLDER_END-->', md_text, re.DOTALL)
    if toc_match:
        toc_html = toc_match.group(1)
        # Remove the placeholder from markdown text
        md_text = re.sub(r'<!--TOC_PLACEHOLDER_START-->.*?<!--TOC_PLACEHOLDER_END-->', '<!--TOC_INSERTION_POINT-->', md_text, flags=re.DOTALL)
    
    # Render markdown to HTML
    html_output = markdown.markdown(
        md_text,
        extensions=[
            'fenced_code',
            'tables',
            'nl2br',
            'sane_lists',
            'codehilite',
            'toc',
            'extra',
            'attr_list',
            'def_list',
            'abbr',
            'footnotes',
            'md_in_html',
            'admonition',
            'pymdownx.arithmatex',
            'pymdownx.betterem',
            'pymdownx.caret',
            'pymdownx.mark',
            'pymdownx.tilde',
            'pymdownx.details',
            'pymdownx.highlight',
            'pymdownx.inlinehilite',
            'pymdownx.keys',
            'pymdownx.smartsymbols',
            'pymdownx.snippets',
            'pymdownx.superfences',
            'pymdownx.tabbed',
            'pymdownx.tasklist',
            'pymdownx.magiclink',
        ]
    )
    
    # Replace the insertion point with actual TOC HTML
    if toc_html:
        html_output = html_output.replace('<!--TOC_INSERTION_POINT-->', toc_html)
    
    return html_output


def run_pipeline(md_text: str, steps: List[Callable[[str], str]]) -> str:
    out = md_text
    for fn in steps:
        out = fn(out)
    return out
