from collections import Counter
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
import StringIO
import sys
import urllib
style.use("ggplot")

def pct_rank_qcut(series, n):
  edges = pd.Series([float(i) / n for i in range(n + 1)])
  f = lambda x: (edges >= x).argmax()
  return series.rank(pct=1).apply(f)

def read_data():
  link = "https://gist.githubusercontent.com/ihsansatriawan/70fa30c1eb366223fd54a1a2462d4fd3/raw/ec0b9d5ffe415e3d7fd2b7ffc9c7c7919b77418c/sample_data.csv"
  f = urllib.urlopen(link)
  datas = f.read()
  data_string = StringIO.StringIO(datas)
  csv_reader = csv.reader(data_string, delimiter=',')
  next(csv_reader, None)
  list_data = list(csv_reader)
  df = pd.DataFrame(list_data, columns=['name', 'recency', 'frequency', 'monetary'])
  return df


def normalize_data(dataFrame):
  dataFrame['recency'] = dataFrame['recency'].astype(float)
  dataFrame['frequency'] = dataFrame['frequency'].astype(float)
  dataFrame['monetary'] = dataFrame['monetary'].astype(float)

  dataFrame['recency'] = pct_rank_qcut(dataFrame.recency, 5)
  dataFrame['frequency'] = pct_rank_qcut(dataFrame.frequency, 5)
  dataFrame['monetary'] = pct_rank_qcut(dataFrame.monetary, 5)

  return dataFrame

def customer_segment(dataFrame):
  print dataFrame
  cluster_num = 3
  kmeans = KMeans(n_clusters=cluster_num, n_init=50)
  kmeans.fit(dataFrame[dataFrame.columns[1:]])

  dataFrame['cluster'] = kmeans.fit_predict(dataFrame[dataFrame.columns[1:]])
  centroids = kmeans.cluster_centers_
  labels = kmeans.labels_

  c = Counter(labels)
  print "centroids : "
  print centroids

  for cluster_number in range(cluster_num):
    print("Cluster {} contains {} samples".format(cluster_number, c[cluster_number]))

  #visualize 3 dimension
  plot_df = dataFrame[dataFrame.columns[1:5]]
  color = ["b", "g", "r", "c", "m", "y", "k", "w"]
  fig = figure()
  ax = fig.gca(projection='3d')
  for i in range(len(plot_df)):
    ax.scatter(plot_df['recency'][i], plot_df['frequency'][i], plot_df['monetary'][i], c=color[plot_df['cluster'][i]], s=150)
    label = '(%d, %d, %d)' % (plot_df['recency'][i], plot_df['frequency'][i], plot_df['monetary'][i])
    ax.text(plot_df['recency'][i], plot_df['frequency'][i], plot_df['monetary'][i], label)

  ax.scatter(centroids[:, 0],centroids[:, 1], centroids[:, 2], marker = "x", s=150, linewidths = 5, zorder = 100)
  ax.set_xlabel('Recency (R)')
  ax.set_ylabel('Frequency (F)')
  ax.set_zlabel('Monetary (M)')
  plt.show()

  # visualize 2 dimension
  pca_2 = PCA(2)
  plot_columns = pca_2.fit_transform(dataFrame[dataFrame.columns[1:]])

  plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=dataFrame["cluster"])
  plt.show()

def main(argv):
  data = read_data()
  data_normalize = normalize_data(data)
  customer_segment(data_normalize)
if __name__ == "__main__":
  sys.exit(main(sys.argv))