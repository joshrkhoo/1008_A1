import abc
import math
from data_structures.array_sorted_list import ArraySortedList

from data_structures.referential_array import ArrayR
from data_structures.sorted_list_adt import ListItem
from data_structures.stack_adt import ArrayStack

class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):

    def __init__(self, attack, defense, speed, max_hp) -> None:
        # TODO: Implement
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp


    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp

class ComplexStats(Stats):

    def __init__(
        self,
        attack_formula: ArrayR[str],
        defense_formula: ArrayR[str],
        speed_formula: ArrayR[str],
        max_hp_formula: ArrayR[str],
    ) -> None:
        # TODO: Implement
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula




    def get_attack(self, level: int):
        return int(self.evaluate_expression(self.attack_formula, level))

    def get_defense(self, level: int):
        return int(self.evaluate_expression(self.defense_formula, level))

    def get_speed(self, level: int):
        return int(self.evaluate_expression(self.speed_formula, level))
    
    def get_max_hp(self, level: int):
        return int(self.evaluate_expression(self.max_hp_formula, level))
    
    def evaluate_expression(self, formula, level: int):
        stack = ArrayStack(len(formula))

        for element in formula:
            # print(stack)
            try:
                stack.push(float(element))          
            except ValueError:
                if element == "+":
                    stack.push(stack.pop() + stack.pop())
                elif element == "-":
                    first = stack.pop()
                    second = stack.pop()
                    stack.push(second - first)
                elif element == "*":
                    first = stack.pop()
                    second = stack.pop()
                    stack.push(second * first)
                elif element == "sqrt":
                    stack.push(math.sqrt(stack.pop()))
                elif element == "middle":
                    # find the median of the numbers in the stack
                    sortedArray = ArraySortedList(3)
                    for i in range(3):
                        val = stack.pop()
                        sortedArray.add(ListItem(val, val))
                    stack.push(sortedArray[1].key)
                elif element == "level":
                    stack.push(level)
                elif element == "power":
                    first = stack.pop()
                    second = stack.pop()
                    stack.push(second ** first)
        return stack.pop()

                

        
            


    
    


