import numpy as np
import torch

def generate_2D_gaussian(num_points, mu, sigma=np.eye(2)):
	"""
	Generates num_points*len(mu) total data points, with equal numbers coming from each center specified in mu.

	Parameters:
	int num_points: the total number of data points to generate from each center
	list mu: list of length 2 arrays specifying the location of each 2D gaussian to generate points from
	list sigma: if not None, must be a list of equal length to mu, each item being a 2D covariance matrix 
	corresponding to the 
	"""
	data_set = np.array([])
	for i in range(len(mu)):
		data = np.random.multivariate_normal(mean=mu[i], cov=sigma, size=num_points)
		if data_set.size == 0:
			data_set = data
		else:
			data_set = np.concatenate([data_set,data])
	return data_set


def gaussian_batch(batch_size, num_centers, num_points, r=0.5):
	"""
	Generates a set of almost-surely positive samples from a mixture of gaussians centered around the origin.
	
	Parameters:
	int batch_size: the number of samples to generate for the batch
	int num_centers: the number of gaussians to use for generating samples
	int num_points: the number of points to generate for each sample
	float r: (default r=0.5) radius of circle to place the centers on
	"""

	assert num_points % num_centers == 0

	num_points = int(num_points/num_centers)
	print(num_points)
	centers = []
	for i in range(num_centers):
		theta = 2 * np.pi * i / num_centers + np.pi / 4
		centers.append([r * np.cos(theta) + 2 * r, r * np.sin(theta) + 2 * r])

	batch = []
	for i in range(batch_size):
		sample = generate_2D_gaussian(num_points, centers, sigma=0.001*np.eye(2))
		torch_sample = torch.Tensor(sample)
		batch.append(torch_sample)
	return batch


if __name__ == '__main__':
	import matplotlib.pyplot as plt
	points_per_center = 50
	centers = [[0.3, 0.5], [0.6, 0.7], [0.9, 0.3]]
	data = generate_2D_gaussian(points_per_center, centers, sigma=0.001*np.eye(2))

	fig = plt.figure()
	colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
	for i in range(len(centers)):
		plt.scatter(data[i*points_per_center:(i+1)*points_per_center,0],
			    data[i*points_per_center:(i+1)*points_per_center,1], c=colors[i%len(colors)])
	plt.show()
	plt.close()

	batch_size = 2
	num_centers = 8
	batch = gaussian_batch(batch_size, num_centers, 10*num_centers)
	for j in range(batch_size):
		fig = plt.figure()
		for i in range(num_centers):
			plt.scatter(batch[j].numpy()[i*10:(i+1)*10][:,0],
				    batch[j].numpy()[i*10:(i+1)*10][:,1], c=colors[i%len(colors)])
		plt.show()
