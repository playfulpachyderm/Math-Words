from nose.tools import *
from mathwords.lexer import *

# ============ Words to numbers ============

def test_tokenize_breaks_numbers_into_powers_of_1000():
	assert_equal(
		tokenize([0]),
		{1: [0]}
	)
	assert_equal(
		tokenize([40, 3, 1000000, 3, 100, 5]),
		{1000000: [40, 3], 1: [3, 100, 5]}
	)

def test_tokenize_fails_on_multiple_values_for_same_power():
	assert_raises(ValueError, tokenize, [40, 3, 1000000, 20, 1000000])

def test_parse_token():
	# without hundreds
	assert_equal(parse_token([40, 3]), 43)
	assert_equal(parse_token([30, 0]), 30)

	# with hundreds
	assert_equal(parse_token([5, 100, 40, 3]), 543)

def test_parse_token_fails_if_given_invalid_numbers():
	assert_raises(ValueError, parse_token, [3, 5])   # multiple of the same digit
	assert_raises(ValueError, parse_token, [3, 40])  # out of order

def test_parse_number_helper():
	assert_equal(helper(528), 2)
	assert_equal(helper(84), 1)
	assert_equal(helper(3), 0)
	assert_equal(helper(0), 0)

def test_parse_number_translates_string_to_number():
	assert_equal(parse_number("forty three million three hundred five"), 43000305)

def test_parse_number_can_handle_zero():
	assert_equal(parse_number("zero"), 0)

def test_parse_number_can_handle_negatives():
	assert_equal(parse_number("twenty one"), 21)

def test_parse_number_fails_if_given_nonnumber_string():
	assert_raises(KeyError, parse_number, "fasdf")

#TODO: update this with "a" into "one" regex
def test_reformat():
	# should strip whitespace, remove "and"s, turn "a"
	# into "one", and change to lowercase
	str1 = "   a million a thousand FIVE Hundred AND fifty five     "
	str2 = "one million one thousand five hundred fifty five"
	assert_equal(reformat(str1), str2)

def test_evaluate_handles_basic_operations():
	assert_equal(evaluate("three added to eight"), 11)
	assert_equal(evaluate("twenty three minus four"), 19)
	assert_equal(evaluate("five times six"), 30)
	assert_equal(evaluate("twenty eight divided by seven"), 4)
	assert_equal(evaluate("five to the power of three"), 125)

def test_evaluate_handles_repeated_operations():
	assert_equal(evaluate("five times five times five"), 125)

def test_evaluate_handles_order_of_operations():
	assert_equal(evaluate("eight minus five plus three"), 6)
	assert_equal(evaluate("ten divided by two plus three"), 8)

# ============ Numbers to words ============

def test_unparse_part():
	assert_equal(unparse_part(38).strip(), "thirty eight")
	assert_equal(unparse_part(512).strip(), "five hundred twelve")

def test_unparse_translates_number_to_string():
	assert_equal(unparse(1500), "one thousand five hundred")
	assert_equal(unparse(158000342), "one hundred fifty eight million three hundred forty two")

def test_unparse_handles_zero():
	assert_equal(unparse(0), "zero")

def test_unparse_handles_multipliers():
	assert_equal(unparse(1), "one")
	assert_equal(unparse(1000), "one thousand")
	assert_equal(unparse(1000000), "one million")

def test_unparse_handles_negatives():
	assert_equal(unparse(-12), "negative twelve")

