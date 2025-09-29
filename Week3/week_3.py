#!/usr/bin/env python
# coding: utf-8

# # Preliminaries
# 
# The `pandas` library allows the user several data structures for different data manipulation tasks:
# 1. Data storage through its `Series` and `DataFrame` data structures.
# 2. Data filtering using multiple methods from the package.
# 3. Reading data from many different file formats such as `csv`, `txt`, `xlsx`, ...
# 
# Below we provide a brief overview of the `pandas` functionalities needed for these exercises. The complete documentation can be found on the [`pandas` website](https://pandas.pydata.org/).
# 
# ## Pandas data structures
# 
# ### Series
# The Pandas Series data structure is similar to a one-dimensional array. It can store any type of data. The values are mutable but the size not.
# 
# To create `Series`, we call the `pd.Series()` method and pass an array. A `Series` may also be created from a numpy array.

# In[1]:


import pandas as pd
import numpy as np

first_series = pd.Series([1,10,100,1000])

print(first_series)

teams = np.array(['PSV','Ajax','Feyenoord','Twente'])
second_series = pd.Series(teams)

print('\n')
print(second_series)


# ### DataFrame
# One can think of a `DataFrame` as a table with rows and columns (2D structure). The columns can be of a different type (as opposed to `numpy` arrays) and the size of the `DataFrame` is mutable.
# 
# To create `DataFrame`, we call the `pd.DataFrame()` method and we can create it from scratch or we can convert a numpy array or a list into a `DataFrame`.

# In[2]:


# DataFrame from scratch
first_dataframe = pd.DataFrame({
    "Position": [1, 2, 3, 4],
    "Team": ['PSV','Ajax','Feyenoord','Twente'],
    "GF": [80, 75, 75, 70],
    "GA": [30, 25, 40, 60],
    "Points": [79, 78, 70, 66]
})

print("From scratch: \n {} \n".format(first_dataframe))

# DataFrme from a list
data = [[1, 2, 3, 4], ['PSV','Ajax','Feyenoord','Twente'], 
        [80, 75, 75, 70], [30, 25, 40, 60], [79, 78, 70, 66]]
columns = ["Position", "Team", "GF", "GA", "Points"]

second_dataframe = pd.DataFrame(data, index=columns)

print("From list: \n {} \n".format(second_dataframe.T)) # the '.T' operator is explained later on

# DataFrame from numpy array
data = np.array([[1, 2, 3, 4], ['PSV','Ajax','Feyenoord','Twente'], 
                 [80, 75, 75, 70], [30, 25, 40, 60], [79, 78, 70, 66]])
columns = ["Position", "Team", "GF", "GA", "Points"]

third_dataframe = pd.DataFrame(data.T, columns=columns)

print("From numpy array: \n {} \n".format(third_dataframe))


# ### DataFrame attributes
# This section gives a quick overview of some of the `pandas.DataFrame` attributes such as `T`, `index`, `columns`, `iloc`, `loc`, `shape` and `values`.

# In[3]:


# transpose the index and columns
print(third_dataframe.T)


# In[4]:


# index makes reference to the row labels
print(third_dataframe.index)


# In[5]:


# columns makes reference to the column labels
print(third_dataframe.columns)


# In[6]:


# iloc allows to access the index by integer-location (e.g. all team names, which are in the second columm)
print(third_dataframe.iloc[:,1])


# In[7]:


# loc allows to access the index by label(s)-location (e.g. all team names, which are in the "Team" columm)
print(third_dataframe.loc[0, 'Team'])


# In[8]:


# shape returns a tuple with the DataFrame dimension, similar to numpy
print(third_dataframe.shape)


# In[9]:


# values return a Numpy representation of the DataFrame data
print(third_dataframe.values)


# ### DataFrame methods
# This section gives a quick overview of some of the `pandas.DataFrame` methods such as `head`, `describe`, `concat`, `groupby`,`rename`, `filter`, `drop` and `isna`. To import data from CSV or MS Excel files, we can make use of `read_csv` and `read_excel`, respectively.

# In[10]:


# print the first few rows in your dataset with head()
print(third_dataframe.head()) # In this case, it is not very useful because we don't have thousands of rows


# In[11]:


# get the summary statistics of the DataFrame with describe()
print(third_dataframe.describe())


# In[12]:


# concatenate (join) DataFrame objects using concat()

# first, we will split the above DataFrame in two different ones
df_a = third_dataframe.loc[[0,1],:]
df_b = third_dataframe.loc[[2,3],:]

print(df_a)
print('\n')

print(df_b)
print('\n')

# now, we concatenate both datasets
df = pd.concat([df_a, df_b])

print(df)


# In[13]:


# group the data by certain variable via groupby()
# here, we have grouped the data by goals for, which in this case is 75

group = df.groupby('GF')

print(group.get_group('75'))


# In[14]:


