import sys
import csv
import urllib
import pandas as pd
import StringIO
from sklearn.cluster import KMeans
from collections import Counter

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


def main(argv):
  data = read_data()
  data_normalize = normalize_data(data)
  customer_segment(data_normalize)
if __name__ == "__main__":
  sys.exit(main(sys.argv))