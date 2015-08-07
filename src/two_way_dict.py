class TwoWayDict(dict):
	def __init__(self, d):
		super().__init__()
		for key, value in d.items():
			self[key] = value
			self[value] = key

	def __setitem__(self, key, value):
		if key in self:
			del self[key]
		if value in self:
			del self[value]
		super().__setitem__(key, value)
		super().__setitem__(value, key)

	def __delitem__(self, key):
		super().__delitem__(self[key])
		super().__delitem__(key)

	def __len__(self):
		return super().__len__() // 2
