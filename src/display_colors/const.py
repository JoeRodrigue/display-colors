SGR_BEG   = '\033['
SGR_END   = 'm'
RESET     = 0
DIM       = 2
MEDIUM    = 22
ITALIC    = 3
BOLD      = 1
REV_VIDEO = 7
UNDERLINE = 4

FG_8_BIT_PREFIX = '38;5;'
BG_8_BIT_PREFIX = '48;5;'

CODE_COL_WIDTH = 8       ## Widest attr code is '22;97;7m'

FG_COLOR_4_BIT_OFFSET         = 30
BG_COLOR_4_BIT_OFFSET         = 40
DEFAULT_FG_COLOR_4_BIT_OFFSET = 39
DEFAULT_BG_COLOR_4_BIT_OFFSET = 49
BRIGHT_FG_COLOR_4_BIT_OFFSET  = 90
BRIGHT_BG_COLOR_4_BIT_OFFSET  = 100
FG_COLOR_8_BIT_OFFSET         = 0
BG_COLOR_8_BIT_OFFSET         = 0
BRIGHT_FG_COLOR_8_BIT_OFFSET  = 8
BRIGHT_BG_COLOR_8_BIT_OFFSET  = 8

_8_BIT_COLORS_N         = 256
_8_BIT_PALETTE_OFFSET   = 16

COLORS = (
	'black',
	'red',
	'green',
	'yellow',
	'blue',
	'magenta',
	'cyan',
	'white',
)

COLOR_REPR = {
	'default': 'df',
	'black':   'bk',
	'red':     're',
	'green':   'gr',
	'yellow':  'ye',
	'blue':    'bl',
	'magenta': 'ma',
	'cyan':    'cy',
	'white':   'wh',
}

ALL_WEIGHTS = (
	'Dim',
	'Default',
	'Medium',
	'Bold',
)

WEIGHT_ATTR = {
	'Dim':     DIM,
	'Default': RESET,
	'Medium':  MEDIUM,
	'Bold':    BOLD,
}

WEIGHT_REPR = {
	'Dim':     'Dim',
	'Default': 'Def',
	'Medium':  'Med',
	'Bold':    'Bld',
}
