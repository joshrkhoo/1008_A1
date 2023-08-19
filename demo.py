import random
import typing
from data_structures.referential_array import ArrayR
from team import MonsterTeam
from helpers import Flamikin, Thunderdrake, Aquariuma, Vineon, Normake, Rockodile, Mystifly, Strikeon, Faeboa, Soundcobra, Gustwing, Thundrake

my_monsters = ArrayR(5)
my_monsters[0] = Flamikin
my_monsters[1] = Aquariuma
my_monsters[2] = Vineon
my_monsters[3] = Thundrake
my_monsters[4] = Normake


# print(my_monsters)


team = MonsterTeam(
    team_mode=MonsterTeam.TeamMode.OPTIMISE,
    selection_mode=MonsterTeam.SelectionMode.MANUAL,
    sort_key=MonsterTeam.SortMode.HP,
)

print(team)

team.special()

print(team)

team.regenerate_team()

print(team)


# team.special()

# team.regenerate_team()

# print(team)
# # flamikin = team.retrieve_from_team()

# print(flamikin)

# thundrake = team.retrieve_from_team()

# print(thundrake)


# team.special()
# print(team)

# team.regenerate_team()
# print(team)

# flamikin = team.retrieve_from_team()

# print(isinstance(flamikin, Flamikin))
