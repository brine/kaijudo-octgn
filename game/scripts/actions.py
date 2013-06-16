#------------------------------------------------------------------------------
# Constant and Variables Values
#------------------------------------------------------------------------------
import re
shields = []
playerside = None
sideflip = None
diesides = 20

def align():
  mute()
  global playerside  ##Stores the Y-axis multiplier to determine which side of the table to align to
  global sideflip  ##Stores the X-axis multiplier to determine if cards align on the left or right half
  if sideflip == 0:  ##the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
    return "BREAK"
  if Table.isTwoSided():
    if playerside == None:  ##script skips this if playerside has already been determined
      if me.hasInvertedTable():
        playerside = -1  #inverted (negative) side of the table
      else:
        playerside = 1
    if sideflip == None:  ##script skips this if sideflip has already been determined
      playersort = sorted(players, key=lambda player: player._id)  ##makes a sorted players list so its consistent between all players
      playercount = [p for p in playersort if me.hasInvertedTable() == p.hasInvertedTable()]  ##counts the number of players on your side of the table
      if len(playercount) > 2:  ##since alignment only works with a maximum of two players on each side
        whisper("Cannot align: Too many players on your side of the table.")
        sideflip = 0  ##disables alignment for the rest of the play session
        return "BREAK"
      if playercount[0] == me:  ##if you're the 'first' player on this side, you go on the positive (right) side
        sideflip = 1
      else:
        sideflip = -1
  else:  ##the case where two-sided table is disabled
    whisper("Cannot align: Two-sided table is required for card alignment.")
    sideflip = 0  ##disables alignment for the rest of the play session
    return "BREAK"
  cardorder = [[],[],[]]
  for card in table:
    if card.controller == me:
      if not card.isFaceUp:
        cardorder[1].append(card)
      elif card.orientation == Rot180 or card.orientation == Rot270:
        cardorder[2].append(card)
      else:
        cardorder[0].append(card)
  xpos = 80
  ypos = 5
  for cardtype in cardorder:
    if cardorder.index(cardtype) == 1:
      xpos = 80
      ypos += 93
    elif cardorder.index(cardtype) == 2:
      xpos = 80
      ypos += 93
    for c in cardtype:
        c.moveToTable(sideflip * xpos, playerside * ypos + (44*playerside - 44))
        xpos += 79

def clear(card, x = 0, y = 0):
    mute()
    card.target(False)

def setup(group, x = 0, y = 0):
    mute()
    for card in me.Deck.top(5): toShields(card, notifymute = True)
    for card in me.Deck.top(5): toHand(card, notifymute = True)
    align()
    notify("{} sets up their battle zone.".format(me))

def setDie(group, x = 0, y = 0):
    mute()
    global diesides
    num = askInteger("How many sides?\n\nFor Coin, enter 2.\nFor Chaos die, enter 6.", diesides)
    if num != None and num > 0:
      diesides = num
      dieFunct(diesides)

def rollDie(group, x = 0, y = 0):
    mute()
    global diesides
    dieFunct(diesides)

def dieFunct(num):
    if num == 6:
      n = rnd(1, 6)
      if n == 1:
        notify("{} rolls 1 (PLANESWALK) on a 6-sided die.".format(me))
      elif n == 6:
        notify("{} rolls 6 (CHAOS) on a 6-sided die.".format(me))
      else:
        notify("{} rolls {} on a 6-sided die.".format(me, n))
    elif num == 2:
      n = rnd(1, 2)
      if n == 1:
        notify("{} rolls 1 (HEADS) on a 2-sided die.".format(me))
      else:
        notify("{} rolls 2 (TAILS) on a 2-sided die.".format(me))
    else:
      n = rnd(1, num)
      notify("{} rolls {} on a {}-sided die.".format(me, n, num))

def untapAll(group, x = 0, y = 0):
    mute()
    for card in group:
        if card.orientation == Rot90:
            card.orientation = Rot0
        if card.orientation == Rot270:
            card.orientation = Rot180
    notify("{} untaps all cards.".format(me))
    
def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} taps {}'.format(me, card))
    else:
        notify('{} untaps {}'.format(me, card))    

def banish(card, x = 0, y = 0):
    mute()
    if not card.isFaceUp:
        card.peek()
        rnd(1,10)
        if re.search("Shield Blast", card.Rules):
            if confirm("Activate Shield Blast for {}\n\n{}?".format(card.Name, card.Rules)):
                toDiscard(card, notifymute = False)
                rnd(1,10)
                notify("{} uses {}'s Shield Blast.".format(me, card))
                return
        toHand(card, notifymute = True)
        notify("{}'s shield is broken.".format(me))

def shuffle(group, x = 0, y = 0):
    mute()
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    notify("{} shuffled their {}".format(me, group.name))

def draw(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    toHand(card, notifymute = True)
    notify("{} draws a card.".format(me))

def drawX(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    count = askInteger("Draw how many cards?", 7)
    if count == None: return
    for card in group.top(count): toHand(card, notifymute = True)
    notify("{} draws {} cards.".format(me, count))
    
def mill(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    toDiscard(card, notifymute = True)
    notify("{} discards top card of Deck.".format(me))
    
def millX(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    count = askInteger("Discard how many cards?", 1)
    if count == None: return
    for card in group.top(count): toDiscard(card, notifymute = True)
    notify("{} discards top {} cards of Deck.".format(me, count))

def randomDiscard(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group.random()
    toDiscard(card, notifymute = True)
    if notifymute == False:
        rnd(1,10)
        notify("{} randomly discards {}.".format(me, card))

def mana(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    toMana(card, notifymute = True)
    notify("{} charges top card of {} as mana.".format(me, group.name))
    
def shields(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    toShields(card, notifymute = True)
    notify("{} sets top card of {} as shield.".format(me, group.name))

def toMana(card, x = 0, y = 0, notifymute = False):
    mute()
    card.moveToTable(0,0)
    card.orientation = Rot180
    align()
    if notifymute == False:
        notify("{} charges {} as mana.".format(me, card))
    
def toShields(card, x = 0, y = 0, notifymute = False):
    mute()
    card.moveToTable(0,0,True)
    align()
    if notifymute == False:
        notify("{} sets a new shield.".format(me))
        
def toPlay(card, x = 0, y = 0, notifymute = False):
    mute()
    card.moveToTable(0,0)
    align()
    if notifymute == False:
        notify("{} plays {}.".format(me, card))

def toDiscard(card, x = 0, y = 0, notifymute = False):
    mute()
    card.moveTo(card.owner.piles['Discard Pile'])
    if notifymute == False:
        notify("{} discards {}.".format(me, card))

def toHand(card, x = 0, y = 0, notifymute = False):
    mute()
    card.moveTo(card.owner.hand)
    if notifymute == False:
        notify("{} moves {} to hand.".format(me, card))