# rename() helps you change the column or index names
print(df.rename(columns={'Position':'Pos','Team':'Club'}))


# In[15]:


# build a subset of rows or columns of your dataset according to labels via filter()
# here, items refer to the variable names: 'Team' and 'Points'; to select columns, we specify axis=1
print(df.filter(items=['Team', 'Points'], axis=1))


# In[16]:


# dropping some labels
print(df.drop(columns=['GF', 'GA']))


# In[17]:


# search for NA (not available) entries in the DataFrame
print(df.isna()) # No NA values
print('\n')

# create a pandas Series with a NA value
# the Series as W (winnin matches)
tmp = pd.Series([np.NaN, 25, 24, 19],  name="W")

# concatenate the Series with the DataFrame
df = pd.concat([df,tmp], axis = 1)
print(df)
print('\n')

# again, check for NA entries
print(df.isna())


# ## Dataset
# 
# For this week exercises we will use a dataset from the Genomics of Drug Sensitivity in Cancer (GDSC) project (https://www.cancerrxgene.org/). In this study (['Iorio et al., Cell, 2016']()), 265 compounds were tested on 1001 cancer cell lines for which different types of -omics data (RNA expression, DNA methylation, Copy Number Alteration, DNA sequencing) are available. This is a valuable resource to look for biomarkers of drugs sensitivity in order to try to understand why cancer patients responds very differently to cancer drugs and find ways to assign the optimal treatment to each patient.
# 
# For this exercise we will use a subset of the data, focusing the response to the drug YM155 (Sepantronium bromide) on four cancer types, for a total of 148 cancer cell lines.
# 
# | ID          | Cancer type                      |
# |-------------|----------------------------------|
# |   COAD/READ | Colorectal adenocarcinoma        |
# |   NB        | Neuroblastoma                    |
# |   KIRC      | Kidney renal clear cell carcinoma|
# |   BRCA      | Breast carcinoma                 |
# 
# We will use the RNA expression data (RMA normalised). Only genes with high variability across cell lines (variance > 5, resulting in 238 genes) have been kept.
# 
# Drugs have been tested at different concentration, measuring each time the viability of the cells. Drug sensitivity is measured using the natural log of the fitted IC50 metric, which is defined as the half maximal inhibitory concentration. A lower IC50 corresponds to a more sensitive cell line because a lower amount of drug is sufficient to have a strong response, while a higher IC50 corresponds to a more resistant cell line because more drug is needed for killing the cells.
# 
# Based on the IC50 metric, cells can be classified as sensitive or resistant. The classification is done by computing the $z$-score across all cell lines in the GDSC for each drug, and considering as sensitive the ones with $z$-score < 0 and resistant the ones with $z$-score > 0.
# 
# The dataset is originally provided as 3 files ([original source](https://www.sciencedirect.com/science/article/pii/S0092867416307462?via%3Dihub)) :
# 
# `GDSC_RNA_expression.csv`: gene expression matrix with the cell lines in the rows (148) and the genes in the columns (238).
# 
# `GDSC_drug_response.csv`: vector with the cell lines response to the drug YM155 in terms of log(IC50) and as classification in sensitive or resistant.
# 
# `GDSC_metadata.csv`: metadata for the 148 cell lines including name, COSMIC ID and tumor type (using the classification from ['The Cancer Genome Atlas TCGA'](https://www.cancer.gov/about-nci/organization/ccg/research/structural-genomics/tcga))
# 
# For convenience, we provide the data already curated.
# 
# `RNA_expression_curated.csv`: [148 cell lines , 238 genes]
# 
# `drug_response_curated.csv`: [148 cell lines , YM155 drug]
# 
# The curated data cam be read as `pandas` `DataFrame`s in the following way:

# In[18]:


import pandas as pd

gene_expression = pd.read_csv("./data/RNA_expression_curated.csv", sep=',', header=0, index_col=0)
drug_response = pd.read_csv("./data/drug_response_curated.csv", sep=',', header=0, index_col=0)


# You can use the `DataFrame`s directly as inputs to the the `sklearn` models. The advantage over using `numpy` arrays is that the variable are annotated, i.e. each input and output has a name.

# ## Tools
# The `scikit-learn` library provides the required tools for linear regression/classification and shrinkage, as well as for logistic regression.

# In[1]:


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression


# Note that the notation used for the hyperparameters in the `scikit-learn` library is different from the one used in the lecture. More specifically, in the lecture $\alpha$ is the tunable parameter to select the compromise between Ridge and Lasso. Whereas, `scikit-learn` library refers to `alpha` as the tunable parameter $\lambda$. Please check the documentation for more details.

