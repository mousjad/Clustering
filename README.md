# Clustering

You should have git installed (https://git-scm.com/download/win or download the files from here and skip step one) and conda(https://docs.conda.io/en/latest/miniconda.html) and pip . Here they are:
git clone https://github.com/mousjad/Clustering.git
conda install pip
conda create -n myenv python=3.9
conda activate myenv
pip install -r requirements.txt
python Marzieh_clustering.py

When you want to re-run this later you only have to do the following:
conda activate myenv
python Marzieh_clustering.py
The python code tries KMeans with 2 to 20 clusters and finds the best one according to the silhouette score (https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html).
The height is defined as the 99th percentile of Z values, it was successful for the point cloud you gave me, and I suspect it might be for others.