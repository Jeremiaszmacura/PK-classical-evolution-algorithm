import random

from sklearn import metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier


def mutationRandomForestClassifier(individual):
    numberParamer = random.randint(0, len(individual) - 1)
    if numberParamer == 0:
        # criterion
        individual[0] = random.choice(['gini', 'entropy', 'log_loss'])
    elif numberParamer == 1:
        # bootstrap
        individual[1] = random.choice([True, False])
    elif numberParamer == 2:
        # max_depth
        individual[2] = random.randint(2, 10)
    elif numberParamer == 3:
        # max_features
        individual[3] = random.choice(['sqrt', 'log2', None])
    elif numberParamer == 4:
        # random_state
        individual[4] = random.randint(0, 10000)
    else:  # genetyczna selekcja cech
        if individual[numberParamer] == 0:
            individual[numberParamer] = 1
        else:
            individual[numberParamer] = 0


def RandomForestClassifierParametersFitness(y, df, numberOfAtributtes, individual):
    split = 5
    cv = StratifiedKFold(n_splits=split)

    listColumnsToDrop = []  # lista cech do usuniecia
    for i in range(numberOfAtributtes, len(individual)):
        if individual[i] == 0:  # gdy atrybut ma zero to usuwamy cechę
            listColumnsToDrop.append(i - numberOfAtributtes)

    dfSelectedFeatures = df.drop(df.columns[listColumnsToDrop], axis=1, inplace=False)

    mms = MinMaxScaler()
    df_norm = mms.fit_transform(dfSelectedFeatures)
    estimator = RandomForestClassifier(criterion=individual[0], bootstrap=individual[1], max_depth=individual[2],
                                       max_features=individual[3], random_state=individual[4], n_estimators=10)
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


def RandomForestClassifierParameters(numberFeatures, icls):
    genome = list()

    # criterion
    genome.append(random.choice(['gini', 'entropy', 'log_loss']))

    # bootstrap
    genome.append(random.choice([True, False]))

    # max_depth
    genome.append(random.randint(2, 10))

    # max_features
    genome.append(random.choice(['sqrt', 'log2', None]))

    # random_state
    genome.append(random.randint(0, 10000))

    for _ in range(0, numberFeatures):
        genome.append(random.randint(0, 1))

    return icls(genome)
