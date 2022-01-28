import Group


def a_x_b(a, b) -> list:
    """
    Returns a list of the (a, b)'s

    :param a: a group or a list of numbers
    :param b: a group or list of numbers
    :return:
    """
    a = list(range(a)) if type(a) == int else a.g
    b = list(range(b)) if type(b) == int else b.g

    return [(i, j) for i in a for j in b]


def a_x_b_rule(a: Group, b: Group) -> str:
    """
    This generates the rule of aXb from the groups'
    rule.

    :param a: group a
    :param b: group b
    :return: rule as str
    """
    a_rule = a.rule.format('{0[0]}', '{1[0]}')
    b_rule = b.rule.format('{0[1]}', '{1[1]}')
    return '({}, {})'.format(a_rule, b_rule)


def a_x_b_dictionary(a: Group, b: Group) -> dict:
    """
    This method takes all mappings for two groups, and
    transforms them into a dictionary.

    :param a: Group or int
    :param b: Group or int
    :return: dictionary of all rule mapping
    """
    a_b = a_x_b(a, b)
    rules = {}
    for x in a_b:
        for y in a_b:
            n_a = a.apply_rule(x[0], y[0])
            n_b = b.apply_rule(x[1], y[1])
            new_t = (n_a, n_b)
            res = '({}, {})({}, {})'.format(x[0], x[1], y[0], y[1], new_t)

            if res not in rules:
                rules[res] = new_t

    return rules


def a_x_b_group(a: Group, b: Group, rule_based: bool = True) -> Group:
    """
    This returns the direct product group from two groups.

    :param a: group a
    :param b: group b
    :param rule_based: whether to create rule-based group or dictionary-based
    :return: Group of aXb
    """
    if rule_based:
        n_rule = a_x_b_rule(a, b)
        n_set = a_x_b(a, b)
        n_e = (a.e, b.e)
        return Group.Group(g=n_set, rule=n_rule, e=n_e)
    else:
        pass


def group_from_cayley(file: str, sep: str = '\t'):
    with open(file, 'r') as f:
        g = [l.strip() for l in f.readline().split(sep)]

        d = {}
        for a in g:
            a_t = [l.strip() for l in f.readline().split(sep)]
            if not a_t:
                raise IndexError("Make sure header row matches columns.")
            for i, b in enumerate(g):
                d[f'{b}*{a}'] = a_t[i]
    G = Group.Group(g=g, rule="{0}*{1}")
    G.dictionary_rule(d)
    return G


if __name__ == '__main__':
    Z_2 = Group.Group(g=2, rule='m', e=1)
    Z_4 = Group.Group(g=4, rule='m', e=1)
    Z_2XZ_4 = a_x_b_group(Z_2, Z_4)
    Z_2XZ_4.cayley_table()
    Z_2XZ_4.units_table()
