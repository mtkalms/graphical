CODE_FORMAT = """
<svg class="rich-terminal" viewBox="0 0 {terminal_width} {terminal_height}" xmlns="http://www.w3.org/2000/svg">
    <!-- Generated with Rich https://www.textualize.io -->
    <style>
        .{unique_id}-matrix {{
            font-family: Cascadia Code, monospace;
            font-size: {char_height}px;
            line-height: {line_height}px;
            font-variant-east-asian: full-width;
        }}
        .{unique_id}-title {{
            font-size: 18px;
            font-family: arial;
        }}
        {styles}
    </style>
    <defs>
        <clipPath id="{unique_id}-clip-terminal">
            <rect x="0" y="0" width="{terminal_width}" height="{terminal_height}" />
        </clipPath>
        {lines}
    </defs>
    <g clip-path="url(#{unique_id}-clip-terminal)">
    {backgrounds}
    <g class="{unique_id}-matrix">
    {matrix}
    </g>
    </g>
</svg>
"""

GLYPHS_CODE = """
from rich.text import Text

output = Text.from_markup('\\n'.join({lines}))
"""


def rich(source, language, css_class, options, md, attrs, **kwargs) -> str:
    """A superfences formatter to insert an SVG screenshot."""

    import io

    from rich.console import Console
    from rich.terminal_theme import TerminalTheme

    THEME = TerminalTheme(
        (0, 0, 0),
        (166, 166, 166),
        [
            (0, 0, 0),
            (217, 4, 41),
            (58, 217, 0),
            (255, 231, 0),
            (105, 67, 255),
            (255, 43, 112),
            (0, 197, 199),
            (199, 199, 199),
        ],
        [
            (128, 128, 128),
            (255, 0, 0),
            (0, 255, 0),
            (255, 255, 0),
            (0, 0, 255),
            (255, 0, 255),
            (0, 255, 255),
            (199, 199, 199),
        ],
    )

    title = attrs.get("title", "Rich")
    rows = int(attrs.get("lines", 24))
    columns = int(attrs.get("columns", 100))
    transparent = attrs.get("transparent", False)

    console = Console(
        file=io.StringIO(),
        record=True,
        force_terminal=True,
        color_system="truecolor",
        width=columns,
        height=rows,
    )
    error_console = Console(stderr=True)

    globals: dict = {}
    try:
        exec(source, globals)
    except Exception:
        error_console.print_exception()
        # console.bell()

    format = CODE_FORMAT
    if not transparent:
        format = """<pre><code>""" + format + """</code></pre>"""

    if "output" in globals:
        console.print(globals["output"])
    output_svg = console.export_svg(title=title, code_format=format, theme=THEME)
    return output_svg


def glyphs(source: str, language, css_class, options, md, attrs, **kwargs) -> str:
    _lines = [line.replace("~", "") for line in source.splitlines()]
    _source = GLYPHS_CODE.format_map({"lines": _lines})
    return rich(_source, language, css_class, options, md, attrs, **kwargs)
