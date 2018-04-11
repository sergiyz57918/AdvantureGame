import random
class gameItems:
    class Weapon:
        def __init__(self):
            raise NotImplementedError("No we cannot make it in to the weapon")

        def __str__(self):
            return self.name

    class Spear(Weapon):
        def __init__(self):
            self.name = "Spear"
            self.description = "A razor tipped polearm. The shaft is wooden, and the tip is worked steel " 
            self.damage = 10

    class pistol223(Weapon):
        def __init__(self):
            self.name = ".223 pistol"
            self.description = "A .223 rifle modified and cut down to a pistol. This is a one-of-a-kind firearm, obviously made with love and skill." 
            self.damage = 50
    class Explosives(Weapon):
        def __init__(self):
            self.name = "Explosives"
            self.description = "A chunk of Cordex, a military brand of plastic explosives. Highly stable, very destructive. Includes a timer." 
            self.damage = 1000
       
    class Consumable:
        def __init__(self):
            raise NotImplementedError("Do not create raw Consumable objects.")

        def __str__(self):
            return self.name+" (+"+str(self.healing_value)+" HP)"


    class HealingPouder(Consumable):
        def __init__(self):
            self.name = "Healing Pouder"
            self.healing_value = 25
class NonPlayableCharacter(object):
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        return self.name


class Chest(NonPlayableCharacter):
    def __init__(self):
        self.name = "Chest"
        self.h = 100
        self.inventory = [gameItems.Explosives()]
class enemies:
    
    class Enemy:
        def __init__(self):
            raise NotImplementedError("Do not create raw Enemy objects.")

        def __str__(self):
            return self.name

        def is_alive(self):
            return self.hp > 0

    class GiantAnt(Enemy):
        def __init__(self):
            self.name = "Giant Ant"
            self.hp = 10
            self.damage = 2

    class RadScorpion(Enemy):
        def __init__(self):
            self.name = "Rad Scorpion"
            self.hp = 20
            self.damage = 5

    class Cameron(Enemy):
        def __init__(self):
            self.name = "Cameron"
            self.hp = 80
            self.damage = 15

    class Door(Enemy):
        def __init__(self):
            self.name = "Door"
            self.hp = 1000

