import numpy as np
import random


class BPPGenerator():
# Input: number of items N,
#       size of optimal bin(cube/square) Bin = [L, W, H] / [L, W] ( cube / square ),
#.      batch_size
# Output: batch_items, batch_rotation
	def __init__(self, N, Bin, batch_size, random_seed = None):
		self.N = N
		self.Bin = Bin
		self.batch_size = batch_size

	def BatchData(self):
		def BPPGenerator(N, Bin):
			items = [Bin]
			while len(items) < N:
				pop_item = [1]
				while max(pop_item) == 1:
					choose_item = random.randint(0, len(items) - 1)
					pop_item = items.pop(choose_item)
				choose_axis = random.randint(0, len(Bin) - 1)
				while pop_item[choose_axis] == 1:#cannot split
					choose_axis = random.randint(0, len(Bin) - 1)
				choose_position = random.randint(1, pop_item[choose_axis] - 1)
				new_item1, new_item2 = pop_item[:], pop_item[:]
				new_item1[choose_axis] = choose_position
				new_item2[choose_axis] = pop_item[choose_axis] - choose_position
				items.append(new_item1)
				items.append(new_item2)
			if len(self.Bin) == 3:
				rotation = np.random.randint(0, 2, (N, 3)).tolist()
			else:
				rotation = np.random.randint(0, 2, N).tolist()
			return items, rotation
		batch_items, batch_rotation = [], []
		i = 0
		while i < self.batch_size:
			data = BPPGenerator(self.N, self.Bin)
			batch_items.append(data[0])
			batch_rotation.append(data[1])
			i += 1
		return batch_items, batch_rotation


if __name__ == '__main__':
	data = BPPGenerator(10, [10, 10], 1)
	batch_data = data.BatchData()
	print(batch_data)
