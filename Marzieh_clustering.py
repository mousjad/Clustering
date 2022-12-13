import trimesh
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, OPTICS
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
from tqdm import tqdm
import easygui

def main():
	fid = easygui.fileopenbox('Choose .asc file', 'Choose .asc file')
	pc = np.loadtxt(fid)

	pcd = trimesh.PointCloud(pc)

	trans = np.array(((0.00267553, -0.999992, -0.00283233, 1187.8),
					 (0.999996, 0.00267354, 0.0007051, -1.23891),
					 (-0.000697522, -0.0028342, 0.999996, 1043.45),
					  (0, 0, 0, 1)))

	pcd.apply_transform(trans)

	height = np.percentile(pcd.vertices[:,2], 99)
	idx = np.where((pcd.vertices[:, 2] > height))[0]

	pcd1 = pcd[idx, :]
	best_score = -np.inf
	best_score_cluster = -1
	lscore = []
	for i in tqdm(range(2, 20)):
		kmeans = KMeans(n_clusters=i, n_init='auto')
		clusters = kmeans.fit_predict(pcd1)
		score = silhouette_score(pcd1, clusters.reshape(-1))
		lscore.append(score)

		if score > best_score:
			best_score = score
			best_score_cluster = clusters
			best_score_kmeans = kmeans

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.scatter(pcd1[:, 0], pcd1[:, 1], pcd1[:,2], c=best_score_cluster, cmap='jet')
	plt.show()

	plt.plot(range(2, 20), np.array(lscore))
	plt.grid()
	plt.show()
	print(best_score_cluster.max()+1)

	classification = -np.ones(pcd.vertices.shape[0])
	classification[idx] = best_score_cluster

	show_height = height-1
	pcdshow = pcd[np.nonzero(pcd[:,2]>show_height)]
	classificationshow = classification[np.nonzero(pcd[:,2]>show_height)]


	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.scatter(pcdshow[:, 0], pcdshow[:, 1], pcdshow[:, 2], c=classificationshow, cmap='jet')
	plt.show()

	fid = easygui.filesavebox('Select where to save file', 'Select where to save file', default='Classification.txt', filetypes='.txt')
	if not fid.endswith('.txt'):
		fid = fid + '.txt'
	np.savetxt(fid, classification)
	return None

if __name__ == '__main__':
    main()