from collections.abc import Iterable, Iterator

def cat_gens(*gens: Iterable[str]) -> Iterator[str]:
	for gen in gens:
		yield from gen
