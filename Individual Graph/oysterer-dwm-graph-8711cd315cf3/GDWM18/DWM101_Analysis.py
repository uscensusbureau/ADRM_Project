import matplotlib.pyplot as plt
from matplotlib import pyplot
from numpy import mean
from numpy import std
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split


def correlation_analysis():
    precision_array = [1, 1, 0.8889, 0.9854, 0.9911, 0.9457, 0.9464, 0.788, 0.7877, 0.6824, 0.7806, 0.7235, 0.7455,
                       0.701, 0.7571, 0.7699, 0.7825, 0.9478, 0.9707, 0.9419, 0.9579, 0.9543, 0.9622, 0.6908, 0.65,
                       0.6954, 0.756, 0.6995, 0.7511]
    recall_array = [0.963, 0.8958, 0.9286, 0.8869, 0.8729, 0.9737, 0.8665, 0.8881, 0.8827, 0.8453, 0.8116, 0.8348,
                    0.9041, 0.8386, 0.7764, 0.7424, 0.7723, 0.8116, 0.8003, 0.8464, 0.8226, 0.8242, 0.8247, 0.816,
                    0.9331, 0.81578, 0.80716, 0.7514, 0.7948]
    f_measure_array = [0.9811, 0.9451, 0.9083, 0.9335, 0.9282, 0.9595, 0.9047, 0.835, 0.8324, 0.7552, 0.7958, 0.7752,
                       0.8172, 0.7636, 0.7666, 0.756, 0.7774, 0.8745, 0.8773, 0.8916, 0.8851, 0.8845, 0.8882, 0.7666,
                       0.7663, 0.7508, 0.7807, 0.7245, 0.7724]
    plt.scatter(precision_array, recall_array)
    plt.ylabel('Recall')
    plt.xlabel('Precision')
    plt.show()
    plt.scatter(precision_array, f_measure_array)
    plt.ylabel('Precision')
    plt.xlabel('F-Measure')
    plt.show()
    plt.scatter(recall_array, f_measure_array)
    plt.ylabel('Recall')
    plt.xlabel('F-Measure')
    plt.show()
    print('Precision: mean=%.3f stdv=%.3f' % (mean(precision_array), std(precision_array)))
    print('Recall: mean=%.3f stdv=%.3f' % (mean(recall_array), std(recall_array)))
    print('F-measure: mean=%.3f stdv=%.3f' % (mean(f_measure_array), std(f_measure_array)))
    corr1, _ = pearsonr(precision_array, recall_array)
    corr2, _ = pearsonr(precision_array, f_measure_array)
    corr3, _ = pearsonr(recall_array, f_measure_array)
    print('Pearsons correlation between precision and recall: %.3f' % corr1)
    print('Pearsons correlation between precision and f-measure: %.3f' % corr2)
    print('Pearsons correlation between recall and f-measure: %.3f' % corr3)
    corr1, _ = spearmanr(precision_array, recall_array)
    corr2, _ = spearmanr(precision_array, f_measure_array)
    corr3, _ = spearmanr(recall_array, f_measure_array)
    print('Spearman correlation between precision and recall: %.3f' % corr1)
    print('Spearman correlation between precision and f-measure: %.3f' % corr2)
    print('Spearman correlation between recall and f-measure: %.3f' % corr3)


def roc_analysis():
    # generate 2 class dataset
    X, y = make_classification(n_samples=1000, n_classes=2, random_state=1)
    # split into train/test sets
    trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.5, random_state=2)
    # generate a no skill prediction (majority class)
    ns_probs = [0 for _ in range(len(testy))]
    # fit a model
    model = LogisticRegression(solver='lbfgs')
    model.fit(trainX, trainy)
    # predict probabilities
    lr_probs = model.predict_proba(testX)
    # keep probabilities for the positive outcome only
    lr_probs = lr_probs[:, 1]
    # calculate scores
    ns_auc = roc_auc_score(testy, ns_probs)
    lr_auc = roc_auc_score(testy, lr_probs)
    # summarize scores
    print('No Skill: ROC AUC=%.3f' % (ns_auc))
    print('Logistic: ROC AUC=%.3f' % (lr_auc))
    # calculate roc curves
    ns_fpr, ns_tpr, _ = roc_curve(testy, ns_probs)
    lr_fpr, lr_tpr, _ = roc_curve(testy, lr_probs)
    # plot the roc curve for the model
    pyplot.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
    pyplot.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
    # axis labels
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    # show the legend
    pyplot.legend()
    # show the plot
    pyplot.show()


if __name__ == "__main__":
    # correlation_analysis()
    roc_analysis()
