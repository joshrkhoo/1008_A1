from __future__ import annotations
import abc
import math
from elements import EffectivenessCalculator

from stats import Stats

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        
        self.simple_mode = simple_mode
        self.level = level

        # set that the monster is not ready to evolve (lvl needs be different to original)
        self.evolve_ready = False

        # if we are in simple mode then we use simplestats
        if simple_mode:
            self.stats = self.get_simple_stats()
        
        # otherwise we use complexstats
        else:
            self.stats = self.get_complex_stats()

        # set the current hp to the max hp (this hp will change when the monster loses hp)
        # we dont call stats because there may be new monsters created that are not in the stats file
            # this could be child classes (variations of the same monster / parent class)
        self.hp = self.get_max_hp()

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""

        difference = self.get_max_hp() - self.get_hp()


        self.level = self.level + 1

        self.set_hp(self.get_max_hp() - difference)

        # level changed so 1 requirement of evolution is met
        self.evolve_ready = True

    def get_hp(self):
        """Get the current HP of this monster instance"""

        # here we just return self.hp because this one is dynamic (it changes depending if it loses hp or not) 
        # As assigned in init
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""

        #we just set the hp to the value passed in
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.stats.get_attack()

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.stats.get_defense()

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.stats.get_speed()

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""

        # we call the stats.get_max_hp() method as it is always the same for that monster instance
        return self.stats.get_max_hp()
    
    def alive(self) -> bool:
        """Whether this monster instance is alive"""
        # if the current hp is greater than 0 then the monster is alive
        return self.hp > 0
  


    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP

        if other.get_defense < self.get_attack / 2:
            damage = self.get_attack - other.get_defense
        elif other.get_defence < self.get_attack:
            damage = self.get_attack * 5/8 - other.get_defense / 4
        else:
            damage = self.get_attack / 4

        effective_damage = damage * EffectivenessCalculator.get_effectiveness(self.get_element(), other.get_element())
        
        effective_damage = math.ceil(effective_damage)

        other.set_hp(other.get_hp() - effective_damage)


    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""

        return self.get_evolution() != None and self.evolve_ready
        

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        if self.ready_to_evolve():
            # create new monster class by calling get_evolution()() (extra parethesis to call the class)
            evolved_monster = self.get_evolution()(
                simple_mode=self.simple_mode,
                level=self.level
            )
            difference = self.get_max_hp() - self.get_hp()
            evolved_monster.set_hp(evolved_monster.get_max_hp() - difference)
            return evolved_monster

    

            
    #method for str(obj)
    def __str__(self) -> str:
        return f"LV.{self.get_level()} {self.get_name()}, {self.get_hp()}/{self.get_max_hp()} HP"

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
