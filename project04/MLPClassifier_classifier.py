import random

from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPClassifier


def mutationMLPClassifier(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        # solver
        individual[0] = random.choice(['lbfgs', 'sgd', 'adam'])
    elif numberParamer == 1:
        # random_state
        individual[1] = random.randint(0, 10000)
    elif numberParamer == 2:
        # warm_start
        individual[2] = random.choice([True, False])
    elif numberParamer == 3:
        # alpha
        individual[3] = random.uniform(0.00001, 0.01)
    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0


def MLPClassifierParametersFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)

    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = MLPClassifier(solver=individual[0], random_state=individual[1], warm_start=individual[2],
                              alpha=individual[3], tol=0.1)
    resultSum = 0
    for train, test in cv.split(df_norm, y):
        estimator.fit(df_norm[train], y[train])
        predicted = estimator.predict(df_norm[test])
        expected = y[test]
        tn, fp, fn, tp = metrics.confusion_matrix(expected, predicted).ravel()
        result = (tp + tn) / (
                tp + fp + tn + fn)  # w oparciu o macierze pomyłek
        # https://www.dataschool.io/simple-guide-to-confusion-matrix-terminology/
        resultSum = resultSum + result  # zbieramy wyniki z poszczególnych etapów walidacji krzyżowej

    return resultSum / split,


def MLPClassifierParameters(numberFeatures, icls):
    genome = list()

    # solver
    genome.append(random.choice(['lbfgs', 'sgd', 'adam']))

    # random_state
    genome.append(random.randint(0, 10000))

    # warm_start
    genome.append(random.choice([True, False]))

    # alpha
    genome.append(random.uniform(0.00001, 0.01))

    for _ in range(0, numberFeatures):
        genome.append(random.randint(0, 1))

    return icls(genome)
