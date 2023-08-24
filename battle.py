from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """




        ##########################################################COMPLEXITY ANALYSIS############################################################
        """
        The complexity of this function depends on what runs each turn. 
        This complexity analysis will go through each possible action and the differences in complexity for specific teams.

        Important complexities to go through:
            - attack() method
                - Complexity of this function is the complexity of get_effectiveness() which is O(n * x) where n is the number of elements in the element_names array and x is the number of enum values in the Element class
                - All mathematical operations are O(1) complexity as they are basic operations
                - All other functions used are monster_base() functions which are O(1) complexity
            
            - alive(), evolve(), get_speed(), get_hp(), set_hp(), level_up() and any other monster_base () functions are all O(1) complexity

        


        1. Swap Action
            - If a FRONT team chooses to swap the complexity is O(1) as push() and pop() methods are O(1) complexity
            - If a BACK team chooses to swap the complexity is O(1) as append() and serve() methods are O(1) complexity
            - If an OPTIMISE team chooses to swap the complexity is O(n) + O(log n) = O(n) where n is the number of monsters in the team
                - O(n) complexity for retrieve_from_team() 
                - O(log n) complexity for add_to_team() as it uses a binary search to find the correct position to insert the monster
                - O(n) + O(log n) = O(n) because O(n) is dominant

            - If both teams choose to swap, the complexity would be the sum of the complexities of each team, where dominant complexity would be taken into account
                for example if it were FRONT vs OPTIMISE:
                    - Big O Complexity = O(1) + O(n) = O(n) where n is the number of monsters in the team


        2. Special Action
            - If a FRONT team chooses to special the complexity is O(1) (Special of FRONT Team)
            - If a BACK team chooses to special the complexity is O(1) (Special of BACK Team)
            - If an OPTIMISE team chooses to special the complexity is O(nlogn) (Special of OPTIMISE Team)

            If both teams choose to special, the complexity would be the sum of the complexities of each team, where dominant complexity would be taken into account
                for example if it were FRONT vs OPTIMISE:
                    - Big O Complexity = O(1) + O(nlogn) = O(nlogn) where n is the number of monsters in the team
        
        3. Attack Action
            - FRONT team:
                - 
        



        """
        ##########################################################COMPLEXITY ANALYSIS############################################################

        self.turn_number += 1
        if self.verbosity > 0:
            print(f"Turn {self.turn_number}")
        
        # Process actions for both teams
        action1 = self.team1.choose_action(self.out1, self.out2)
        action2 = self.team2.choose_action(self.out2, self.out1)
        
        if action1 == Battle.Action.SWAP:
            self.team1.add_to_team(self.out1)
            self.out1 = self.team1.retrieve_from_team()
        
        if action1 == Battle.Action.SPECIAL:
            # If SPECIAL is chosen, the monster is returned to the team, the method .special() is called on the team object, and a monster is retrieved from the team (possibly the same monster).
            self.team1.add_to_team(self.out1)
            self.team1.special()
            self.out1 = self.team1.retrieve_from_team()            


        if action2 == Battle.Action.SWAP:
            self.team2.add_to_team(self.out2)
            self.out2 = self.team2.retrieve_from_team()
        
        if action2 == Battle.Action.SPECIAL:
            self.team2.add_to_team(self.out2)
            self.team2.special()
            self.out2 = self.team2.retrieve_from_team()

        if action1 == Battle.Action.ATTACK and action2 != Battle.Action.ATTACK:
            self.out1.attack(self.out2)

        if action1 != Battle.Action.ATTACK and action2 == Battle.Action.ATTACK:
            self.out2.attack(self.out1)
        
        if action1 == Battle.Action.ATTACK and action2 == Battle.Action.ATTACK:
            if self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2)
                if self.out2.alive():
                    self.out2.attack(self.out1)
            elif self.out2.get_speed() > self.out1.get_speed():
                self.out2.attack(self.out1)
                if self.out1.alive():
                    self.out1.attack(self.out2)
            
            elif self.out1.get_speed() == self.out2.get_speed():
                # monsters atack simultaneously
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)


        # Check if both monsters still alive
        if self.out1.alive() and self.out2.alive():
            # -1 health if both monsters alive
            self.out1.set_hp(self.out1.get_hp() - 1)
            self.out2.set_hp(self.out2.get_hp() - 1)
        
        # Check if both monsters fainted
        if not self.out1.alive() and not self.out2.alive():
            if len(self.team1) == 0 and len(self.team2) == 0:
                return Battle.Result.DRAW
            # both monsters fainted
            self.out1 = self.team1.retrieve_from_team()
            self.out2 = self.team2.retrieve_from_team()
        
        # Check if monster 1 fainted
        elif self.out1.alive() and not self.out2.alive():
            if len(self.team2) == 0:
                return Battle.Result.TEAM1
            self.out1.level_up()
            self.out1 = self.out1.evolve()
            self.out2 = self.team2.retrieve_from_team()
        
        # Check if monster 2 fainted
        elif self.out2.alive() and not self.out1.alive():
            if len(self.team1) == 0:
                return Battle.Result.TEAM2
            self.out2.level_up()
            self.out2 = self.out2.evolve()
            self.out1 = self.team1.retrieve_from_team() 

            

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
