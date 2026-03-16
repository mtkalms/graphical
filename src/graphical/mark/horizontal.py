from graphical.mark import Mark

#  BAR

BAR_BLOCK_H = Mark(" ▏▎▍▌▋▊▉█", " ▕▕▕▐▐▐███", invertible=True)
BAR_LIGHT_H = Mark(" ╴─", " ╶─")
BAR_HEAVY_H = Mark(" ╸━", " ╺━")

# WHISKER

WHISKER_LIGHT_H = Mark(" ─", caps=("┤", "├"))
WHISKER_HEAVY_H = Mark(" ━", caps=("┫", "┣"))
WHISKER_DOUBLE_H = Mark(" ═", caps=("╣", "╠"))

# LOLLIPOP

LOLLIPOP_OUTLINE_LIGHT_H = Mark(" ─", caps="◯")
LOLLIPOP_OUTLINE_HEAVY_H = Mark(" ━", caps="◯")
LOLLIPOP_FILLED_LIGHT_H = Mark(" ─", caps="●")
LOLLIPOP_FILLED_HEAVY_H = Mark(" ━", caps="●")
