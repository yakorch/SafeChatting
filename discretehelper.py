# TODO: discrete class!
import string
from itertools import combinations
from typing import Union


class DiscreteChecker:

    @staticmethod
    def gcd(first: int, second: int, info: bool = False) -> Union[int, tuple]:
        """
        НСД | GCD
        param first: first number
        param second: second number
        param info: if True, returns as + bn = gcd(first, second) representation
        return: int (the greatest common divider) or tuple of as + bn
        >>> DiscreteChecker().gcd(14, 7)
        7
        >>> DiscreteChecker().gcd(19, 17)
        1
        >>> DiscreteChecker().gcd(125, 275)
        25
        >>> DiscreteChecker().gcd(13, 25, info=True) # means -1 * 25 + 2 * 13
        ((-1, 25), (2, 13))
        """
        one_coeff = [1, 0]
        two_coeff = [0, 1]

        if first == 0:
            if info:
                return (1, first), (0, second)
            return second
        elif second == 0:
            if info:
                return (1, first), (0, second)
            return first

        first, second = max([first, second]), min([first, second])
        first_copy = int(first)
        second_copy = int(second)
        previous_diff = second
        while True:
            diff = first % second
            if info:
                fraction = first // second
                one_coeff.append(one_coeff[-2] - fraction * one_coeff[-1])
                two_coeff.append(two_coeff[-2] - fraction * two_coeff[-1])
            first = second
            second = diff
            if diff == 0:
                if info:
                    return (one_coeff[-2], first_copy), (two_coeff[-2], second_copy)
                return previous_diff
            previous_diff = diff

    def euler_func(self, number: int) -> int:
        """
        φ(n) euler func - 
        param number: integer
        return: func value
        >>> DiscreteChecker().euler_func(19)
        18
        """
        res = 0
        for numb in range(1, number):
            if self.gcd(numb, number) == 1:
                res += 1
        return res

    def linear_equation(self, coeff: int, remainder: int, mod: int, verbose: bool = False) -> Union[int, list]:
        """
        Solves linear congruences.
        For example given 3x = 1 (mod 4), then x = 3 (mod 4)
        param coeff: coefficient near x
        param remainder: remainder, ostacha :)
        param mod: mod
        param verbose: does nothing
        return: x value
        >>> DiscreteChecker().linear_equation(2, 2, 5) # for 2x = 2 (mod 5)
        1
        >>> DiscreteChecker().linear_equation(1, 4, 5)
        4
        """
        gcds = [self.gcd(coeff, remainder), self.gcd(remainder, mod), self.gcd(coeff, mod)]
        if 1 not in gcds:
            if verbose:
                min_gcd = min(gcds)
                return [int(remainder / min_gcd), int(mod / min_gcd)]
            return int(remainder / min(gcds))
        coeff = coeff % mod
        opposite = self.gcd(coeff, mod, info=True)[1][0]
        res = remainder * opposite % mod
        if verbose:
            return [res, mod]
        return res

    def opposite_euclid(self, num, mod):
        """
        Find the inverse of the number modulo
        For example, to find opposite to 3 mod 5, use self.opposite_euclid(3, 5)
        param num: number
        param mod: mod
        return: x value
        >>> DiscreteChecker().opposite_euclid(3, 5)
        2
        >>> DiscreteChecker().opposite_euclid(2, 13)
        7
        """
        return self.linear_equation(num, 1, mod)

    @staticmethod
    def check_compatibility(bigger: list, smaller: list) -> bool:
        return bigger[0] % smaller[-1] == smaller[0]
        # return smaller[-2] * times == bigger[-2]

    @staticmethod
    def isclose(first: int, second: int, epsilon: float = 0.001) -> bool:
        return abs(first - second) < epsilon

    @staticmethod
    def is_perfect_square(number):
        return number in [i ** 2 for i in range(1, int(number ** 0.5) + 2)]

    @staticmethod
    def get_first_values(equation: list, number: int = 500) -> set:
        return {equation[-1] * i + equation[-2] for i in range(number)}

    def rid_same_eq(self, equations: list) -> Union[list, bool]:
        """Function uses magic to solve magic equations"""
        res = []
        mods = [el[-1] for el in equations]

        to_simplify = [item for item in combinations(mods, 2) if self.gcd(item[0], item[1]) != 1]
        all_mods_to_simpl = {el for item in to_simplify for el in item}
        except_simplify = set(mods).symmetric_difference(all_mods_to_simpl)

        for mod in except_simplify:
            find_it = [eq for eq in equations if eq[-1] == mod][0]
            res.append(find_it)
        for pair in to_simplify:
            gcd = self.gcd(pair[0], pair[1])
            bigger_one, smaller_one = max(pair), min(pair)
            first = [eq for eq in equations if eq[-1] == bigger_one][0]
            second = [eq for eq in equations if eq[-1] == smaller_one][0]
            if gcd == smaller_one:
                if self.check_compatibility(first, second):
                    if first not in res:
                        res.append(first)
                else:
                    return False
            else:
                original_sets = self.get_first_values(first) & self.get_first_values(second)
                # first try
                mod1 = int(first[-1] / gcd)
                new_first_1 = [first[0] % mod1, mod1]
                new_first_2 = [first[0] % gcd, gcd]
                first_try = self.get_first_values(new_first_1) & self.get_first_values(new_first_2)
                first_try &= self.get_first_values(second)
                makes_sense = True
                for elem in first_try:
                    if elem not in original_sets:
                        makes_sense = False
                if makes_sense is False:
                    # second try
                    makes_sense = True
                    mod2 = int(second[-1] / gcd)
                    new_second_1 = [second[0] % mod2, mod2]
                    new_second_2 = [second[0] % gcd, gcd]
                    second_try = self.get_first_values(new_second_1) & self.get_first_values(new_second_2)
                    second_try &= self.get_first_values(first)
                    new_r = [new_second_1, new_second_2, first]
                    for elem in second_try:
                        if elem not in original_sets:
                            makes_sense = False
                    if makes_sense is False:
                        new_r = [new_first_1, new_first_2, new_second_1, new_second_2]
                else:
                    new_r = [new_first_1, new_first_2, second]
                for item in new_r:
                    if item not in res:
                        res.append(item)
                for item in new_r:
                    for elem in new_r:
                        if item != elem:
                            if item[-1] == elem[-1] and item[-2] != elem[-2]:
                                return False
                return self.rid_same_eq(list(reversed(res)))
        return res

    def chinese_remain(self, equations: list) -> Union[tuple[int, int], str]:
        """
        Equation is a list of lists where each represent one equation.
        For example, to solve this system:
        3x = 5 (mod 14)
        3x = 2 (mod 11)
        5x = 11 (mod 12)
        Enter DiscreteChecker().chinese_remain([[3, 5, 14], [3, 2, 11], [5, 11, 12]])
        >>> DiscreteChecker().chinese_remain([[3, 5, 14], [3, 2, 11], [5, 11, 12]])
        Given equations are:
        3x = 5 (mod 14)
        3x = 2 (mod 11)
        5x = 11 (mod 12)
        <BLANKLINE>
        Simplified equations are:
        x = 8 (mod 11)
        a = 8, µ = 84, y = 8
        <BLANKLINE>
        x = 4 (mod 7)
        a = 4, µ = 132, y = 6
        <BLANKLINE>
        x = 7 (mod 12)
        a = 7, µ = 77, y = 5
        <BLANKLINE>
        Result:  x = 151 (mod 924)
        (151, 924)
        >>> DiscreteChecker().chinese_remain([[1, 1, 5], [1, 15, 27], [1, 6, 15]])
        Given equations are:
        1x = 1 (mod 5)
        1x = 15 (mod 27)
        1x = 6 (mod 15)
        <BLANKLINE>
        Simplified equations are:
        x = 1 (mod 5)
        a = 1, µ = 27, y = 3
        <BLANKLINE>
        x = 15 (mod 27)
        a = 15, µ = 5, y = 11
        <BLANKLINE>
        Result:  x = 96 (mod 135)
        (96, 135)
        """
        # x = SUM(yi * µi * ai)
        simplified_eq = []
        meow = 1
        res = 0
        print("Given equations are:")
        for eq in equations:
            print(f"{eq[0]}x = {eq[1]} (mod {eq[2]})")
            simple = self.linear_equation(eq[0], eq[1], eq[2], verbose=True)
            simplified_eq.append(simple)
        print()
        print(f"Simplified equations are:")
        helping = ""
        for eq in simplified_eq:
            helping += f"x = {eq[0]} (mod {eq[1]})\n"
        simplified_eq = self.rid_same_eq(simplified_eq)
        if simplified_eq is False:
            print(helping)
            print("No solutions exist")
            return "No solutions exist"
        for eq in simplified_eq:
            meow *= eq[-1]
        for eq in simplified_eq:
            print(f"x = {eq[0]} (mod {eq[1]})")
            meow_i = int(meow / eq[-1])
            a_i = eq[0]
            y_i = self.opposite_euclid(meow_i, eq[-1])
            print(f"a = {a_i}, µ = {meow_i}, y = {y_i}")
            res += meow_i * a_i * y_i
            print()
        print(f"Result:  x = {res % meow} (mod {meow})")
        return res % meow, meow

    @staticmethod
    def cesar_code(line: str, offset: int, lang: str = "en"):
        """
        line: string line
        param offset: k value in f(p) = p+k (mod alphabet_length)
        lang: "en" or "ua"
        return: ciphered line
        >>> DiscreteChecker().cesar_code("russkie are animals", 2, 'en')
        twuumkg ctg cpkocnu
        'twuumkg ctg cpkocnu'
        """
        if lang == "en":
            how = 27
            table = list(string.ascii_lowercase)
        elif lang == "ua":
            how = 34
            table = ["а", "б", "в", "г", "ґ", "д", "е", "є",
                     "ж", "з", "и", "і", "ї", "й", "к", "л", "м", "н", "о", "п",
                     "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я"]
        new_l = ""
        for ind in range(len(line)):
            elem = line[ind]
            if elem != " ":
                new_l += table[(table.index(elem) + offset) % (how - 1)]
            else:
                new_l += " "
        print(new_l)
        return new_l


# DiscreteChecker().chinese_remain([[3, 5, 14], [3, 2, 11], [5, 11, 12]])
# DiscreteChecker().chinese_remain([[3, 16, 20], [2, 4, 8], [5, 2, 7]])
# DiscreteChecker().chinese_remain([[3, 8, 20], [5, 8, 9], [4, 1, 21]])
# DiscreteChecker().chinese_remain([[1, 1, 5], [1, 15, 27], [1, 6, 15]])


helper = DiscreteChecker()

# print(helper.gcd())

# print(helper.linear_equation(96, 38, 125))
# print(helper.opposite_euclid())

# print(helper.chinese_remain([[1, 12, 17], [1, 11, 21], [1, 10, 29]]))
# print(helper.euler_func())
# print((99**3 % 32)**3 % 15)