import click

from display_colors.const   import (
	COLOR_REPR,
	COLORS,
	RESET,
	SGR_BEG,
	SGR_END,
	Switch_Attr,
)
from display_colors.init    import (
	_4_BIT_BG_REPR_ATTR,
	_4_BIT_FG_REPR_ATTR,
	init_display_attributes,
)

EFFECT_SWITCH: dict[str, Switch_Attr] = dict()

def color_text(attrs: str, text: str) -> str:
	return f'{SGR_BEG}{attrs}{SGR_END}{text}'

def test_attributes(neutral_text: str, on_text: str, off_text: str, gutter: str) -> None:
	l_col_w = max(len(name + ':') for name in EFFECT_SWITCH.keys())
	for name, sw in EFFECT_SWITCH.items():
		on_attr  = getattr(sw, 'on')
		off_attr = getattr(sw, 'off')
		label = name + ':'
		print(f'{label:<{l_col_w}}', end = ' ')
		for repr_attr in (_4_BIT_FG_REPR_ATTR, _4_BIT_BG_REPR_ATTR):
			for modifier in (str.lower, str.upper):
				for color in COLORS:
					color_attr = repr_attr[modifier(COLOR_REPR[color])]
					print(color_text(   color_attr,          neutral_text), end = '')
					print(color_text(f'{color_attr};{on_attr}',   on_text), end = '')
					print(color_text(f'{color_attr};{off_attr}', off_text), end = '')
					print(color_text(RESET, ''), end = gutter)
		print()

@click.command('effects')
@click.option('--gutter',        '_gutter',       type = str,  help = "String delimiting output columns  [default: empty string]",     default = '',    show_default = True)
@click.option('--pattern',       '_pattern',      type = str,  help = "Sample pattern character for the --test option",                default = '|',   show_default = True)
def display_effects(_gutter: str, _pattern: str):
	"""Complete display of effects the terminal emulator may support"""
	init_display_attributes(EFFECT_SWITCH)
	test_attributes(_pattern, _pattern, _pattern, _gutter)
