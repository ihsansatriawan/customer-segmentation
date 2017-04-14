import sys
import csv
import urllib
import pandas as pd
import StringIO

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
  print df

def main(argv):
  read_data()
if __name__ == "__main__":
  sys.exit(main(sys.argv))