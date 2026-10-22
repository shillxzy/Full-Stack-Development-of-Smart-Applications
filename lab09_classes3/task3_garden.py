"""Завдання 3. Класи Apple, AppleTree, Gardener."""


class Apple:
    states = ("Відсутнє", "Цвітіння", "Зелене", "Червоне")   # стадії дозрівання

    def __init__(self, index):
        self._index = index
        self._state = Apple.states[0]

    def grow(self):
        """Переводить яблуко на наступну стадію (якщо воно ще не дозріле)."""
        i = Apple.states.index(self._state)
        if i < len(Apple.states) - 1:
            self._state = Apple.states[i + 1]

    def is_ripe(self):
        return self._state == Apple.states[-1]

    def __repr__(self):
        return f"Яблуко №{self._index}: {self._state}"


class AppleTree:
    def __init__(self, count):
        self.apples = [Apple(i) for i in range(1, count + 1)]

    def grow_all(self):
        for apple in self.apples:
            apple.grow()

    def all_are_ripe(self):
        return all(apple.is_ripe() for apple in self.apples)

    def give_away_all(self):
        self.apples.clear()


class Gardener:
    def __init__(self, name, tree):
        self.name = name
        self._tree = tree

    def work(self):
        print(f"{self.name} доглядає за деревом...")
        self._tree.grow_all()

    def harvest(self):
        if not self._tree.apples:
            print("На дереві немає яблук")
            return False
        if self._tree.all_are_ripe():
            print(f"{self.name} зібрав(ла) урожай: {len(self._tree.apples)} яблук")
            self._tree.give_away_all()
            return True
        print("Попередження: яблука ще не дозріли!")
        return False

    @staticmethod
    def apple_base(apples):
        """Довідка: кількість яблук і ступінь стиглості кожного."""
        print(f"Кількість яблук: {len(apples)}")
        for apple in apples:
            print(" ", apple)


if __name__ == "__main__":
    loose = [Apple(i) for i in range(1, 4)]
    loose[1].grow()
    loose[2].grow(); loose[2].grow()
    Gardener.apple_base(loose)
    print()
    tree = AppleTree(5)
    gardener = Gardener("Марія", tree)
    gardener.work()
    Gardener.apple_base(tree.apples)
    while not gardener.harvest():
        gardener.work()
        Gardener.apple_base(tree.apples)
    print("Залишилось яблук на дереві:", len(tree.apples))
