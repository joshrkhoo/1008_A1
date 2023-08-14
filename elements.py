from __future__ import annotations

from enum import auto
from typing import Optional

from base_enum import BaseEnum

from data_structures.referential_array import ArrayR

class Element(BaseEnum):
    """
    Element Class to store all different elements as constants, and associate indicies with them.

    Example:
    ```
    print(Element.FIRE.value)         # 1
    print(Element.GRASS.value)        # 3

    print(Element.from_string("Ice")) # Element.ICE
    ```
    """

    FIRE = auto() #1
    WATER = auto() #2
    GRASS = auto() #3
    BUG = auto() #4
    DRAGON = auto() #5
    ELECTRIC = auto() #6
    FIGHTING = auto() #7
    FLYING = auto()
    GHOST = auto()
    GROUND = auto()
    ICE = auto()
    NORMAL = auto()
    POISON = auto()
    PSYCHIC = auto()
    ROCK = auto()
    FAIRY = auto()
    DARK = auto()
    STEEL = auto()

    @classmethod
    def from_string(cls, string: str) -> Element:
        for elem in Element:
            if elem.name.lower() == string.lower():
                return elem
        raise ValueError(f"Unexpected string {string}")

class EffectivenessCalculator:
    """
    Helper class for calculating the element effectiveness for two elements.

    This class follows the singleton pattern.

    Usage:
        EffectivenessCalculator.get_effectiveness(elem1, elem2)
    """

    # Optional[EffectivenessCalculator] is a type hint that says that this variable can be either None or an EffectivenessCalculator
    # instance is a class variable that stores the singleton instance of EffectivenessCalculator
    instance: Optional[EffectivenessCalculator] = None

    def __init__(self, element_names: ArrayR[str], effectiveness_values: ArrayR[float]) -> None:
        """
        Initialise the Effectiveness Calculator.

        The first parameter is an ArrayR of size n containing all element_names.
        The second parameter is an ArrayR of size n*n, containing all effectiveness values.
            The first n values in the array is the effectiveness of the first element
            against all other elements, in the same order as element_names.
            The next n values is the same, but the effectiveness of the second element, and so on.

        Example:
        element_names: ['Fire', 'Water', 'Grass']
        effectivness_values: [0.5, 0.5, 2, 2, 0.5, 0.5, 0.5, 2, 0.5]
        Fire is half effective to Fire and Water, and double effective to Grass [0.5, 0.5, 2]
        Water is double effective to Fire, and half effective to Water and Grass [2, 0.5, 0.5]
        Grass is half effective to Fire and Grass, and double effective to Water [0.5, 2, 0.5]
        """


        #ArrayR of size n containing all element_names
        self.element_names = element_names

        #ArrayR of size n*n, containing all effectiveness values
        self.effectiveness_values = effectiveness_values



                                        ##### COMPLEXITY ANALYSIS #####
        # INCLUDING COST OF COMPARION: 
            # The time complexity of the map below is O(n * (x * y)) where n is the number of elements in the element_names array, x is the number of enum values in the Element class, and y is the cost of comparison between the two strings in the from_string method 
        
        # EXCLUDING COST OF COMPARISON:
            # The time complexity of the map below is O(n * x) where n is the number of elements in the element_names array and x is the number of enum values in the Element class

        # NOTE: The complexity of this map is inefficient however it will only be this complexity once which is better than having to run O(n) time complexity every time we want to get the effectiveness value
    
        # This complexity however will occur ONCE AND ONLY ONCE as we are essentially creating a map that maps the index of the element to the index of the effectivenes which allows the get_effectiveness function to be O(1) time complexity (see below for more details)

                                        ##### COMPLEXITY ANALYSIS #####


        print(self.element_names, effectiveness_values)
    
        # This is a map that maps the index of the element to the index of the effectiveness value
        # [element enum value] -> [index of element name value in element_names array]
        self.element_index_map = ArrayR(len(self.element_names))
        for i in range(len(self.element_names)):

            # set the index of the element to the index of the element name in the element_names array
                # this is done by the from_string method which returns the element enum value
            self.element_index_map[Element.from_string(self.element_names[i]).value-1] = i
        print(self.element_index_map)

    @classmethod
    def get_effectiveness(cls, type1: Element, type2: Element) -> float:
        """
        Returns the effectivness of elem1 attacking elem2.

        Example: EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER) == 0.5
        """

        # What is instance? 
            # It is the only EffectivenessCalculator object, which has two attributes: element_names and effectiveness_values
            # element_names is an ArrayR of size n containing all element_names
            # effectiveness_values is an ArrayR of size n*n, containing all effectiveness values

        # The effectiveness_values array is a 2D array... we need to convert it into a 1D array using the formula: row * num_cols + col
            # This allows us to get the index of the effectiveness value directly without having to loop through the array


        ####### COMPLEXITY ANALYSIS #######
        # The time complexity of this function is O(1) 
            # This is because we are getting the effectiveness value by index directly
                # The calculation is done by using mathematical operations which are all O(1) time complexity
                # There are no loops to iterate through and thus no O(n) time complexity where n would be the number of elements in the array of effectiveness values
        ####### COMPLEXITY ANALYSIS #######


        
        # Assigning cls.instance to a variable called instance
            # This allows us to access the instance/object of EffectivenessCalculator
            # cls.instance is an object with two attributes: element_names and effectiveness_values that are managed in the from_csv function
        instance = cls.instance

        # # Here we are getting the array of effectives values from the instance variable
        effectiveness_values = instance.effectiveness_values

        # Here we are getting the index of the effectiveness value of type1 attacking type2 in the effectiveness_values array
            # This is done by using the formula: row * num_cols + col
            # .value returns the index of the element
                # this method comes from the BaseEnum class which is a child class of Enum 
            # type1.value-1 is used because the index of the enums is 1-indexed and the index of the mapped array is 0-indexed
        index_of_effectiveness_value = instance.element_index_map[type1.value-1] * len(instance.element_names) + instance.element_index_map[type2.value-1]


        # # Here we are getting the effectiveness value by index
        effectiveness = effectiveness_values[index_of_effectiveness_value]
        print(len(instance.element_names), type1, type2, type1.value, type2.value, instance.element_index_map[type1.value-1], instance.element_index_map[type2.value-1], index_of_effectiveness_value, effectiveness)

        return effectiveness



    @classmethod
    def from_csv(cls, csv_file: str) -> EffectivenessCalculator:
        # NOTE: This is a terrible way to open csv files, if writing your own code use the `csv` module.
        # This is done this way to facilitate the second half of the task, the __init__ definition.

        """
        This function is basically spliting the csv file into two parts: header and rest
        header is the first line of the csv file (the element names)
        rest is the rest of the csv file (the effectiveness values)
        """
        
        with open(csv_file, "r") as file:
            header, rest = file.read().strip().split("\n", maxsplit=1)
            header = header.split(",")
            rest = rest.replace("\n", ",").split(",")
            a_header = ArrayR(len(header))
            a_all = ArrayR(len(rest))
            for i in range(len(header)):
                a_header[i] = header[i]
            for i in range(len(rest)):
                a_all[i] = float(rest[i])
            return EffectivenessCalculator(a_header, a_all)
        

    # Over here we just make an instance of the class where it has the element names and effectiveness values as attributes
    @classmethod
    def make_singleton(cls):
        cls.instance = EffectivenessCalculator.from_csv("type_effectiveness.csv")

EffectivenessCalculator.make_singleton()


if __name__ == "__main__":
    print(EffectivenessCalculator.get_effectiveness(Element.ELECTRIC, Element.WATER))
