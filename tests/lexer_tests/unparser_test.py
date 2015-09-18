import math
from nose.tools import *
from mathwords.lexer import *

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

def test_unparse_handles_decimals():
	# will require changing if lexer.ARBITRARY_AMOUNT changes
	assert_equal(unparse(5/3), "one point six six six six seven")
	assert_equal(unparse(0.1), "zero point one")
	assert_equal(unparse(0.99999999), "one")
