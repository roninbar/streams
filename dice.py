import operator
from functools import partial
from itertools import accumulate, count, takewhile
from random import randrange

D = 6           # Number of die sides
N = 100_000   # Number of die rolls

zeros = partial(takewhile, operator.not_)

rolls: list[int] = [randrange(D) for i in range(N)]

total_rolls: list[list[int]] = [list(accumulate(map(lambda r: 1 if r == k else 0, rolls))) for k in range(D)]

required: list[int] = [
    max(len(list(zeros(total_rolls[k][j] - total_rolls[k][i] for j in range(i, N)))) for k in range(D))
    for i in range(N)]

print(sum(required) / len(required))