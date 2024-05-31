from collections.abc import Generator

def cat_gens(*gens: list[Generator[str, str, str]]) -> Generator[str, str, str]:
	for gen in gens:
		yield from gen
