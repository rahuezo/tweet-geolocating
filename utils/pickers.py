from random import randint


def generate_randoms(start, end, n=100, distinct=True): 
    randoms = []

    while len(randoms) < n: 
        random = randint(start, end)

        if distinct: 
            if end < n: 
                raise Exception("End parameter must be greater than n")

            if random not in randoms: 
                randoms.append(random)
                continue
        else: 
            randoms.append(random)
    return randoms


