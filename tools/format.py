from fonts import FIRA_CODE_DRAWING_SUBSET

CODE_FORMAT = (
    """\
<svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <!-- Generated with Rich https://www.textualize.io -->
    <style>
        @font-face {{
            font-family: 'fira_coderegular';
            src: url(data:application/font-woff2;charset=utf-8;base64,"""
    + FIRA_CODE_DRAWING_SUBSET
    + """) format('woff2');
            font-weight: normal;
            font-style: normal;
        }}
        .{unique_id}-matrix {{
            font-family: fira_coderegular, 'SF Mono', Consolas, 'Courier New', monospace;
            font-size: {char_height}px;
            line-height: {line_height}px;
            font-variant-east-asian: full-width;
        }}
    {styles}
    </style>
    <defs>
        <clipPath id="{unique_id}-clip-terminal">
            <rect x="0" y="0" width="{terminal_width}" height="{terminal_height}" />
        </clipPath>
        {lines}
    </defs>
    <g transform="translate({terminal_x}, {terminal_y})" clip-path="url(#{unique_id}-clip-terminal)">
    {backgrounds}
    <g class="{unique_id}-matrix">
    {matrix}
    </g>
    </g>
</svg>
"""
)
