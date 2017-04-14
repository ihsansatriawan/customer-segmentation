import sys

def pct_rank_qcut(series, n):
  edges = pd.Series([float(i) / n for i in range(n + 1)])
  f = lambda x: (edges >= x).argmax()
  return series.rank(pct=1).apply(f)

def normalize_data():
  # Normalize data with pct_rank_qcut method

def main(argv):
  normalize_data()
if __name__ == "__main__":
  sys.exit(main(sys.argv))