# # Exercises
# 
# ## Selection of the hyperparameter
# 
# Implement cross-validation (using `sklearn.grid_search.GridSearchCV`) to select the `alpha` hyperparameter of `sklearn.linear_model.Lasso`. 
# 
# 
# ## Feature selection
# 
# Look at the features selected using the hyperparameter which corresponds to the minimum cross-validation error.
# 
# <p><font color='#770a0a'>Is the partition in training and validation sets playing a role in the selection of the hyperparameter? How will this affect the selection of the relevant features?</font></p>
# 
# <p><font color='#770a0a'>Should the value of the intercept also be shrunk to zero with Lasso and Ridge regression? Motivate your answer.</font></p>
# 
# 
# ## Bias-variance 
# 
# Show the effect of the regularization on the parameter estimates in terms of bias and variance. For this you can repeat the optimization 100 times using bootstrap and visualise the profile of the Lasso regression coefficient over a grid of the hyperparameter, optionally including the variability as error bars.
# 
# <p><font color='#770a0a'>Based on the visual analysis of the plot, what are your observation on bias and variance in relation to model complexity? Motivate your answer.</font></p>
# 
# 
# ## Logistic regression
# 
# <p><font color='#770a0a'>Write the expression of the objective function for the penalized logistic regression with $L_1$ and $L_2$ regularisation (as in Elastic net).</font></p>

# In[9]:


import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load curated data
gene_expression = pd.read_csv("./data/RNA_expression_curated.csv", sep=',', header=0, index_col=0)
drug_response = pd.read_csv("./data/drug_response_curated.csv", sep=',', header=0, index_col=0)

# Use continuous outcome (logIC50)
X = gene_expression.values
y = drug_response["YM155"].values

# Define pipeline: scale -> Lasso
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("lasso", Lasso(max_iter=5000))
])

# Define hyperparameter grid for alpha
param_grid = {
    "lasso__alpha": np.logspace(-3, 2, 30)   # test 30 values from 1e-3 to 1e2
}

# Set up cross-validation
grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    cv=5,                       # 5-fold CV
    scoring="neg_mean_squared_error",
    n_jobs=-1
)

# Run search
grid.fit(X, y)

print("Best alpha:", grid.best_params_["lasso__alpha"])
print("Best CV score (neg MSE):", grid.best_score_)


# Best alpha: 0.2592943797404667
# This is the regularization strength chosen by cross-validation for the Lasso model.
# 
# Smaller values of alpha → weaker regularization (more coefficients non-zero, risk of overfitting).
# 
# Larger values of alpha → stronger regularization (more coefficients shrink to zero, simpler model, risk of underfitting).
# 
# Here, the CV process found that α ≈ 0.26 gave the best predictive performance (lowest MSE across folds).
# 

# Best CV score (neg MSE): -5.119. Since MSE is a loss (lower is better), sklearn negates it. So, on average across folds, the mean squared error of predictions was ≈ 5.12. That means that, on the log(IC50) scale, the squared error between predicted and actual values is about 5.12 units on average.

# In[16]:


import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Use your data
X = gene_expression.values
y = drug_response["YM155"].values
genes = gene_expression.columns.tolist()

# Fit Lasso with best alpha found from GridSearchCV
best_alpha = grid.best_params_["lasso__alpha"]

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("lasso", Lasso(alpha=best_alpha, max_iter=5000))
])

pipe.fit(X, y)

# Extract coefficients
lasso_coef = pipe.named_steps["lasso"].coef_

# Make a DataFrame with gene names and coefficients
coef_df = pd.DataFrame({
    "gene": genes,
    "coef": lasso_coef
})

# Keep only non-zero coefficients (selected features)
selected_genes = coef_df[coef_df["coef"] != 0].sort_values(by="coef", key=abs, ascending=False)

print("Number of selected genes:", selected_genes.shape[0])
print(selected_genes)


# Out of 238 total genes, Lasso shrank most coefficients to zero.
# Only 11 genes survived, meaning Lasso considers these the most predictive of YM155 logIC₅₀ at α ≈ 0.26.
# 
# Positive coefficient → higher expression of the gene is associated with higher logIC₅₀ (i.e., more resistant cells).
# 
# Negative coefficient → higher expression is associated with lower logIC₅₀ (i.e., more sensitive cells).

# Now, answering the questions stated in this excercise:
# 
# The partition of training/validation sets does affect the hyperparameter selection and future feature selection.
# Different splits → different training/validation sets. The “best α” depends on how representative the validation sets are of the overall data. Small changes in the split can lead to slightly different validation errors, so the α that minimizes CV error might change. Also, that affects feature selection because Lasso’s sparsity depends on α: higher α → fewer non-zero coefficients. Therefore, if α changes due to a different CV split, the set of selected genes can also change slightly. With small datasets (like 148 cell lines), this effect can be noticeable.
# 
# Last, but not least, the value of the intercept should not be shrunk to zero with Lasso and Ridge regression because it would bias the baseline prediction unnecessarily. The intercept represents the baseline level of the response (average drug sensitivity when all gene expression = 0 after centering). So penalizing it would harm performance without benefit.
# 

# In[ ]:




