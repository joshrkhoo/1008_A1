from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from data_structures.sorted_list_adt import ListItem
from elements import Element
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR


# for front team
from data_structures.stack_adt import ArrayStack as Stack
# for back team
from data_structures.queue_adt import CircularQueue
# for optimised team
from data_structures.array_sorted_list import ArraySortedList



if TYPE_CHECKING:
    from battle import Battle

class MonsterTeam:

    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        """
        O(1) complexity best/worst case
            - initialising the team is O(1) complexity
            - initialising the provided monsters array is O(1) complexity
                - assuming the get() method of the array is O(1) complexity
            - initialising the sort key is O(1) complexity

        """
        
        self.team_mode = team_mode
        self.selection_mode = selection_mode
        self.kwargs = kwargs
        self.provided_monsters_index = 0

        # create the provided monsters array (we use this for regenerating the team)
            # monsters are added to this on initialisation in chosen selection mode
        self.provided_monsters = self.kwargs.get("provided_monsters", ArrayR(self.TEAM_LIMIT))

        self.sort_key: self.SortMode = self.kwargs.get("sort_key", None)

        # create the team based on the team mode
        self.regenerate_team()

        # Whenever creating a team and the length of the team is greater than the team limit, raise a ValueError
        if len(self) > self.TEAM_LIMIT:
            raise ValueError(f"Team size {len(self)} exceeds limit {self.TEAM_LIMIT}.")

    def __len__(self) -> int:
        """
        Returns the length of the team
        
        O(1) complexity best/worst case
        """

        if self.team_mode == self.TeamMode.FRONT:
            return len(self.front_team)
        elif self.team_mode == self.TeamMode.BACK:
            return len(self.back_team)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            return len(self.optimised_team)
    
    
    def __str__(self) -> str:
        """
        Returns a string representation of the team
        """

        if self.team_mode == self.TeamMode.FRONT:
            return f"Front Team: {str(self.front_team)}"
        elif self.team_mode == self.TeamMode.BACK:
            return f"Back Team: {str(self.back_team)}"
        elif self.team_mode == self.TeamMode.OPTIMISE:
            return f"Optimised Team: {str(self.optimised_team)}"
        

           
    def _get_monster_key(self, monster: MonsterBase) -> int:
        """
        O(1) complexity best/worst case
        """

        # get keys of monsters for the optimised team (we are useing a sorted list)
        key = None
        if self.sort_key == self.SortMode.HP:
            key = monster.get_hp()
        elif self.sort_key == self.SortMode.ATTACK:
            key = monster.get_attack()
        elif self.sort_key == self.SortMode.DEFENSE:
            key = monster.get_defense()
        elif self.sort_key == self.SortMode.SPEED:
            key = monster.get_speed()
        elif self.sort_key == self.SortMode.LEVEL:
            key = monster.get_level()
        return key
    
    def get_monster_elements(self) -> ArrayR[Element]:
        # need to get monster elements for the battle tower
        # this is used for the out of meta method

        element_array = ArrayR(len(self))

        for monster in self.provided_monsters:
            monster_element = Element.from_string(monster.get_element()).value
            for i in range(len(element_array)):
                if element_array[i] is None:
                    element_array[i] = monster_element
                    break
                elif element_array[i] == monster_element:
                    break
        return element_array                




    def add_to_team(self, monster: MonsterBase):
        """
        O(1) complexity best/worst case for FRONT and BACK team modes
            - push() and append() are O(1) complexity
        
        O(log(n)) complexity best/worst case for OPTIMISE team mode
            - add() is O(log(n)) complexity due to binary search
        """
        if self.team_mode == self.TeamMode.FRONT:
            self.front_team.push(monster)
        elif self.team_mode == self.TeamMode.BACK:
            self.back_team.append(monster)
        elif self.team_mode == self.TeamMode.OPTIMISE:
            key = self._get_monster_key(monster)
            # multiply by self.sort_direction in case a monster is added to the team after special() is called
                # this is because the direction changes when special() is called 
                    #i.e descending to ascending or vice versa
            self.optimised_team.add(ListItem(monster, key * self.sort_direction))

    def retrieve_from_team(self) -> MonsterBase:
        """
        O(1) complexity best/worst case for FRONT and BACK team modes
            - pop() and serve() are O(1) complexity
        O(n) complexity best/worst case for OPTIMISE team mode
            - delete_at_index() is O(n) complexity where n is the size of the optimised team 
                - this is because all the items have to shuffle in the direction the index is deleted
                    - so if the index is 0, all the items have to shuffle to the left
        """

        if self.team_mode == self.TeamMode.FRONT:
            return self.front_team.pop()
        elif self.team_mode == self.TeamMode.BACK:
            return self.back_team.serve()
        elif self.team_mode == self.TeamMode.OPTIMISE:
            return self.optimised_team.delete_at_index(0).value
    

    def special(self) -> None:

        ########### FRONT TEAM COMPLEXITY ###########
        """
        Both best and worse case complexity is O(1) as we are only iterating through 3 elements of a queue
            - while loop is O(1) complexity due to is_empty() being constant complexity 
        """ 
        ########### FRONT TEAM COMPLEXITY ###########    


        # if team mode is front
        if self.team_mode == self.TeamMode.FRONT:
            # create a queue to store popped monsters
                # do this as we cant just use stack operations to reverse elements
            temp_queue = CircularQueue(3)
            for i in range(3):
                # if there are no more monsters in the front team, break
                    # so even if there are only 2 monsters they will still be reversed
                    # if there is one monster then it doesnt matter
                if len(self.front_team) == 0:
                    break
                temp_queue.append(self.front_team.pop())

            while not temp_queue.is_empty():
                self.front_team.push(temp_queue.serve())


        ########### BACK TEAM COMPLEXITY ###########
        """
        Both best and worse case complexity is O(n) where n is the size of the back team 
            - All data structure methods are O(1) complexity
            - Best case would occur when there is only 1 monster in the team
            - Worst case would occur when there are 6+ monsters in the team
        """ 
        ########### BACK TEAM COMPLEXITY ###########    

        if self.team_mode == self.TeamMode.BACK:
            team_size = len(self.back_team)
            temp_stack = Stack(team_size)
            temp_queue = CircularQueue(team_size)
            
            # iterate through the back team up until the halfway point
            for i in range(len(self.back_team)//2):
                # add the first half of the monsters to the temp queue
                    # these monsters will remain in the same order 
                temp_queue.append(self.back_team.serve())

            # remove the second half of the monsters from the back team
                # add those monsters to the temp stack so they are reversed when appended back
            while not self.back_team.is_empty():
                temp_stack.push(self.back_team.serve())
            # add the monsters from the temp stack to the back team first so they are at the front
            while not temp_stack.is_empty():
                self.back_team.append(temp_stack.pop())
            # then add the front half to the back team so they are at the back
            while not temp_queue.is_empty():
                self.back_team.append(temp_queue.serve())


        ########### OPTIMISE TEAM COMPLEXITY ###########
        """
        Both best and worse case complexity is O(n * logn) where n is the size of the optimised team 
            - logn is due to the add() method which uses binary search
        """ 
        ########### OPTIMISE TEAM COMPLEXITY ###########   


        if self.team_mode == self.TeamMode.OPTIMISE:
            temp_list = ArraySortedList(len(self.optimised_team))
            # update the sort direction
            self.sort_direction *= -1
            # print(self.sort_direction)

            # iterate through the optimised team and add the monsters with the updated sort direction to the temp list
                # this will change the sort direction from whatever it is 
                    # if its descending (-1) it will change to ascending (1)
            for i in range(len(self.optimised_team)):
                item = self.optimised_team[i]
                item.key = item.key * -1
                temp_list.add(item)
            self.optimised_team = temp_list

    
 
    def regenerate_team(self) -> None:
        """
        Initialises the teams based on the selection mode, then switches to provided mode for rengenerating teams.

                                                    Complexity Analysis:
        On initialisation:
            If selection mode is RANDOM:
                - Best/Worse case complexity = complexity of select_randomly() 
            If selection mode is MANUAL:
                - Best/Worse case complexity = O(a + n) where a is the complexity of get_all_monsters() and n is the size of the team that the user chooses (number of monsters in the team)
            If selection mode is PROVIDED:
                - Best/Worse case complexity = O(n) where n is the number of monsters in the provided monsters array
        
        On regenerating teams:
            - Best/Worse case complexity = O(n) where n is the number of monsters in the provided monsters array
            - This is because we populate self.provided_monsters with monsters that are chosen on initialisation no matter the selection mode
        """

        self.front_team = Stack(self.TEAM_LIMIT)
        self.back_team = CircularQueue(self.TEAM_LIMIT)
        self.optimised_team = ArraySortedList(self.TEAM_LIMIT)

        # initial sort direction is -1 as we want to sort in descending order as a default
            # this will occur for regenerating teams as well
        self.sort_direction = - 1

        # create provided_monsters
        if self.selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly()
        elif self.selection_mode == self.SelectionMode.MANUAL:
            self.select_manually()
        elif self.selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(self.provided_monsters)
        else:
            raise ValueError(f"self.selection_mode {self.selection_mode} not supported.")
        
        # switch to provided so we can regenerate teams to initial state (this will occur on innitialisation)
        self.selection_mode = self.SelectionMode.PROVIDED




    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable-1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        # adding mosters to provided monsters array for regeneration
                        self.provided_monsters[self.provided_monsters_index] = monsters[x]
                        self.provided_monsters_index += 1
                        self.add_to_team(monsters[x]())
                        break
            else:
                raise ValueError("Spawning logic failed.")
            
    

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

            How many monsters are there? 2
            MONSTERS Are:
            1: Flamikin [✔️]
            2: Infernoth [❌]
            3: Infernox [❌]
            4: Aquariuma [✔️]
            5: Marititan [❌]
            6: Leviatitan [❌]
            7: Vineon [✔️]
            8: Treetower [❌]
            9: Treemendous [❌]
            10: Rockodile [✔️]
            11: Stonemountain [❌]
            12: Gustwing [✔️]
            13: Stormeagle [❌]
            14: Frostbite [✔️]
            15: Blizzarus [❌]
            16: Thundrake [✔️]
            17: Thunderdrake [❌]
            18: Shadowcat [✔️]
            19: Nightpanther [❌]
            20: Mystifly [✔️]
            21: Telekite [❌]
            22: Metalhorn [✔️]
            23: Ironclad [❌]
            24: Normake [❌]
            25: Strikeon [✔️]
            26: Venomcoil [✔️]
            27: Pythondra [✔️]
            28: Constriclaw [✔️]
            29: Shockserpent [✔️]
            30: Driftsnake [✔️]
            31: Aquanake [✔️]
            32: Flameserpent [✔️]
            33: Leafadder [✔️]
            34: Iceviper [✔️]
            35: Rockpython [✔️]
            36: Soundcobra [✔️]
            37: Psychosnake [✔️]
            38: Groundviper [✔️]
            39: Faeboa [✔️]
            40: Bugrattler [✔️]
            41: Darkadder [✔️]
            Which monster are you spawning? 38
            MONSTERS Are:
            1: Flamikin [✔️]
            2: Infernoth [❌]
            3: Infernox [❌]
            4: Aquariuma [✔️]
            5: Marititan [❌]
            6: Leviatitan [❌]
            7: Vineon [✔️]
            8: Treetower [❌]
            9: Treemendous [❌]
            10: Rockodile [✔️]
            11: Stonemountain [❌]
            12: Gustwing [✔️]
            13: Stormeagle [❌]
            14: Frostbite [✔️]
            15: Blizzarus [❌]
            16: Thundrake [✔️]
            17: Thunderdrake [❌]
            18: Shadowcat [✔️]
            19: Nightpanther [❌]
            20: Mystifly [✔️]
            21: Telekite [❌]
            22: Metalhorn [✔️]
            23: Ironclad [❌]
            24: Normake [❌]
            25: Strikeon [✔️]
            26: Venomcoil [✔️]
            27: Pythondra [✔️]
            28: Constriclaw [✔️]
            29: Shockserpent [✔️]
            30: Driftsnake [✔️]
            31: Aquanake [✔️]
            32: Flameserpent [✔️]
            33: Leafadder [✔️]
            34: Iceviper [✔️]
            35: Rockpython [✔️]
            36: Soundcobra [✔️]
            37: Psychosnake [✔️]
            38: Groundviper [✔️]
            39: Faeboa [✔️]
            40: Bugrattler [✔️]
            41: Darkadder [✔️]
            Which monster are you spawning? 2
            This monster cannot be spawned.
            Which monster are you spawning? 1
            """
        
        """
                                        Complexity Analysis:
            
            O(a + n) complexity best/worst case 
                - n is size of the team that the user chooses (number of monsters in the team)
                - a is the get_all_monsters() complexity
                - User inputs are O(1) complexity
            
            Complexity would change to O(n) or O(a) depending on whether the size of team that the user chooses is greater than the number of monsters in the game

        """ 
        
        # Prompting user for team size
        num_of_user_monsters = int(input("How many monsters are there? "))
        while num_of_user_monsters < 1 or num_of_user_monsters > self.TEAM_LIMIT:
            print("Invalid team size.")
            num_of_user_monsters = int(input("How many monsters are there? "))

        # Printing out the monsters for user to choose
        print("MONSTERS Are:")
        monsters = get_all_monsters()
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                print(f"{x+1}: {monsters[x]} [✔️]")
            else:
                print(f"{x+1}: {monsters[x]} [❌]")

        # Prompting user to choose monsters        
        for i in range(num_of_user_monsters):
            while True:
                user_monster = int(input("Which monster are you spawning? "))
                if user_monster < 1 or user_monster > len(monsters):
                    print("Invalid monster.")
                    continue
                if monsters[user_monster-1].can_be_spawned():
                    # adding mosters to provided monsters array for regeneration 
                    self.provided_monsters[self.provided_monsters_index] = monsters[user_monster-1]
                    self.provided_monsters_index += 1
                    self.add_to_team(monsters[user_monster-1]())
                    break
                else:
                    print("This monster cannot be spawned.")
        

    def select_provided(self, provided_monsters: Optional[ArrayR[type[MonsterBase]]]=None):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """

        """
        O(n) complexity best/worst case where n is the number of monsters in the provided monsters array
            - iterating through the provided monsters array is O(n) complexity
        """
        
        if provided_monsters is None:
            raise ValueError("provided_monsters cannot be None.")

        for monster in provided_monsters:
            # Random monster makes between 1 and max monsters (rest of array is None)
            if monster is None:
                break
            if monster.can_be_spawned() is False:
                raise ValueError(f"Monster {monster} cannot be spawned.")
            self.add_to_team(monster())

            


    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
