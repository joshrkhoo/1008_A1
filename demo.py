from helpers import Metalhorn

f = Metalhorn(simple_mode=True, level=1)
print(f)
f.level_up()
print(f.ready_to_evolve())
print(f)
f.set_hp(8)
print(f.get_hp())
print(f.evolve())