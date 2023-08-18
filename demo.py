import random
import typing
from data_structures.referential_array import ArrayR
from team import MonsterTeam
from helpers import Flamikin, Thunderdrake, Aquariuma, Vineon, Normake, Rockodile, Mystifly, Strikeon, Faeboa, Soundcobra, Thundrake

my_monsters = ArrayR(4)
my_monsters[0] = Flamikin
my_monsters[1] = Aquariuma
my_monsters[2] = Vineon
my_monsters[3] = Thundrake

print(my_monsters)


team = MonsterTeam(
    team_mode=MonsterTeam.TeamMode.FRONT,
    selection_mode=MonsterTeam.SelectionMode.PROVIDED,
    provided_monsters= my_monsters
)

team.print_team()