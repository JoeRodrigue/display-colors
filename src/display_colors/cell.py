from display_colors.const import (
	RESET,
	REV_VIDEO,
	SGR_BEG,
	SGR_END,
	WEIGHT_ATTR,
)
from display_colors.init import (
	_4_BIT_BG_REPR_ATTR,
	_4_BIT_FG_REPR_ATTR,
	_8_BIT_BG_REPR_ATTR,
	_8_BIT_FG_REPR_ATTR,
)

def colored_cell(attrs: int, text: str) -> str:
	return f'{SGR_BEG}{attrs}{SGR_END}{text}{SGR_BEG}{RESET}{SGR_END}'

def create_attrs(weight: str, fg_repr: str, bg_repr: str, rev_video: bool = False, _8_bit: bool = False) -> str:
	(fg, bg) = (bg_repr, fg_repr) if rev_video else (fg_repr, bg_repr)
	(fg_repr_attr, bg_repr_attr) = (_8_BIT_FG_REPR_ATTR, _8_BIT_BG_REPR_ATTR) if _8_bit else (_4_BIT_FG_REPR_ATTR, _4_BIT_BG_REPR_ATTR)
	rev_video_attr = f';{REV_VIDEO}' if rev_video else f''
	return f'{WEIGHT_ATTR[weight]};{fg_repr_attr[fg]};{bg_repr_attr[bg]}{rev_video_attr}'

def cell_text(fg_repr: str = '', bg_repr: str = '', text: str = '', transpose: bool = False, cell_w: int = 0) -> str:
	str = f'{fg_repr}/{bg_repr}' if transpose else text
	w   = cell_w or len(str) + 2
	return f'{str:^{w}}'
