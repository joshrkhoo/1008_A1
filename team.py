from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

# for back team
from data_structures.queue_adt import Queue, CircularQueue
# for optimised team
from data_structures.array_sorted_list import ArraySortedList
# for front team
from data_structures.stack_adt import ArrayStack as Stack

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
        self.front_team = Stack(self.TEAM_LIMIT)
        self.back_team = CircularQueue(self.TEAM_LIMIT)
        self.optimised_team = ArraySortedList(self.TEAM_LIMIT)


        self.team_mode = team_mode
        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")
        

    def __len__(self) -> int:
        raise NotImplementedError
    

    def print_team(self) -> None:
        if self.TeamMode.FRONT:
            while not self.front_team.is_empty():
                self.front_team.peek()
                self.front_team.pop() 


    def add_to_team(self, monster: MonsterBase):
        if self.TeamMode.FRONT:
            self.front_team.push(monster)
        elif self.TeamMode.BACK:
            self.back_team.append(monster)
        elif self.TeamMode.OPTIMISE:
            # it is added in the position which maintains the sorted order descending with respect to a particular stat, which is provided at initialisation.
            if self.SortMode.HP:
                self.optimised_team.add(monster, lambda x: x.get_hp())
            elif self.SortMode.ATTACK:
                self.optimised_team.add(monster, lambda x: x.get_attack())
            elif self.SortMode.DEFENSE:
                self.optimised_team.add(monster, lambda x: x.get_defense())
            elif self.SortMode.SPEED:
                self.optimised_team.add(monster, lambda x: x.get_speed())
            elif self.SortMode.LEVEL:
                self.optimised_team.add(monster, lambda x: x.get_level())
    

        

    def retrieve_from_team(self) -> MonsterBase:
        if self.TeamMode.FRONT:
            return self.front_team.pop()
        elif self.TeamMode.BACK:
            return self.back_team.serve()
        elif self.TeamMode.OPTIMISE:
            return self.optimised_team.delete_at_index(0)
    

    def special(self) -> None:
        if self.TeamMode.FRONT:
            # first 3 monsters at the front are reversed up to the current capacity of the stack
            # creating a temp stack to store popped monsters
            temp_stack = Stack(self.TEAM_LIMIT)
            if len(self.front_team) >= 3:
                for _ in range(3):
                    temp_stack.push(self.front_team.pop())


    def regenerate_team(self) -> None:
        raise NotImplementedError

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
        
        user_monsters = int(input("How many monsters are there? "))
        print("MONSTERS Are:")
        monsters = get_all_monsters()
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                print(f"{x+1}: {monsters[x]} [✔️]")
            else:
                print(f"{x+1}: {monsters[x]} [❌]")
        for _ in range(user_monsters):
            while True:
                user_monster = int(input("Which monster are you spawning? "))
                if monsters[user_monster-1].can_be_spawned():
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
        
        if provided_monsters is None:
            raise ValueError("provided_monsters cannot be None.")
        
        if self.TeamMode.FRONT:
            for monster in provided_monsters[::-1]:
                self.add_to_team(monster())
                print(monster())

        
        

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
