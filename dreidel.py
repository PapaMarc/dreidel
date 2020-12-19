import random
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

#MAX_ROUNDS = 1500
MIN_STARTING_AMOUNT = 2
MAX_STARTING_AMOUNT = 20
MIN_PLAYER_COUNT = 2
MAX_PLAYER_COUNT = 9
TYPICAL_PLAYER_COUNT = 7
#TRIAL_COUNT = 300

MAX_ROUNDS = 5000
TRIAL_COUNT = 1000

GRAPH_PLAYER_OFFSETS = [-2,0,2]
GRAPH_PLAYER_COLORS = ['b', 'g', 'y']

def main():
#	starting_amounts = [x for x in range(MIN_STARTING_AMOUNT, MAX_STARTING_AMOUNT+1)]
	starting_amounts = [8,9,10]
#	player_counts = [x for x in range(MIN_PLAYER_COUNT, MAX_PLAYER_COUNT+1)]
	player_counts = [5,7,9]
	ending_rounds = [[0 for y in range(0, len(starting_amounts))] for x in range(0, len(player_counts))]
	for amt_idx, starting_amount in enumerate(starting_amounts):
		for plr_idx, player_count in enumerate(player_counts):
#			ending_rounds[plr_idx][amt_idx] = play_many_rounds(TRIAL_COUNT, player_count, starting_amount) / player_count
			ending_rounds[plr_idx][amt_idx] = play_many_rounds(TRIAL_COUNT, player_count, starting_amount)

	make_plots(np.array(ending_rounds), np.array(starting_amounts), np.array(player_counts))

def make_plots(ending_rounds, starting_amounts, player_counts):
	""" graph the results """
	fig = plt.figure()

	# show 3d surface
	ax = fig.add_subplot(1,2,1,projection='3d')
	# ax = fig.gca(projection='3d')
	X, Y = np.meshgrid(starting_amounts, player_counts)
	ax.plot_surface(X, Y, ending_rounds, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=False)
	ax.set_xlabel("starting pieces per player")
	ax.set_ylabel("number of players")
	ax.set_zlabel("rounds to convergence")
	ax.set_title("Rounds to dreidel convergence")

	# show line graphs of starting amount v. ending round for several different player counts
	ax = fig.add_subplot(1, 2, 2)
	for ii in range(0, len(GRAPH_PLAYER_OFFSETS)):
		player_count = TYPICAL_PLAYER_COUNT+GRAPH_PLAYER_OFFSETS[ii]
		ax.plot(starting_amounts, ending_rounds[ii], GRAPH_PLAYER_COLORS[ii], label="%i players" % player_count)
	ax.legend(loc=0)
	ax.set_xlabel("starting pieces per player")
	ax.set_ylabel("rounds to convergence")
	ax.set_title("Rounds to dreidel convergence")

	plt.show()

def play_many_rounds(trial_count, player_count, starting_amount):
	""" run trail_count games of dreidel with player_count players, each starting with 
		starting_amount coins. go until the game converges to one player winning all the pieces
		and return the average ending round.
	"""
	scores = {}
	ending_round = []
	spins=0
	players = [x for x in range(0, player_count)]
	for trials in range(0,trial_count):
		pot = len(players)
		print ("[%-20s] %d%% of games against {0} played".format(TRIAL_COUNT) % ('='*1*int(trials/(TRIAL_COUNT/20.1)), int(((trials/TRIAL_COUNT)*100)+1)), end = '\r')   # added this progress bar to get a sense of completion, particularly if you try to bump up TRIAL_COUNT dramatically. Heck-- what's an ancestor simulation without running it 10K times :-)
		for p in players:
			scores[p] = starting_amount
		for r in range(0,MAX_ROUNDS):
			for p in players:
				if scores[p] <= 0:
					continue
				roll = random.randint(1, 4)
				spins +=1
				if roll == 1: # Gimmel (get them all)
					scores[p] += pot
					pot = 0
				elif roll == 2: # Shin (give one)
					scores[p] -= 1
					pot += 1
				elif roll == 3: # Hay (get half)
					amount = math.floor(pot/2)
					scores[p] += amount
					pot -= amount
				else: # Nun (nothing)
					pass # nothing
				if pot <= 0: # if pot is empty, all ante up
					for p in players:
						scores[p] -= 1
						if scores[p] < 0:
							scores[p] = 0
						else: pot += 1
			non_zero_players = 0
			for p in players:
				if scores[p] > 0:
					non_zero_players += 1
			if non_zero_players < 2:
				ending_round.append(r)
				break
	if len(ending_round) < 1: return 0
	print ("")
	print("Players: {0}; Gelt/player: {1}; Array: {2}; {3}of{4}gamesFinishedWithin{5}rounds; AvgRnds/game: {6}; AvgSpins/game:{7}".format(len(players), starting_amount, (ending_round), len(ending_round), TRIAL_COUNT, MAX_ROUNDS, (mean(ending_round)), (spins/(len(ending_round)))))
	return mean(ending_round)

def mean(l):
	return sum(l)/len(l)


if __name__ == '__main__':
	main()