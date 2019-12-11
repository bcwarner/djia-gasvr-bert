from sklearn import svm
from sklearn import linear_model
import datetime
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import math
import joblib
import copy
from genetic_selection import GeneticSelectionCV

# Read FRED data
def main():
    djia_in = []
    djia_out = []
    dat_ = []
    dat = []
    st = 0
    with open("DJIA.csv", "r") as djia_r:
        djia_r.readline()
        for l in djia_r:
            x = l.strip().split(",")
            if x[1] == ".":
                continue
            u = [(datetime.datetime.strptime(x[0], "%Y-%m-%d") - datetime.datetime(1970, 1, 1)).total_seconds(), djia_out[-1] if len(djia_out) != 0 else float(x[1]), djia_out[-2] if len(djia_out) > 1 else float(x[1])]
            if x[0] == "2018-11-09": # Check this date
                st = len(dat_)
            v = float(x[1])
            dat_.append(u + [v])

    dat = dat_[st:]
    print(st)
    split = int(.8 * len(dat))

    scaler = MinMaxScaler()
    scaler.fit(dat)
    djia_s = scaler.transform(dat)

    djia_in = [x[:-1] for x in djia_s]
    djia_out = [x[-1] for x in djia_s]

    djia_in_train = np.array(djia_in[:split])
    djia_out_train = np.array(djia_out[:split])
    djia_in_test = np.array(djia_in[split:])
    djia_out_test = np.array(djia_out[split:])

    print(djia_s)

    m = svm.SVR(C=0.01, cache_size=1000, coef0=djia_out_train[-1], degree=5, epsilon=0.005, gamma='auto', kernel='poly', max_iter=5000, shrinking=True, tol=0.0001, verbose=True)

    model = m.fit(djia_in_train, djia_out_train)
    res = copy.deepcopy(m.predict(djia_in_test))

    xs = [x[0] for x in djia_in_test]
    plt.plot(xs, res, "b", label="SVR")

    m2 = GeneticSelectionCV(m, cv=5, verbose=1, scoring="neg_mean_squared_error", n_population=1000, crossover_proba=0.5, mutation_proba=0.2, n_generations=2000, crossover_independent_proba=0.5, mutation_independent_proba=0.05, tournament_size=3, n_gen_no_change=10, caching=True, n_jobs=10)
    m2.fit(djia_in_train, djia_out_train)

    res2 = m2.predict(djia_in_test)


    plt.plot(xs, res2, "g", label="GA/SVR")
    plt.plot(xs, djia_out_test, "m", label="Actual")
    plt.xlabel('Time (scaled)')
    plt.ylabel('Points (scaled)')
    plt.legend()

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(1, len(res)):
        dirres = res[i] - res[i - 1] >= 0
        diract = djia_out_test[i] - djia_out_test[i - 1] >= 0
        if dirres == diract:
            if dirres == True:
                tp += 1
            else:
                tn += 1
        else:
            if dirres == True:
                fp += 1
            else:
                fn += 1

    print(tp, tn, fp, fn)
    
    plt.suptitle("RMSE = " + str(math.sqrt(mean_squared_error(djia_out_test, res))))
    plt.show()

"""
with open("DJIA_out.csv", "w") as djia_w:
    for x in range(len(res)):
        djia_w.write(str(djia_in_test[x][0]) + "," + str(res[x]) + "," + str(djia_out_test[x]) + "\n")
"""

if __name__ == "__main__":
    main()
