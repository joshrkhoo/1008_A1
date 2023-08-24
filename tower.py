from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularQueue

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.battle = battle or Battle(verbosity=0)
        self.my_team = None
        self.my_team_lives = None
        self.enemy_teams = None
        self.enemy_teams_lives = None

        self.my_team_elements = ArrayR(0)
        self.enemy_team_elements = ArrayR(0)
        self.out_of_meta_elements = ArrayR(0)

        

    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.my_team = team
        self.my_team_lives = RandomGen.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES)

        self.my_team_elements = self.my_team.get_monster_elements()
        print(self.my_team_elements)
    

    def generate_teams(self, n: int) -> None:

        self.enemy_teams = CircularQueue(n)
        self.enemy_teams_lives = CircularQueue(n)

        for i in range(n):
            self.enemy_teams.append(MonsterTeam(
                team_mode=MonsterTeam.TeamMode.BACK,
                selection_mode=MonsterTeam.SelectionMode.RANDOM
            ))
            self.enemy_teams_lives.append(RandomGen.randint(BattleTower.MIN_LIVES, BattleTower.MAX_LIVES))


    def battles_remaining(self) -> bool:
        # The battle tower ends when there are no enemy teams left, or no lives left for the player team, or both.
        
        # Both have to be true for the battle tower to continue.
        if len(self.enemy_teams) == 0 or self.my_team_lives == 0:
            return False
        else:
            return True


    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        # Simulate one battle
        # Return the result, my team, enemy team, my team lives, enemy team lives


        enemy_team = self.enemy_teams.serve()
        enemy_team_lives = self.enemy_teams_lives.serve()

        self.enemy_team_elements = enemy_team.get_monster_elements()
        print(self.enemy_team_elements)


        self.my_team.regenerate_team()
        enemy_team.regenerate_team()

        battle_result = self.battle.battle(self.my_team, enemy_team)

        if battle_result == Battle.Result.TEAM1:
            enemy_team_lives -= 1
            if enemy_team_lives > 0:
                self.enemy_teams_lives.append(enemy_team_lives)
                self.enemy_teams.append(enemy_team)
        elif battle_result == Battle.Result.DRAW:
            self.my_team_lives -= 1
            enemy_team_lives -= 1
            if enemy_team_lives > 0:
                self.enemy_teams_lives.append(enemy_team_lives)
                self.enemy_teams.append(enemy_team)
        elif battle_result == Battle.Result.TEAM2:
            self.my_team_lives -=1
            self.enemy_teams_lives.append(enemy_team_lives)
            self.enemy_teams.append(enemy_team)
     
        return (battle_result, self.my_team, enemy_team, self.my_team_lives, enemy_team_lives)


    def out_of_meta(self) -> ArrayR[Element]:
        #The out of meta method should compute what elements of monsters have been present in the battles in the battle tower so far, but are not present in the upcoming battle.
        raise NotImplementedError
        
        

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    got = []
    while bt.battles_remaining():
        res = bt.next_battle()
        got.append(res)

    for result, my_team, tower_team, player_lives, tower_lives in got:
        print(result, my_team, tower_team, player_lives, tower_lives)
