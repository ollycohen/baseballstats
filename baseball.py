import re, math, sys, os

valid_name = re.compile(r"^\b[A-Z]{1}\w*\s[A-Z]{1}\w*\b")
valid_bats = re.compile(r"(?<=batted\s)\d")
valid_hits = re.compile(r"\d(?=\shits)")


#https://classes.engineering.wustl.edu/cse330/index.php?title=Python#Command-Line_Arguments
#Check number of arguments
if len(sys.argv) < 2:
    sys.exit(f"Usage: {sys.argv[0]} filename")
    
filename = sys.argv[1]
#filename = "cardinals-1940.txt"
    
if not os.path.exists(filename):
    sys.exit(f"Error: File '{sys.argv[1]}' not found")

#Initialize dictionary of players
players = {}

#find___Match inspired by: https://docs.python.org/3/library/re.html#regular-expression-examples
#findNameMatch calls the addData function if there's a match 
def findNameMatch(match):
    if match is None:
        return None
    else:
        return match.group()
    
def findBatsMatch(match):
    if match is None:
        return None
    else:
        return int(match.group())
        
def findHitsMatch(match):
    if match is None:
        return None
    else:
        return int(match.group())
    

def addData(name, at_bats, hits):
    if name in players:
        players[name][0] += at_bats
        players[name][1] += hits
    else:
        players[name] = [at_bats,hits]


def makePlayers(file):
    with open(file) as f:
            for line in f:
                at_bats = findBatsMatch(valid_bats.search(line))
                hits = findHitsMatch(valid_hits.search(line))
                name = findNameMatch(valid_name.match(line))
                if name is not None:
                    addData(name, at_bats, hits)

    
def calculateAvg(players):
    for player in players:
        bat_avg = players[player][1] / players[player][0]
        #https://stackoverflow.com/questions/19986662/rounding-a-number-in-python-but-keeping-ending-zeros
        rounded_avg = '{:.3f}'.format(round(bat_avg, 3)) 
        players[player].append(rounded_avg)  

        

makePlayers(filename)
calculateAvg(players)


#https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value    
sorted_players = {k: v for k, v in sorted(players.items(), key=lambda item: item[1][2], reverse= True)}

for player in sorted_players:
    print("%s : %s" % (player, sorted_players[player][2]))
