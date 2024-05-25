# display-colors

`display-colors` is a program to explore the color and display effect capabilities of a terminal emulator

## Compatibility

`display-colors` runs on macOS and Linux.
It requires Python 3.

## Installation and Use

`display-colors` should be installed in a virtual environment.

### How to Create, Use and Destroy a Virtual Environment

```
python -m venv .venv         // Create the virtual environment '.venv'
source .venv/bin/activate    // Enter .venv
(.venv) ...                  // While in the virtual environment, your prompt will be prefixed with '(.venv)'
(.venv) deactivate           // Exit .venv
rm -rf .venv                 // Destroy .venv
```

### How to Install and Uninstall `display-colors`

```
(.venv) python -m pip   install display-colors  // Install
(.venv) python -m pip uninstall display-colors  // Uninstall
```

### Use

```
(.venv) display-colors [--help|--version] COMMAND [OPTIONS]
```

COMMAND: 4-bit | 8-bit | effects

OPTIONS vary depending on the command; do `display-colors COMMAND --help` to list them

## Features

Modern terminal emulators support color but the results vary across emulators, let alone across platforms.  Three sets of colors are available: 4 bit, 8 bit and 24 bit.  They may not be completely supported.

`display-colors` produces test patterns that include all of the 4- and 8-bit colors: all foreground-background combinations of 4-bit colors, which can vary depending on the theme, and swatches of all 8-bit colors.  It also demonstrates each Select Graphic Rendition (SGR) code controlling effects like underline and blink.  Support for these among emulators is spotty.

The SGR codes also specify four font weights: default, dim, medium and bold.  Implementation of these varies.  The `--weight` option in 4-bit mode lets you specify what weights you would like to see (8-bit mode text uses the default weight).

One of the widely-supported effects is reverse video.  This is not always implemented by swapping foreground and background colors.  The `--reverse-video` option displays each line twice, the second with foreground and background colors swapped *and* reverse video turned on.  If reverse video is implemented simply by swapping the two lines will appear identical; if not, they won't.

The program has four modes:

 - 4-bit -- A color palette in the traditional format, one background color per column (*qv* [iTerm2 Color Schemes](https://iterm2colorschemes.com/))
 - 4-bit transpose -- A palette with one foreground color per column
 - 8-bit -- A palette of background colors, including the standard 16 and grayscale (*qv* [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit))
 - effects -- A test pattern of terminal effects

### 4-bit mode (`display-colors 4-bit`)

Options:

 - `--col-width` *`n`* -- Width of the columns in the body of the output table (default: 7)
 - `--gutter` *`string`* -- Delimiter between output columns (default: empty string)
 - `--reverse-video` -- Displays each row twice, the second time with BG-color on FG-color in reverse video.  If your terminal emulator implements reverse video by swapping background and foreground, the two lines will appear identical
  - `--stanzas` -- Group output rows by color (default: off)
 - `--text` *`string`* -- Specifies the sample text to be displayed in each cell (default: 'gYw')
 - `-w` *`string`*, `--weight` *`string`* -- Specifies which weight font to display and in what order (use multiple times).  Supported weights are `dim`, `default`, `medium`, `bold` and `all` (default: `default`, `bold`)

This format lists background colors one per column with their SGR codes at top and left.  The default background color is the leftmost column and the topmost rows show the default foreground color.

Each row is labeled on the left with its weight.  If the row is reverse video, the weight label will appear in reverse video.

### 4-bit transpose mode (`display-colors 4-bit --transpose`)

Options:

 - `--col-width` *`n`* -- (see '4-bit mode' above)
 - `--gutter` *`string`* -- (see '4-bit mode' above)
 - `--reverse-video` -- (see '4-bit mode' above)
 - `-w` *`string`*, `--weight` *`string`* -- (see '4-bit mode' above)

This format lists foreground colors one per column, with the default foreground color in the leftmost column and the default background color in the topmost rows.  The SGR codes are not shown and the sample text is of the form FG/BG.

### 8-bit mode (`display-colors 8-bit`)

This has three parts:

 - 16 standard and bright colors
 - The palette of 216 RGB colors
 - 24 grayscale colors

These are displayed as background colors.  The text in each cell is the hexadecimal value of the color code; for example, the background color of cell D8 in the test pattern is given by the ANSI escape code `\033[48;5;216m`.  The foreground colors in the test pattern are (standard) white for the darker cells and black for the lighter ones.  Some terminal emulators modify this in an attempt to improve the contrast.

The text in the cells is in hexadecimal by default because it is more readable and to save space.

The sixteen standard colors are presented just above their 4-bit equivalents (sometimes these are different).

The 216 RGB colors are arranged in a 6x6 cube, displayed in 6 slices with the origin at the back upper left corner.  We assign codes to them in xyz order, with the x coordinate varying first.  The x coordinate moves left to right, the y coordinate top to bottom and the z coordinate back to front.  The display shows three views of the cube, one per row: head-on sliced back to front, from above sliced top to bottom and from the left sliced left to right.  (The view in the [ANSI escape code illustration](https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit) is the second of these views).

From these slices you can see that the darker cells occupy the top half of the cube, the greens the back lower left corner, the reds the front upper left corner and the blues the back upper right corner.

### Effects mode (`display-colors effects`)

Options:

 - `--pattern` *`string`* -- Specify a string to use as a sample text pattern (default: '|').  Most screens will not be wide enough to accomodate a test pattern string of more than one character.  (If the pattern string contains a character that has a special meaning to the shell, like '|', it must be escaped (preceded) by a backslash: `--pattern \|`).
 - `--gutter` *`string`* -- (see '4-bit mode' above)

Displays a sample of the effect of each SGR code in all 4-bit foreground and background colors (see [Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) for the list of SGR codes).  Some effects may be more visible in certain colors than in others.  The text samples are displayed in groups of three:

 1.  Without applying the effect
 2.  After turning the effect on
 3.  After turning the effect off again

So for a supported effect, you should see that effect applied to the second character only and the first and third characters should be identical.

Practically all of the effects can be individually turned on and off.  One code was unwisely assigned to both 'bold off' and 'double underline on', and for emulators that support double underline you can see this in the 'Bold:' row.  For those emulators you should substitute a different SGR code, such as the one for 'medium', in place of 'bold off'.

### Color names

The display uses abbreviations for the colors, as follows:

 | | |
 | :---: | :--- |
 | df | Default color |
 | bk | Black |
 | re | Red |
 | gr | Green |
 | ye | Yellow |
 | bl | Blue |
 | ma | Magenta |
 | cy | Cyan |
 | wh | White |
 | BK | Bright black |
 | RE | Bright red |
 | GR | Bright green |
 | YE | Bright yellow |
 | BL | Bright blue |
 | MA | Bright magenta |
 | CY | Bright cyan |
 | WH | Bright white |

## Problems

If the terminal somehow gets into a confused state, it will not display colors correctly.  If the output of `display-colors` looks incorrect, try one of the following to reset the terminal:

```bash
reset
tput reset
```

## Examples

Traditional 4-bit palette, including all font weights, with reverse-video rows, divided into stanzas by color:
```bash
display-colors 4-bit --weight all --reverse-video --stanzas
```
4-bit palette with one column per foreground color, rows ordered 'dim, medium, bold, medium' and spaces between the columns:
```bash
display-colors 4-bit --transpose -w dim -w medium -w bold -w medium --gutter ' '
```
8-bit display including standard and bright colors, 216-color RGB palette and grayscale background colors:
```bash
display-colors 8-bit
```
Terminal effect test pattern with spaces between the columns:
```bash
display-colors effects --gutter ' '
```
