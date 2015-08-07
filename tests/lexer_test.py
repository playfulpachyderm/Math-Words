from lexer import *
from nose.tools import *

def test_str_to_num_array():
	assert_equal(str_to_num_array("zero"),
								  [0])
	assert_equal(str_to_num_array("twenty one"),
								  [20, 1])
	assert_equal(str_to_num_array("forty three million three hundred five"),
								  [40, 3, 1000000, 3, 100, 5])
	assert_raises(KeyError, str_to_num_array, "fasdf")

def test_tokenize():
	assert_equal(
		tokenize([0]),
		{1: [0]}
	)
	assert_equal(
		tokenize([40, 3, 1000000, 3, 100, 5]),
		{1000000: [40, 3], 1: [3, 100, 5]}
	)

	assert_raises(ValueError, tokenize, [40, 3, 1000000, 20, 1000000])

def test_parse_token():
	assert_equal(parse_token([40, 3]), 43)
	assert_equal(parse_token([5, 100, 40, 3]), 543)

def test_unparse_part():
	assert_equal(unparse_part(0), "zero")
	assert_equal(unparse_part(38).strip(), "thirty eight")
	assert_equal(unparse_part(512).strip(), "five hundred twelve")

def test_unparse():
	assert_equal(unparse(1500), "one thousand five hundred")
	assert_equal(unparse(158342), "one hundred fifty eight thousand three hundred forty two")
	assert_equal(unparse(0), "zero")
	assert_equal(unparse(-1), "negative one")

def test_reformat():
	str1 = "   FIVE Hundred AND fifty five     "
	str2 = "five hundred fifty five"
	assert_equal(reformat(str1), str2)

def test_evaluate():
	pass
