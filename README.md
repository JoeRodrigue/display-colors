# display-colors

`display-colors` is a program to explore the color and display effect capabilities of a terminal emulator

## Compatibility

At present `display-colors` only runs on macOS.
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
(.venv) display-colors [OPTIONS]
```

## Features

`display-colors` produces test patterns that show the capabilities of your terminal emulator.  They include each combination of foreground and background four-bit colors, which can vary depending on the theme (some themes barely support the bright variants of the eight basic colors, which are not included in the original ECMA-48 standard).  The program also demonstrates each Select Graphic Rendition (SGR) code controlling effects like underline and blink.  Support for these among emulators is spotty.

It has three modes:

 - Standard -- A color palette in the traditional format (*qv* [iTerm2 Color Schemes](https://iterm2colorschemes.com/))
 - Transpose -- A palette with one foreground color per column
 - Test -- A test pattern of terminal effects

### Standard mode (default)

Options:

 - `--col-width` *`n`* -- Width of the columns in the body of the output table (default: 7)
 - `--gutter` *`string`* -- Delimiter between output columns (default: empty string)
 - `--reverse-video` -- Repeats each row using BG-color on FG-color in reverse video.  Some terminal emulators don't implement reverse video as BG-color on FG-color.  If yours does, this transformation is a no-op and this row should appear identical to the row above it
 - `--stanzas` -- Group output rows by color (default: off)
 - `--text` *`string`* -- Specifies the sample text to be displayed in each cell (default: `gYw`)
 - `-w` *`string`*, `--weight` *`string`* -- Specifies which weight font to display and in what order (use multiple times).  Supported weights are `dim`, `default`, `medium`, `bold` and `all` (default: `default`, `bold`)

This format lists background colors one per column with their SGR codes at top and left.  The default background color is the leftmost column and the topmost rows show the default foreground color.

Each row is labeled on the left with its weight.  If the row is reverse video, the weight label will appear in reverse video.

### Transpose mode (`--transpose`)

Options:

 - `--col-width` *`n`* -- (see 'Standard mode' above)
 - `--gutter` *`string`* -- (see 'Standard mode' above)
 - `--reverse-video` -- (see 'Standard mode' above)
 - `-w` *`string`*, `--weight` *`string`* -- (see 'Standard mode' above)

This format lists foreground colors one per column, with the default foreground color in the leftmost column and the default background color in the topmost rows.  The SGR codes are not shown and the sample text is of the form fg/bg.

### Test mode (`--test`)

Options:

 - `--pattern` *`string`* -- Specify a string to use as a sample text pattern (default: '|').  Most screens will not be wide enough to accomodate a test pattern string of more than one character.  (If the pattern string contains a character that has a special meaning to the shell, like '|', it must be escaped (preceded) by a backslash: `--pattern \|`).
 - `--gutter` *`string`* -- (see 'Standard mode' above)

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

## Examples

Traditional palette, including all font weights, with reverse-video rows, divided into stanzas by color:

```bash
display-colors --weight all --reverse-video --stanzas
```

Palette with one column per foreground color, rows ordered 'dim, medium, bold, medium' and spaces between the columns:

```bash
display-colors --transpose -w dim -w medium -w bold -w medium --gutter ' '
```

Terminal effect test pattern with spaces between the columns:

```bash
display-colors --test --gutter ' '
```
