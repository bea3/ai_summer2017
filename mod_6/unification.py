import tokenize
from StringIO import StringIO

'''
IMPORTANT NOTES:
* constants - values and predicates
    * values start with uppercase letter (Fred)
    * predicates use lowercase letters (loves)
* variables - lowercase and start with ? (?x)
* expressions (lists) - these use the S-expression syntax
'''


def atom(next, token):
    if token[1] == '(':
        out = []
        token = next()
        while token[1] != ')':
            out.append(atom(next, token))
            token = next()
            if token[1] == ' ':
                token = next()
        return out
    elif token[1] == '?':
        token = next()
        return "?" + token[1]
    else:
        return token[1]


def parse(exp):
    src = StringIO(exp).readline
    tokens = tokenize.generate_tokens(src)
    return atom(tokens.next, tokens.next())


def is_variable(exp):
    return isinstance(exp, str) and exp[0] == "?"


def is_constant(exp):
    return isinstance(exp, str) and not is_variable(exp)


def apply(result, exp1, exp2):
    if result != "{}":
        symbols = result.split('/')
        symbols = [symbols[0].replace('{', ''), symbols[1].replace('}', '')]

        for n, i in enumerate(exp2):
            if i == symbols[0]:
                exp2[n] = symbols[1]
    return exp1, exp2


def unify(s_expression1, s_expression2):
    return unification(parse(s_expression1), parse(s_expression2))


def unification(list_expression1, list_expression2):
    if (is_constant(list_expression1) and is_constant(list_expression2)) or (
            len(list_expression1) == 0 and len(list_expression2) == 0):
        if list_expression1 == list_expression2:
            return "{}"
        else:
            return "FAIL"
    elif is_variable(list_expression1):
        if list_expression1 in list_expression2:
            return "FAIL"
        else:
            return "{" + str(list_expression1) + "/" + str(list_expression2) + "}"
    elif is_variable(list_expression2):
        if list_expression2 in list_expression1:
            return "FAIL"
        else:
            return "{" + str(list_expression2) + "/" + str(list_expression1) + "}"

    if type(list_expression1) is list:
        first1 = list_expression1.pop(0)
    else:
        first1 = list_expression1

    if type(list_expression2) is list:
        first2 = list_expression2.pop(0)
    else:
        first2 = list_expression2

    result1 = unification(first1, first2)
    if result1 == "FAIL":
        return "FAIL"

    list_expression1, list_expression2 = apply(result1, list_expression1, list_expression2)

    result2 = unification(list_expression1, list_expression2)
    if result2 == "FAIL":
        return "FAIL"

    return result1 + " " + result2


def prettify_result(exp):
    if exp != "FAIL":

        exp = exp.replace('\'', '')
        exp = exp.split("}")
        nonempty = []
        results = dict()

        for i in exp:
            if i != "{}":
                nonempty.append(i)

        for i in nonempty:
            exp = i.replace('{', '')
            exp_list = exp.split('/')
            if len(exp_list) == 2:
                value = exp_list[1].strip()
                value = value.replace('[', '(')
                value = value.replace(']', ')')
                value = value.replace(',', ':')
                results[exp_list[0].strip()] = value
        return results
    else:
        return "FAIL"


def clean_exp(exp1, exp2):
    exp1 = exp1.replace("-", "_")
    exp2 = exp2.replace("-", "_")
    return exp1, exp2


exp1 = "(son Barney Bam-Bam)"
exp2 = "(son ?y (son Barney))"
exp1, exp2 = clean_exp(exp1, exp2)
stuff = unify(exp1, exp2)
print (prettify_result(stuff))
