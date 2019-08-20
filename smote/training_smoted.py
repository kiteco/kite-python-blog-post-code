import pandas as pd

from common import plot_svm_boundary, train_SVM

df = pd.read_csv('df_smoted.csv', encoding='utf-8', engine='python')
clf = train_SVM(df)
plot_svm_boundary(clf, df, "Decision Boundary of SVM trained with a synthetic dataset")
