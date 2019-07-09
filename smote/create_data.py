import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import make_classification
from imblearn.datasets import make_imbalance

# for reproducibility purposes
seed = 100

# create balanced dataset
X1, Y1 = make_classification(n_samples=700, n_features=2, n_redundant=0,
                             n_informative=2, n_clusters_per_class=1,
                             class_sep=1.0, flip_y=0.06, random_state=seed)

plt.title("Balanced dataset")
plt.xlabel('x')
plt.ylabel('y')
plt.scatter(X1[:, 0], X1[:, 1], marker='o', c=Y1,
            s=25, edgecolor='k', cmap=plt.cm.coolwarm)
plt.show()
df = pd.concat([pd.DataFrame(X1), pd.DataFrame(Y1)], axis=1)
df.columns = ['feature_1', 'feature_2', 'label']
df.to_csv('df_base.csv', index=False, encoding='utf-8')

X_res, y_res = make_imbalance(X1, Y1, sampling_strategy={0: 340, 1: 10}, random_state=seed)
plt.title("Imbalanced dataset")
plt.xlabel('x')
plt.ylabel('y')
plt.scatter(X_res[:, 0], X_res[:, 1], marker='o', c=y_res,
            s=25, edgecolor='k', cmap=plt.cm.coolwarm)
plt.show()

df = pd.concat([pd.DataFrame(X_res), pd.DataFrame(y_res)], axis=1)
df.columns = ['feature_1', 'feature_2', 'label']
df.to_csv('df_imbalanced.csv', index=False, encoding='utf-8')
