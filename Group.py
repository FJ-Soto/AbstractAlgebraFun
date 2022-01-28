import math
from itertools import combinations


class Group:
    """
    This class encloses a finite set.
    It includes typical group methods such as
    Cayley and Units table, D4, D3, and subgroups.
    """

    def __init__(self, g, rule, e=None):
        if rule == 'u':
            self.g = [i for i in range(g) if math.gcd(i, g) == 1]
            self._rule = rule = f'({{0}}*{{1}})%{g}'
        else:
            self.g = g
        self.rule = rule
        self.__spacing = len(str(max(g))) if type(g) == list else len(str(g))
        self.__dictionary = None
        self.e = e

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, val):
        if type(val) == int:
            val = list(range(val))
        self._g = val

    @property
    def rule(self) -> str:
        """
        Returns the current rule
        :return: rule as string
        """
        return self._rule

    @rule.setter
    def rule(self, rule: str = 'a'):
        """
        Sets the rule for the group.
        Some pre-included rules include:\n
        'a' -   add (a+b)%n \n
        'm' -   multiply (a*b)%n \n
        'u' -   units of Z_n under mult. mod (n) \n
        The rules should have placeholders {0} = a and {1} = b

        :param rule: rule as string
        """
        if rule == 'a':
            rule = f'({{0}}+{{1}})%{len(self.g)}'
        elif rule == 'm':
            rule = f'({{0}}*{{1}})%{len(self.g)}'
        self._rule = rule

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, e):
        self._e = e

    def dictionary_rule(self, dictionary):
        """
        This sets the rule to be of type dictionary
        That is: the 'key' is the operation and the value is the match.\n
        EX: if a+b = b, dictionary['a+b']=b would be an entry.\n
        NOTE: The rule for the above would be '{0}+{1}'.

        :param dictionary: containing rules to look up
        """
        self.__dictionary = dictionary

    def is_group(self):
        # needs to be associative
        # needs an identity
        # needs to be closed

        hasId = self.e or self.find_identity()
        isAssociative = self.is_associative()
        isClosed = self.is_closed()
        return hasId and isAssociative and isClosed

    def is_closed(self):
        for i in self.g:
            for j in self.g:
                res = self.apply_rule(j, i)

                if res not in self.g:
                    return False

        return True

    def is_associative(self):
        for a in self.g:
            for b in self.g:
                for c in self.g:
                    left_first = self.apply_rule(a, b)
                    left_result = self.apply_rule(left_first, c)

                    right_first = self.apply_rule(b, c)
                    right_result = self.apply_rule(a, right_first)

                    if left_result != right_result:
                        return False

        return True

    def is_commutative(self):
        for a in self.g:
            for b in self.g:
                left_first = self.apply_rule(a, b)

                right_first = self.apply_rule(b, a)

                if left_first != right_first:
                    return False

        return True

    def find_identity(self, set_e: bool = False) -> list:
        """
        Brute force approach to finding an identity element under the rule.
        Return of type list in the case that the set is not a group.
        :param set_e: whether to set e to what is found
        :return: list containing identity elements in the set
        """
        pos_id = {}
        for curr_id in self.g:
            for i, x in enumerate(self.g):
                res1 = self.apply_rule(x, curr_id)
                res2 = self.apply_rule(curr_id, x)
                if res1 != res2:
                    break
                if res1 == res2 == x and i == len(self.g) - 1:
                    if curr_id not in pos_id:
                        pos_id[curr_id] = True

        if pos_id and set_e:
            self.e = list(pos_id.keys())[0]

        return list(pos_id.keys())

    def apply_rule(self, a, b):
        if self.__dictionary is None and type(self.rule) == str:
            return eval(self.rule.format(a, b))
        else:
            return self.__dictionary[self.rule.format(a, b)]

    def cayley_table(self):
        """
        Prints the Cayley Table for the set
        """
        print('{:^{}}|'.format('*', self.__spacing), end=" ")
        for i in self.g:
            print('{0:>{1}}'.format(str(i), self.__spacing), end=" ")

        print()
        print("-" * (self.__spacing + 1) * (len(self.g) + 1))

        for i in self.g:
            print('{:>{}}|'.format(str(i), self.__spacing), end=" ")

            for j in self.g:
                res = self.apply_rule(j, i)
                print('{:>{}}'.format(str(res), self.__spacing), end=" ")
            print()
        print()

    def units(self) -> list:
        """
        Determines if the rule maps to the sets identity.
        :return: list of units
        """
        if self.e is None:
            raise NoIdentityException()

        if self.rule == 'u':
            return self.g

        units = []
        for i in self.g:
            for j in self.g:
                res = self.apply_rule(j, i)

                if res == self.e:
                    units.append(i)

        return list(set(units))

    def units_table(self):
        """
        Prints the Cayley Table with only the units
        """
        units = self.units()
        spacing = len(str(max(units)))
        print('{:^{}}|'.format('*', spacing), end=" ")
        for i in units:
            print('{:{}}'.format(str(i), spacing), end=" ")

        print()
        print("-" * (spacing + 1) * (len(units) + 1))

        for i in units:
            print('{:{}}|'.format(str(i), spacing), end=" ")

            for j in units:
                res = self.apply_rule(j, i)

                print('{:{}}'.format(str(res), spacing), end=" ")
            print()
        print()

    def subgroups(self) -> list:
        """
        WARNING: HIGHLY INEFFICIENT.

        :return: list of all subgroups of the group.
        """
        subs = {}

        # identity
        subs[str([self.e or self.find_identity()[0]])] = True
        subs[str(self.g)] = True

        for i in range(1, len(self.g) + 1):
            for s in combinations(self.g, i):
                t_g = list(s)
                t = Group(g=t_g, rule=self.rule)
                t.dictionary_rule(self.__dictionary)
                if str(t_g) not in subs:
                    if t.is_group():
                        subs[str(t_g)] = True

        return list(subs.keys())

    def a_n(self, a, sort=False):
        if a not in self.g:
            raise NotInGroupException()

        a_n_s = {self.e: self.e}
        if a not in a_n_s:
            a_n_s[a] = a
        prev = a
        while True:
            prev = self.apply_rule(prev, a)
            if prev in a_n_s:
                break
            else:
                a_n_s[prev] = prev

        return sorted(list(a_n_s.keys())) if sort else list(a_n_s.keys())

    def cyclic_groups(self, display=False) -> dict:
        cycs = {}
        for element in self.g:
            res = self.a_n(element)
            if set(res) == set(self.g):
                cycs[element] = res

            if display:
                print(element, res)

        return cycs

    def dis_subs(self):
        cycs = {}
        for element in self.g:
            res = self.a_n(element)
            if set(res) == set(self.g):
                if len(res) in cycs:
                    cycs[res] = cycs[res]
                else:
                    cycs[len(res)] = [element]
        return cycs


    def has_generator(self):
        return bool(self.cyclic_groups())

    def centers(self) -> list:
        centers = []

        for a in self.g:
            works = True
            for b in self.g:
                if self.apply_rule(a, b) != self.apply_rule(b, a):
                    works = False
                    break

            if works:
                centers.append(a)

        return centers

    def centralizers(self) -> dict:
        cent_dict = {}
        for a in self.g:
            a_cent = []
            for b in self.g:
                if self.apply_rule(a, b) == self.apply_rule(b, a):
                    a_cent.append(b)
            cent_dict[a] = a_cent

        return cent_dict


