import re
import math
from .two_way_dict import TwoWayDict

def plus(a, b):     return a + b
def minus(a, b):    return a - b
def multiply(a, b): return a * b
def divide(a, b):   return a / b
def exp(a, b):      return a ** b

ARBITRARY_AMOUNT = 5  # arbitrarily chose five decimal places

unary_operators = [
    ("(?:natural )?log(?:arithm)?", lambda x: math.log(x)),  # no second arg
    ("common log(?:arithm)?", math.log10),
    #TODO: possibly add support for logs with arbitrary base?
    ("sine?", math.sin),
    ("cos(?:ine)?", math.cos),
    ("tan(?:gent)?", math.tan),
    ("(?:square )?root", math.sqrt)
]

binary_operators = [
    # reverse order of BEDMAS since evaluated recursively
    ("(?:plus)|(?:added to)", plus),
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
    "hundred":      100,
    "thousand":     1000,
    "million":      1000000,
    "billion":      1000000000,
    "trillion":     1000000000000,
    "quadrillion":  1000000000000000,
    "quintillion":  1000000000000000000,
    "sextillion":   1000000000000000000000,
    "septillion":   1000000000000000000000000,
    "octillion":    1000000000000000000000000000,
    "nonillion":    1000000000000000000000000000000,
    "decillion":    1000000000000000000000000000000000,
    # ...
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

def helper(num):
    # helper for the parse_token method
    if num == 0:
        # in accordance with numbers like "thirty zero", 0 is a 1's digit
        return 0
    return math.floor(math.log10(num))

def parse_token(token):
    # sums the token, with one caveat for 100s
    if len(token) > 1 and token[1] == 100:
        # numbers before "hundred" are multiplied, like: "five hundred"
        token[0:2] = [token[0] * token[1]]

    # there should be at most 3 digits
    if len(token) > 3:
        raise ValueError

    # digits should be presented in order
    if token != sorted(token, reverse = True):
        raise ValueError

    # check for duplicate digits like "forty thirty" or "three five"
    mirror = [helper(t) for t in token]
    if len(mirror) != len(set(mirror)):  # contains duplicates
        raise ValueError

    return sum(token)

def reformat(s):
    # properly format input string
    s = s.lower().strip()
    for m in MULTIPLIERS:
        s = s.replace("{} and".format(m), str(m))

    # we don't enforce "proper" use of "a" vs "an" because people can have accents
    s = re.sub("\\ban?\\b", "one", s)

    return s

def parse(s):
    s = reformat(s)

    for o in binary_operators:
        split = re.split(o[0], s, maxsplit = 1)
        if len(split) > 1:  # found an occurrence
            return o[1](*[parse(x) for x in split])

    for o in unary_operators:
        split = re.split("^(?:the )?{regex}(?: of)?".format(regex = o[0]), s, maxsplit = 1)
        if len(split) > 1:  # found one
            return o[1](parse(split[1]))

    return parse_number(s)

def unparse(num):
    if num < 0:
        return "negative {}".format(unparse(-num))

    whole_part = int(num)
    frac_part = round(num - whole_part, ARBITRARY_AMOUNT)
    s = ""

    if whole_part == 0:
        s = "{} ".format(NUMBERS[whole_part])

    part = 0
    multiplier = 1
    while whole_part >= multiplier:
        part = whole_part // multiplier % 1000
        if part:
            prepend = unparse_part(part) + ("{} ".format(NUMBERS[multiplier]) if multiplier != 1 else "")
            s = prepend + s
        multiplier *= 1000

    if frac_part:
        s += "point "
        for i in str(frac_part).split(".")[-1]:
            s += "{} ".format(NUMBERS[int(i)])

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

# convenience method
# although to attain true Mathwords, this should be the only visible method
def evaluate(s):
    return unparse(parse(s))