class world(object): 
    class MapTile(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def intro_text(self):
            raise NotImplementedError("Create a subclass instead!")

        def modify_player(self, player):
            pass

    class StartTile(MapTile):
        def intro_text(self):
            return """
            You find yourself at the entrance of a temple.
            You look around and find that only path you have is to go inside,
            as other paths are blocked by the palicade and sharpened stakes.   
            """
    class VictoryTile(MapTile):
        def modify_player(self, player):
            player.victory = True

        def intro_text(self):
            return """
            You see a bright light in the distance...
            ... it grows as you get closer! It's sunlight!
            It is puring down on the blue and yellow jumpsuit!
            You take it and turn it over, it reads:
            VAULT 101
            You realise that you are in Fallout 2 Universe. 
            Congradulations - now go and buy the game if you want to continue
            """
    class DoorTile(MapTile):
            def __init__(self, x, y):
              self.door_opened = False
              self.enemy = enemies.Door()
              super(world.DoorTile,self).__init__(x, y)
              self.alive_text = """
                      You can see a big door with a big lock. 
                      You can try and pick the lock or
                      You can try and destroy it
                      """
              self.dead_text = """Pass is open now
                      """

              super(world.DoorTile,self).__init__(x,y)
        
            def intro_text(self):
               if self.enemy.is_alive():
                 text = self.alive_text  
               else:
                 text =  self.dead_text
               return text
            
    class EnemyTile(MapTile):
        def __init__(self, x, y):
            r = random.random()
            if r < 0.80:
                self.enemy = enemies.GiantAnt()
                self.alive_text ="""
                                 A giant ant toward you 
                                 its pincers snap at you! """
                self.dead_text = """
                                 The corpse of a dead ant 
                                 disolves on the ground. you sing
                                 Dead Ant, Ded Ant, Tad-Da-Da-Da"""
            else: 
                self.enemy = enemies.RadScorpion()
                self.alive_text = """
                                 A giant Scorpion crols toward you 
                                 its stinger lashes at you!"""
                self.dead_text = """
                                 The corpse of a dead scorpion 
                                 disolves on the ground. You Exclaim 
                                 Whisky Tango Foxtrot was that thing?"""

            super(world.EnemyTile,self).__init__(x, y)
        def intro_text(self):
            if self.enemy.is_alive():
              text = self.alive_text  
            else:
             text =  self.dead_text
            return text

        def modify_player(self, player):
            if self.enemy.is_alive():
                player.hp = player.hp - self.enemy.damage
                printNow("Enemy does "+str(self.enemy.damage)+" damage. You have "+str(player.hp)+" HP remaining.")

    class BossTile(MapTile):
        def __init__(self, x, y):
           self.enemy = enemies.Cameron()
           self.alive_text = """
                      A man yels at you:            
                      My Name is Cameron!!!
                      "You Shell Not Pass" and launges at you!
                      """
           self.dead_text = """
                      The corpse of a dead man disolves on the ground. you sing
                          Dead Ant, Ded Ant, Tad-Da-Da-Da"""

           super(world.BossTile,self).__init__(x,y)
        def intro_text(self):
            if self.enemy.is_alive():
              text = self.alive_text  
            else:
             text =  self.dead_text
            return text

        def modify_player(self, player):
            if self.enemy.is_alive():
                player.hp = player.hp - self.enemy.damage
                printNow("Enemy does "+str(self.enemy.damage)+" damage. You have "+str(player.hp)+" HP remaining.")

    class TrapTile(MapTile):
        def __init__(self, x, y):
           self.alive_text = """
                             You notice some strange patterns on the floor, but you barge in anyway
                             """
           super(world.TrapTile,self).__init__(x, y)

    
        def intro_text(self):
            text = self.alive_text
            return text

        def modify_player(self, player):
           r = random.random()
           if r <0.5:
               self.modify_player(player)
               damage = int(random.random()*10)
               player.hp = player.hp - damage
               printNow("Trap does "+str(damage)+" damage. You have "+str(player.hp)+" HP remaining.")
           else: 
               printNow ("You figure that there is a trap somwhere in the room but it seam you go lucky or...")

    class LootTile(MapTile): 
        def __init__(self, x, y):
            #Random Item Drop
            r = random.random()
            self.item_claimed = False
            if r < 0.10:
                self.item = gameItems.pistol223()
            elif r < 0.80:
                self.item = gameItems.HealingPouder()
            else: 
                self.item = gameItems.pistol223()
            super(world.LootTile,self).__init__(x, y)

        def intro_text(self):
            if self.item_claimed:
                return """
                Another unremarkable part of the tample. You must forge onwards.
                """
            else:
                return "Someone dropped some "+self.item.name

        def modifyPlayer(self, player):
            if not self.item_claimed:
                self.item_claimed = True
                item = self.item
                player.inventory.append(item)
                printNow(item.name+" added to your inventory.")
    
    class EnemyLootTile(MapTile): 
        def __init__(self, x, y,name):
            self.name=name
            self.item_claimed = False
            #Random Item Drop
            r = random.random()
            if r < 0.10:
                self.item = gameItems.pistol223()
            elif r < 0.80:
                self.item = gameItems.HealingPouder()
            else: 
                self.item_claimed = True
                
            super(world.EnemyLootTile,self).__init__(x, y)

        def intro_text(self):
            if self.item_claimed:
                return self.name+" body decomposing on the ground"
            else:
                return self.name+" dropped some "+self.item.name

        def modifyPlayer(self, player):
            if not self.item_claimed:
                self.item_claimed = True
                item = self.item
                player.inventory.append(item)
                printNow(item.name+" added to your inventory.")
                
    class PassageTile(MapTile):
        def intro_text(self):
            roomDesc = ["""
            You are in a dark, musty temple. 
            The shadows seem to play tricks with your eyes, 
            and you can hear the faint sound of movement.
            ""","""
            You see a coridor draped in darkness in front of you
            What does this darknes holds for you? 
            ""","""
            You see skatered pieces of cealing on the flor. 
            Watch your steps.
            ""","""
            You can see body lying on the floor, you get closer. 
            Name tag reads "Parzeval" 
            You find the bloody message close to the corps. 
            BeWare they are working for IOI,  they are sixers!
            Don't trust them!
            ""","""
            You start seeing strang glowing symbols in the dark. 
            Sudenly you relise what they are saying: 
            Peace of Eden belongs to us!
            ""","""
            On the walls you can read the big sign: 
            "Save Chear Leader - Save the World"
            ""","""
            A crack in the ceiling above the middle of the north wall 
            allows a trickle of water to flow down to the floor. 
            The water pools near the base of the wall, 
            and a rivulet runs along the wall an out into the hall. 
            The water smells fresh
            ""","""
            A large arched niche pierces one wall of this chamber. 
            Filled with rotting wood and rubble the niche appears 
            to be a dumping ground of sorts. Elsewhere in the room, 
            several sections of floor are cracked and pitted.
            """, """
            This irregularly-shaped room has an uneven floor. 
            Several small puddles have gathered in the deeper depressions. 
            Elsewhere, small pieces of rubble litter the floor.
            ""","""
            The arched ceiling of this chamber rises to a height of 20 ft. 
            In the centre of the room, but is barely man-high where it meets the walls.
            The arches holding the ceiling aloft are carved to represent writhing tentacles;
            a few have been defaced but the upper portions of all remain untouched.
            ""","""
            A pile of rotting wood, rubbish and other detritus partially obscures one wall of this chamber.
            Clearly used as a rubbish dump, the stench of decay and rot hangs heavily in the air
            ""","""
            This large chamber was the scene of an ancient battle. 
            Skeletal remains of at least a dozen humanoids lie scattered about the room where they fell. 
            Several rusting broken spears and shattered, rotting shields lie among the fallen.
            ""","""
            Part of one wall of this room has collapsed, revealing the natural rock behind the dressed stone wall. 
            The rubble has been moved to create a breastwork across one of the room�??s exits. 
            Splatters of old, dried blood decorate the top of the breastwork.
            ""","""
            The remains of a cold camp are evident here. 
            A tattered cloak�??sized for a gnome or halfling�??along with two empty wineskins and the stripped bones
            of a chicken and crusts of mouldy bread bear testimony to an explorer�??s rest.
            ""","""
            A gaping open pit in one of this chamber�??s doorways blocks access to the area beyond. 
            Two skeletons, pierced by dozens of tiny stone spikes, lie in the pit. 
            The chamber beyond boasts a stone plinth and altar set in a semi-circular niche. 
            The chamber�??s other doorway�??twice the width of the trapped one�??appears unprotected.
            """]
        
            #print (self.x, self.y)
            roomDesc= random.choice(roomDesc)
            printNow (roomDesc)
            return ""
    class ChestTile(MapTile):
        def __init__(self, x, y):
          self.chest = Chest()
          super(world.ChestTile,self).__init__(x, y)
        
        def check_chest(self, player):
          while True:
              user_input = requestString("Would you like to (T)cake, (P)lace, or (C)ancel?")
              if user_input.find('C')==0 or user_input.find('c')==0:
                  return
              elif user_input.find('T')==0 or user_input.find('t')==0:
                  print("Here's whats in the chest: ")
                  self.take_item(inv2=player, inv1=self.chest)
              elif user_input.find('P')==0 or user_input.find('p')==0:
                  print("Here's whats you can place in the chest: ")
                  self.take_item(inv2=self.chest, inv1=player)
              else:
                  print("Invalid choice!")
                
        def take_item(self, inv1, inv2):
            for i, item in enumerate(inv1.inventory):
              printNow("/n"+inv1.name+" Content: ")
              printNow(str(i)+". "+item.name+" ")
              while True:
                user_input =  requestString("Choose an item or press C to exit: ")
                if user_input.find('C')==0 or user_input.find('c')==0:
                    return
                else:
                    try:
                        choice = int(user_input)
                        to_swap = inv1.inventory[choice - 1]
                        self.swap(inv1, inv2, to_swap)
                    except ValueError:
                      print("Invalid choice!")

        def swap(self, inventory1, inventory2, item):
            inventory1.inventory.remove(item)
            inventory2.inventory.append(item)
            printNow("  "+item.name+" was transfered")

        def intro_text(self):
            return """
            A sturdy chest tucked in the corner of the room.
            Maybe you should check what is inside.
            """                
                                
                                    
     #Game World Main functions
    worldLocations = """
|VT|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|FB|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|PS|LT|__|__|__|LT|__|__|__|__|__|__|__|__|__|__|__|__|
|__|PS|EN|LT|EN|LT|__|__|__|__|__|__|__|__|__|__|__|__|
|__|TR|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|PS|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|LT|PS|EN|LT|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|EN|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|PS|TR|EN|LT|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|__|PS|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|__|DT|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|__|EN|PS|__|__|LT|CH|__|__|__|__|__|__|__|__|__|__|
|__|__|__|TR|EN|EN|PS|__|__|__|__|__|__|__|__|__|__|__|
|__|__|__|__|PS|__|EN|__|__|__|__|__|__|__|__|__|__|__|
|__|__|__|__|TR|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|__|LT|EN|PS|__|EN|LT|__|__|__|__|__|__|__|__|__|__|
|__|__|__|__|DT|EN|PS|__|__|__|__|__|__|__|__|__|__|__|
|__|__|__|__|ST|__|__|__|__|__|__|__|__|__|__|__|__|__|
|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
"""
    def get():
      return self

    def is_locations_valid(object,locations):
        if locations.count("|ST|") != 1:
            return False
        if locations.count("|VT|") == 0:
            return False
        lines = locations.splitlines()
        lines = [l for l in lines if l]
        pipe_counts = [line.count("|") for line in lines]
        for count in pipe_counts:
            if count != pipe_counts[0]:
                return False

        return True

    tile_type_dict = {"VT": VictoryTile,
                      "FB": BossTile,
                      "EN": EnemyTile,
                      "PS": PassageTile,
                      "ST": StartTile,
                      "LT": LootTile,
                      "TR": TrapTile,
                      "CH": ChestTile,
                      "DT": DoorTile,
                      "__": None}


    world_map = []

    start_tile_location = None


    def parse_world_locations(object):
        if not world.is_locations_valid(object,world.worldLocations):
            raise SyntaxError("Thi location is invalid!")

        locations_lines = world.worldLocations.splitlines()
        #print (locations_lines)
        locations_lines = [x for x in locations_lines if x]
        #print (len(locations_lines))
        for y, locations_row in enumerate(locations_lines):
            row = []
            locations_cells = locations_row.split("|")
            #print (locations_cells)
            locations_cells = [c for c in locations_cells if c]
            #print (len(locations_cells))
            for x, locations_cell in enumerate(locations_cells):
                #print (str(x)+":Cell: |"+locations_cell+"|")
                tile_type = world.tile_type_dict[locations_cell]
                if tile_type == world.StartTile:
                    global start_tile_location
                    start_tile_location = x, y
                if tile_type :
                  row.append(tile_type(x, y))
                else:
                  row.append(None )

            world.world_map.append(row)


    def tile_at(self,x, y):
        if x < 0 or y < 0:
            return None
        try:
            return world.world_map[y][x]
        except IndexError:
            return None
class player:
    class Player:
        def __init__(self):
            self.inventory = [gameItems.Spear() ]
            self.x = start_tile_location[0]
            self.y = start_tile_location[1]
            self.hp = 100
            self.victory = False
            self.name = "Player One"

        def is_alive(self):
            return self.hp > 0

        def print_inventory(self):
            printNow("Inventory:")
            for item in self.inventory:
                printNow('* ' + str(item))

        def heal(self):
            consumables = [item for item in self.inventory
                           if isinstance(item, gameItems.Consumable)]
            if not consumables:
                printNow("You don't have any items to heal you!")
                return
            i=0
            for i,item in enumerate(consumables):
                i=i+1
                printNow("Choose an item to use to heal:")
                printNow(str(int(i))+". "+str(item.name))

            valid = False
            while not valid:
                choice = input("")
                try:
                    to_eat = consumables[int(choice) - 1]
                    self.hp = min(100, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    printNow("Current HP: "+str(self.hp))
                    valid = True
                except (ValueError, IndexError):
                    printNow("Invalid choice, try again.")

        def most_powerful_weapon(self):
            max_damage = 0
            best_weapon = None
            for item in self.inventory:
                try:
                    if item.damage > max_damage:
                        best_weapon = item
                        max_damage = item.damage
                except AttributeError:
                    pass

            return best_weapon

        def move(self, dx, dy):
            self.x += dx
            self.y += dy

        def move_north(self):
            self.move(dx=0, dy=-1)

        def move_south(self):
            self.move(dx=0, dy=1)

        def move_east(self):
            self.move(dx=1, dy=0)

        def move_west(self):
            self.move(dx=-1, dy=0)

        def attack(self,w):
            best_weapon = self.most_powerful_weapon()
            room = w.tile_at(self.x, self.y)
            enemy = room.enemy
            printNow("You use "+best_weapon.name+" against "+enemy.name+"!")
            enemy.hp -= best_weapon.damage
            if not enemy.is_alive():
                printNow("You killed "+enemy.name+"!")
                w.world_map[room.y][room.x]=w.EnemyLootTile(room.x,room.y,enemy.name)
            else:
                printNow(enemy.name+" HP is "+str(enemy.hp))

        def loot(self,w):
            room = w.tile_at(self.x, self.y)
            room.modifyPlayer(self)
        
        def lockpic (self,w):
            r = random.random()
            room = w.tile_at(self.x, self.y)
            printNow(r)
            if r<10:
              room.door_opened=True
              room.enemy.hp=-1
        
        def check(self,w):
              room = w.tile_at(self.x, self.y)
              room.check_chest(self)   
       
        def quit(self):
            self.hp=-1

#Global Variables and Arrays
WELCOME = """
===================================================================================
|                              Sectioin Six Labs                                  |
|                                 Presents                                        |
|                          "Escape from Temple of Terror!"                        |
|             In each room you will be told which directions you can go           |
|     You'll be able to go north, south, east or west by typing that direction    |
|                                                                                 |
===================================================================================
"""
#from collections import OrderedDict


def play():
    w=world()
    w.parse_world_locations()
    printNow(WELCOME)
    p = player.Player()
    while p.is_alive() and not p.victory:
        room = w.tile_at(p.x, p.y)
        printNow(room.intro_text())
        room.modify_player(p)
        if p.is_alive() and not p.victory:
            choose_action(w,room, p)
        elif not p.is_alive():
            printNow("Your journey has come to an early end!")


def choose_action(w,room, player):
    action = None
    while not action:
        available_actions = get_available_actions(w,room, player)
        action_input = requestString("Action: ")
        action = available_actions.get(action_input)
        if action and action_input:
          if action =="loot":
            player.loot(w) 
          elif action =="attack":
            player.attack(w)
          elif action =="lockpic":
            player.lockpic(w)
          elif action =="check":
            player.check(w)
          else:
            action()
        else:
            printNow("Invalid action!")


def get_available_actions(w,room, player):
    actions = {}
    printNow("Choose an action: ")
    action_adder(actions, 'q', player.quit, "Quit")
    if player.inventory:
            action_adder(actions, 'i', player.print_inventory, "Inventory")
    if isinstance(room, world.LootTile) or isinstance(room, world.EnemyLootTile):
        if room.item_claimed == False: 
            action_adder(actions, 'l', "loot", "Loot")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', "attack", "Attack")
    if isinstance(room, world.ChestTile):
        action_adder(actions, 'c', "check", "Check")
    if isinstance(room, world.BossTile) and room.enemy.is_alive():
        action_adder(actions, 'a', "attack", "Attack")
    if isinstance(room, world.DoorTile) and room.enemy.is_alive():
        action_adder(actions, 'a', "attack", "Attack")
        if room.door_opened ==False:
           action_adder(actions, 'p', "lockpic", "Pick a lock")
    else:
        if w.tile_at(room.x, room.y - 1):
            if (isinstance(room, world.DoorTile) or isinstance(room, world.BossTile))and room.enemy.is_alive():
                pass
            else:
              action_adder(actions, 'n', player.move_north, "Go north")
        if w.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Go south")
        if w.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Go east")
        if w.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Go west")
    if player.hp < 100:
        action_adder(actions, 'h', player.heal, "Heal")

    return actions


def action_adder(action_dict, hotkey,action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    action_dict[name.upper()] = action
    action_dict[name.lower()] = action
    printNow(hotkey+": "+name)


play()