from nose.tools import *
from mathwords.two_way_dict import TwoWayDict

def test_create_from_dict():
	d = TwoWayDict({"a": "b"})
	assert_equal(d["a"], "b")
	assert_equal(d["b"], "a")

def test_add_item_sets_mirror_key():
	d = TwoWayDict()
	d["a"] = "b"
	assert_equal(d["b"], "a")

def test_add_item_removes_previous_mirror_keys():
	d = TwoWayDict()
	d["a"] = "b"
	d["b"] = "c"
	assert_equal(d["c"], "b")
	assert_raises(KeyError, lambda x: x["a"], d)

def test_del_item_removes_both_keys():
	d = TwoWayDict({"a": "b", "c": "d"})

	del d["a"]
	assert_raises(KeyError, lambda x: x["a"], d)

	del d["d"]
	assert_raises(KeyError, lambda x: x["c"], d)

def test_length():
	d = TwoWayDict({"a": "b", "c": "d"})
	assert_equal(len(d), 2)
