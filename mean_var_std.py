import numpy as np

def calculate(n):
	# Test to be sure the list is long enough, and that it's actually type: list
	if len(n) != 9:
		raise ValueError("List must contain 9 numbers.")
	if n == []:
		raise Exception("You must enter a list with 9 digits.")

	# create numpy array object from the provided list
	m = np.array([n]).reshape(3,3)
	
	# column, row, and flattened mean
	col_mean = [m[:,0].mean(), m[:,1].mean(), m[:,2].mean()]
	row_mean = [m[0,:].mean(), m[1,:].mean(), m[2,:].mean()]
	mean = m.mean()
	
	# column, row, and flattened variance
	col_var = [m[:,0].var(), m[:,1].var(), m[:,2].var()]
	row_var = [m[0,:].var(), m[1,:].var(), m[2,:].var()]
	variance = m.var()
	
	# column, row, and flattened standard deviation
	col_std = [m[:,0].std(), m[:,1].std(), m[:,2].std()]
	row_std = [m[0,:].std(), m[1,:].std(), m[2,:].std()]
	std = m.std()
	
	# column, row, and flattened minimum values
	col_min = [m[:,0].min(), m[:,1].min(), m[:,2].min()]
	row_min = [m[0,:].min(), m[1,:].min(), m[2,:].min()]
	minimum = m.min()
	
	# column, row, and flattened maximum values
	col_max = [m[:,0].max(), m[:,1].max(), m[:,2].max()]
	row_max = [m[0,:].max(), m[1,:].max(), m[2,:].max()]
	maximum = m.max()
	
	# column, row, and flattened sums
	col_sum = [m[:,0].sum(), m[:,1].sum(), m[:,2].sum()]
	row_sum = [m[0,:].sum(), m[1,:].sum(), m[2,:].sum()]
	array_sum = m.sum()
	
	calculated = {
			'mean': [col_mean, row_mean, mean],
			'variance': [col_var, row_var, variance],
			'standard deviation': [col_std, row_std, std],
			'max': [col_max, row_max, maximum],
			'min': [col_min, row_min, minimum],
			'sum': [col_sum, row_sum, array_sum]}
	
	return calculated
