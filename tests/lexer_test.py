from lexer import *
from nose.tools import *

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

	# with hundreds
	assert_equal(parse_token([5, 100, 40, 3]), 543)


def test_parse_number_translates_string_to_number():
	assert_equal(parse_number("forty three million three hundred five"), 43000305)

def test_parse_number_can_handle_zero():
	assert_equal(parse_number("zero"), 0)

def test_parse_number_can_handle_negatives():
	assert_equal(parse_number("twenty one"), 21)

def test_parse_number_fails_if_given_nonnumber_string():
	assert_raises(KeyError, parse_number, "fasdf")

def test_reformat_makes_lowercase_and_removes_whitespace_and_ands():
	str1 = "   FIVE Hundred AND fifty five     "
	str2 = "five hundred fifty five"
	assert_equal(reformat(str1), str2)

def test_evaluate_handles_basic_operations():
	assert_equal(evaluate("three plus eight"), 11)
	assert_equal(evaluate("twenty three minus four"), 19)
	assert_equal(evaluate("five times six"), 30)
	assert_equal(evaluate("twenty eight divided by seven"), 4)
	assert_equal(evaluate("five to the power of three"), 125)

def test_evaluate_handles_order_of_operations():
	assert_equal(evaluate("eight minus five plus three"), 6)
	assert_equal(evaluate("ten divided by two plus three"), 8)

# ============ Numbers to words ============

def test_unparse_part():
	assert_equal(unparse_part(38).strip(), "thirty eight")
	assert_equal(unparse_part(512).strip(), "five hundred twelve")

def test_unparse():
	assert_equal(unparse(1500), "one thousand five hundred")
	assert_equal(unparse(158342), "one hundred fifty eight thousand three hundred forty two")
	assert_equal(unparse(0), "zero")
	assert_equal(unparse(-1), "negative one")

