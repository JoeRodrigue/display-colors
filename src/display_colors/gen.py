from collections.abc import Generator

def cat_gens(*gens: list[Generator[str, str, str]]) -> Generator[str, str, str]:
	for gen in gens:
		yield from gen

# from typing          import Callable
# from display_colors.const import COLOR_REPR

# def color_gen(colors: tuple[str], modifier: Callable) -> Generator[str, str, str]:
# 	for color in colors:
# 		yield modifier(COLOR_REPR[color])
