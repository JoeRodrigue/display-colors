def base_n_10(n: int, *digits: int) -> int:
	def cont(result: int, digit_list: tuple[int, ...]) -> int:
		return result if not digit_list else cont((result * n) + digit_list[-1], digit_list[:-1])

	return cont(0, digits)
