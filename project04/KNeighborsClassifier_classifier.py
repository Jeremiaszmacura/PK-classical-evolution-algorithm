import random

from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier


def mutationKNeighborsClassifier(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        # n_neighbors
        individual[0] = random.randint(1, 10)
    elif numberParamer == 1:
        # weights
        individual[1] = random.choice(['uniform', 'distance'])
    elif numberParamer == 2:
        # algorithm
        individual[2] = random.choice(['auto', 'ball_tree', 'kd_tree', 'brute'])
    elif numberParamer == 3:
        # leaf_size
        individual[3] = random.randint(10, 50)
    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0


def KNeighborsClassifierParametersFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)

    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = KNeighborsClassifier(n_neighbors=individual[0], weights=individual[1], algorithm=individual[2],
                                     leaf_size=individual[3])
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


def KNeighborsClassifierParameters(numberFeatures, icls):
    genome = list()

    # n_neighbors
    genome.append(random.randint(1, 10))

    # weights
    genome.append(random.choice(['uniform', 'distance']))

    # algorithm
    genome.append(random.choice(['auto', 'ball_tree', 'kd_tree', 'brute']))

    # leaf_size
    genome.append(random.randint(10, 50))

    for _ in range(0, numberFeatures):
        genome.append(random.randint(0, 1))

    return icls(genome)
