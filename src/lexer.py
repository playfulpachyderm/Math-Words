import re
import math
from two_way_dict import TwoWayDict

def plus(a, b):     return a + b
def minus(a, b):    return a - b
def multiply(a, b): return a * b
def divide(a, b):   return a / b
def exp(a, b):      return a ** b

operators = [
    # reverse order of BEDMAS since evaluated recursively
    ("plus", plus),
    ("(?:minus)|(?:subtract)", minus),
    ("(?:times)|(?:multiplied by)", multiply),
    ("(?:divided by)|(?:over)", divide),
    ("(?:raised )?to the(?: power of)?", exp),
]

NUMBERS = TwoWayDict({
    "zero":     0,
    "one":      1,
    "two":      2,
    "three":    3,
    "four":     4,
    "five":     5,
    "six":      6,
    "seven":    7,
    "eight":    8,
    "nine":     9,
    "ten":      10,
    "eleven":   11,
    "twelve":   12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen":  15,
    "sixteen":  16,
    "seventeen":17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty":   20,
    "thirty":   30,
    "forty":    40,
    "fifty":    50,
    "sixty":    60,
    "seventy":  70,
    "eighty":   80,
    "ninety":   90,
})

MULTIPLIERS = TwoWayDict({
    "hundred":  100,
    "thousand": 1000,
    "million":  1000000,
    "billion":  1000000000,
    "trillion": 1000000000000,
})

NUMBERS.update(MULTIPLIERS)

def parse_number(s):
    nums = [NUMBERS[x] for x in s.split()]
    tokens = tokenize(nums)
    parts = [parse_token(token) * multiplier for multiplier, token in tokens.items()]
    return sum(parts)

def tokenize(nums):
    # tokenize by powers of 1000 (break into 3 digit parts)
    tokens = {}

    i = 0
    j = 0
    while j < len(nums):
        if nums[j] < 1000:
            j += 1
            continue
        if nums[j] in tokens.keys():
            raise ValueError("Multiple values for {}".format(nums[j]))
        tokens[nums[j]] = nums[i:j]
        j += 1
        i = j
    if i != j:
        tokens[1] = nums[i:j]
    return tokens

def parse_token(token):
    # sums the token, with one caveat
    if len(token) > 1 and token[1] == 100:
        # numbers before "hundred" are multiplied, like: "five hundred"
        token[0:2] = [token[0] * token[1]]
    return sum(token)

def reformat(s):
    # properly format input string
    s = s.lower().strip()
    for m in MULTIPLIERS:
        s = s.replace("{} and".format(m), str(m))

    return s

def evaluate(s):
    s = reformat(s)

    for o in operators:
        split = re.split(o[0], s)
        if len(split) > 1:
            return o[1](*[evaluate(x) for x in split])

    return parse_number(s)

def unparse(num):
    if num == 0:
        return NUMBERS[num]

    s = ""
    part = 0
    multiplier = 1
    while num > multiplier:
        part = num // multiplier % 1000
        s = unparse_part(part) + ("{} ".format(NUMBERS[multiplier]) if multiplier != 1 else "") + s
        multiplier *= 1000
    return s.strip()

def unparse_part(num):
    hundreds = num // 100
    num %= 100
    teen = num // 10 * 10
    if teen > 10:
        num %= 10
    else:
        teen = 0
    digit = num

    s = ""
    if hundreds:
        s = "{} hundred ".format(NUMBERS[hundreds])
    if teen:
        s += "{} ".format(NUMBERS[teen])
    if digit:
        s += "{} ".format(NUMBERS[digit])
    return s
