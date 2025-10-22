[![Test](https://github.com/mtkalms/graphical/actions/workflows/python-package.yml/badge.svg)](https://github.com/mtkalms/graphical/actions/workflows/python-package.yml)
[![Ruff](https://github.com/mtkalms/graphical/actions/workflows/ruff-format.yml/badge.svg)](https://github.com/mtkalms/graphical/actions/workflows/ruff-format.yml)
![OS support](https://img.shields.io/badge/OS-macOS%20Linux%20Windows-blue)

# Graphical

Graphical is a modular visualization library for the terminal. It is based on the console protocol of [Rich][rich] and is fully compatible with [Textual][textual].

> **NOTE:** Future versions of Textual might include a limited number of graphs and charts (see [Textual Roadmap][roadmap]).

## Graphical Library

### Sparkline

> Sparklines are included in Textual since version 0.27.0 (June 2023)

<img src="img/sparkline.svg" alt="Sparkline Table Example" style="width:720px;"/>

### Ridgeline Chart

<img src="img/ridgeline.svg" alt="Ridgeline Example" style="width:720px;"/>

<details>
  <summary>Variations</summary>
  <img src="img/ridgeline-variations.svg" alt="Ridgeline variations" style="width:720px;"/>
</details>

### Bar

<img src="img/bar-variations.svg" alt="Bar Table Example" style="width:720px;"/>

#### Bar Chart

> Bar charts might be part of future versions of Textual (see [Textual Roadmap][roadmap]).

<img src="img/bar.svg" alt="BarChart Example" style="width:720px;"/>

#### Diverging Bar Chart

<img src="img/bar-diverging.svg" alt="DivergingBarChart Example" style="width:720px;"/>

#### Stacked Bar Chart

<img src="img/bar-stacked.svg" alt="StackedBarChart Example" style="width:720px;"/>

#### Double Bar Chart

<img src="img/bar-double.svg" alt="DoubleBarChart Example" style="width:720px;"/>

## Similar Projects

- [asciichart][asciichart]: line plots
- [drawille][drawille]: drawing in Braille characters
- [gantt][gantt]: gantt charts
- [plotille][plotille]: plots, histograms and images
- [termgraph][termgraph]: bar and calendar graphs
- [terminalplot][terminalplot]: minimalistic plots
- [termplot][termplot]: simple plots
- [termplotlib][termplotlib]: line plots and histograms with a matplotlib feel

### Rich ready

- [netext][netext]: network graphs
- [plotext][plotext]: plots and images
- [rich-pixels][rich-pixels]: images
- [termcharts][termcharts]: bar, pie and doughnut charts

### Textual ready

- [textual-plotext][textual-plotext]: textual wrapper for plotext
- [textual-plot][textual-plot]: plots with panning and zooming

[asciichart]: https://github.com/kroitor/asciichart
[drawille]: https://github.com/asciimoo/drawille
[gantt]: https://github.com/andrew-ls/gantt
[netext]: https://github.com/mahrz24/netext/
[plotext]: https://github.com/piccolomo/plotext
[plotille]: https://github.com/tammoippen/plotille
[rich-pixels]: https://github.com/darrenburns/rich-pixels
[rich]: https://github.com/Textualize/rich
[roadmap]: https://textual.textualize.io/roadmap/
[termcharts]: https://github.com/Abdur-rahmaanJ/termcharts
[termgraph]: https://github.com/mkaz/termgraph
[terminalplot]: https://github.com/kressi/terminalplot
[termplot]: https://github.com/justnoise/termplot
[termplotlib]: https://github.com/nschloe/termplotlib
[textual-plot]: https://github.com/davidfokkema/textual-plot
[textual-plotext]: https://github.com/Textualize/textual-plotext
[textual]: https://github.com/Textualize/textual