class NoIdentityException(Exception):
    def __init__(self, message="Identity element does not exists or is not set."):
        super().__init__(message)


class NotInGroupException(Exception):
    def __init__(self, message="Element is not in the set."):
        super().__init__(message)


# SPECIAL GROUPS: D4, D3
D4_dict = {'r0*r0': 'r0', 'r1*r0': 'r1', 'r2*r0': 'r2', 'r3*r0': 'r3', 'r0*r1': 'r1', 'r1*r1': 'r2', 'r2*r1': 'r3',
           'r3*r1': 'r0', 'r0*r2': 'r2', 'r1*r2': 'r3', 'r2*r2': 'r0', 'r3*r2': 'r1', 'r0*r3': 'r3', 'r1*r3': 'r0',
           'r2*r3': 'r1', 'r3*r3': 'r2', 'r0*m1': 'm1', 'r1*m1': 's1', 'r2*m1': 'm2', 'r3*m1': 's2', 'r0*m2': 'm2',
           'r1*m2': 's2', 'r2*m2': 'm1', 'r3*m2': 's1', 'r0*s1': 's1', 'r1*s1': 'm2', 'r2*s1': 's2', 'r3*s1': 'm1',
           'r0*s2': 's2', 'r1*s2': 'm1', 'r2*s2': 's1', 'r3*s2': 'm2', 'm1*r0': 'm1', 'm2*r0': 'm2', 's1*r0': 's1',
           's2*r0': 's2', 'm1*r1': 's2', 'm2*r1': 's1', 's1*r1': 'm1', 's2*r1': 'm2', 'm1*r2': 'm2', 'm2*r2': 'm1',
           's1*r2': 's2', 's2*r2': 's1', 'm1*r3': 's1', 'm2*r3': 's2', 's1*r3': 'm2', 's2*r3': 'm1', 'm1*m1': 'r0',
           'm2*m1': 'r2', 's1*m1': 'r1', 's2*m1': 'r3', 'm1*m2': 'r2', 'm2*m2': 'r0', 's1*m2': 'r3', 's2*m2': 'r1',
           'm1*s1': 'r3', 'm2*s1': 'r1', 's1*s1': 'r0', 's2*s1': 'r2', 'm1*s2': 'r1', 'm2*s2': 'r3', 's1*s2': 'r2',
           's2*s2': 'r0'}

D4_set = ['r0', 'r1', 'r2', 'r3', 'm1', 'm2', 's1', 's2']
D4 = Group(g=D4_set, rule='{1}*{0}', e='r0')
D4.dictionary_rule(D4_dict)

D3_dict = {'r0*r0': 'r0', 'r1*r0': 'r1', 'r2*r0': 'r2', 'm1*r0': 'm1', 'm2*r0': 'm2', 'm3*r0': 'm3', 'r0*r1': 'r1',
           'r1*r1': 'r2', 'r2*r1': 'r0', 'm1*r1': 'm3', 'm2*r1': 'm1', 'm3*r1': 'm2', 'r0*r2': 'r2', 'r1*r2': 'r0',
           'r2*r2': 'r1', 'm1*r2': 'm2', 'm2*r2': 'm3', 'm3*r2': 'm1', 'r0*m1': 'm1', 'r1*m1': 'm2', 'r2*m1': 'm3',
           'm1*m1': 'r0', 'm2*m1': 'r1', 'm3*m1': 'r2', 'r0*m2': 'm2', 'r1*m2': 'm3', 'r2*m2': 'm1', 'm1*m2': 'r2',
           'm2*m2': 'r0', 'm3*m2': 'r1', 'r0*m3': 'm3', 'r1*m3': 'm1', 'r2*m3': 'm2', 'm1*m3': 'r1', 'm2*m3': 'r2',
           'm3*m3': 'r0'}

D3_set = ['r0', 'r1', 'r2', 'm1', 'm2', 'm3']
D3 = Group(g=D3_set, rule='{1}*{0}', e='r0')
D3.dictionary_rule(D3_dict)

if __name__ == '__main__':
    pass
