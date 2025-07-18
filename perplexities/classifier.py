import pandas as pd
from ipykernel.kernelapp import kernel_aliases
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
import statistics

def perp_translate(row):
    if 'shuffle_control' in row['perturb']:
        return 1
    else:
        return 0

perplexity_result = pd.read_csv('perplexity_results_new.csv')
perplexity_result['possible'] = perplexity_result.apply(perp_translate, axis=1)
perplexity_result.drop(perplexity_result[perplexity_result.perturb.str.contains('adj')].index, inplace=True)
perplexity_result.drop(perplexity_result[perplexity_result.lang.str.contains('RN')].index, inplace=True)
perplexity_result = perplexity_result[perplexity_result['lang'] == 'IT']
perplexity_result.drop(['lang', 'seed', 'perturb'], axis=1, inplace=True)
checkpoints = [f'checkpoint{str(n)}' for n in range(0, 1201,100)]


impossible = perplexity_result[perplexity_result.possible==0]
possible = perplexity_result.drop(perplexity_result[perplexity_result.possible==0].index)

X = perplexity_result[checkpoints]
y = perplexity_result['possible']

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=42)

clf= svm.SVC(kernel='linear', C=1, gamma='auto')
# clf.fit(X_train, y_train)
pipeline = Pipeline([
    ('oversample', RandomOverSampler(random_state=42)),
    ('svc', clf)
])

# sorted(clf.cv_results_['mean_test_score'])
cross_val = cross_val_score(pipeline, X_train, y_train, cv=10, scoring='f1_macro')
print(cross_val)
print("Mean:",sum(cross_val)/len(cross_val))
sd = statistics.stdev(cross_val)
print("Standard Deviation:", sd)