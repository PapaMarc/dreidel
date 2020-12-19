## Dreidel: enough is enough

<PapaMarc>
Credit for the original, and highly functional code goes to https://github.com/NealJMD/dreidel

On the eve of Sat Dec 12, 2020 at some point post brisket, and latkes... and while we were clearing the table and prep'ing for dessert, the kiddos, BigMama and i along with 4 others (8 players total), started a game of dreidel with 10 pieces of gelt each. After many, many spins while i managed to lose all but 2 pieces (at which point i ate one seeing my impending doom, and with a desire for a taste of diminishing chocolate), 1 other and i were eventually eliminated... however the remaining 6 seemed to neither finish, nor get much closer to finishing. Eventually, a couple glasses of wine later, we all left the game for our return to the table and our dessert.  In short, i was left with what appears to be a notion similar to Neal's... i needed to run some ancestor simulations, and see if this game is winable and just how long one can expect to play before a winner emerges. 

The following day, i did a quick search as one now does and came across many dreidle games; on quick inspection of Neal's code i felt it might be that i'd simply run it and be done. A week, and several million simulations later (often running them overnight while i slept) i felt i should persist a few updates. They amount to the following:
- fyi need to 'pip install matplotlib' before this will run.
- a few simple tweaks which 7 years later were required to run via Python v3.x...
    * had to find/replace xrange() method with range() for Python v3 to mitigate: The “NameError: name ‘xrange’ is not defined” error
    * It then ran for several min (>10min on my old clunker) with no feedback at high (40-60% CPU burn) and then generated error: 'list' object has no attribute 'ndim'... so fixed this via transform using np.array (presume this represented a change in matplotlib in the time which transpired as well)... some surfing seemed to clarify that make_plots expects x and y to be numpy array. 'Passing a list tries to get shape of input by reading ndim attribute of numpy array and fails', or something like that per some stackoverflow entries.
    * will note... also getting a warning wrt cmap=cm.coolwarm  it appears in cm.py that matplotlib has deprecated this sort of support. To be honest, i was less interested in the 3-D plot; so far haven't pursued this non-blocking issue.

And this allowed me to start really running many many simulations. And explore. I really wanted to focus on the sweet spot of # of players (relative to my experience), and pieces reflecting what i'd encountered. And on doing so, found some other issues relative to the more populated arrays in the original code. Accordingly... i addressed this by: change ending_rounds[player_count] --> ending_rounds[ii]  # when you muck with the player arrays and TYPICAL_PLAYER_COUNT, it exposed some issues w/the original code which happened to work as it was but which i believe are more dynamically correct as updated.

From there... i added some instrumentation to see what was going on as the simulations were ongoing. While i also did step through in debug to see how things are really working, as noted doing so across 1 entire game can be tedious, let alone doing so at scale across 100s, let alone K's or 10s of Ks... so some feedback as it's computing was helpful to me. As part of that i added in 'spin' count to make sure i was properly differentiating an individual user's spin, from a round of spins by however many players got through the round prior to/if it resulted in any conclusion for the round let alone the game. And that in turn led me to arrive at what i believe was an understandable flaw in the original code... in the final line graph charting which summarized the overall output (and not in gameplay code itself). Namely, rounds were divided by players not as part of the arrays generation during gameplay, but as part of the final presentation of the data in the charting... underestimating the actual game rounds by said multiple. 
I say this is understandable because... ~100 rounds 'feels' exceedingly long as a player for a game, but would be an answer i suppose we all could accept/imagine as a tangible one v 600 or 900 or 1200.
Yet after 10's of Ks of simulations... the truth is the variance in this game is amazing large which is why i suspect he 'needed' to start with MAX_ROUNDS = 1500 despite (some highly limited # of games, relative to games played) arriving at convergence after ~100 rounds as the code was presented. eg. if you set it at MAX_ROUNDS = 150 (which is 50% overage relative to 100rounds completion) it's not unusual to get 0 games that actually complete after the ~100 rounds are played.

After many simulations it became clear to me (unless my additional instrumentation was incorrect)... that 'typically' the game take MUCH longer than 100 rounds on average IFF you play that long (closer to an order of magnitude more!). If you don't allow for 1500+ rounds, and rather set the MAX_ROUNDS to 250-500 you'll likely find games conclude at ~100rounds ~<20% of the time.
That finally got me to conclude and find/fix what i think was a bug in the line charting which empirically appeared to be (based on the added on screen runtime reporting) that the final chart was dividing the rounds by the number of players... and indeed that was the case in the code. So 'fixed' that which unless i'm offbase was required to get the truth. 
eg.
ending_rounds[plr_idx][amt_idx] = play_many_rounds(TRIAL_COUNT, player_count, starting_amount) / player_count  --> 
ending_rounds[plr_idx][amt_idx] = play_many_rounds(TRIAL_COUNT, player_count, starting_amount)

That, albeit i believe reality, leads to some pretty dismal conclusions about how long (how many rounds) on average a game takes!
And my impression that the original parameters as provided, led to a contrived ~100 rounds a statistically insignificant (low % of the time) outcome and associated conclusion. If one really lets the game play out (which one would rarely do in 'real' life outside the simulation), and doesn't erroneously divide rounds by the number of players... the actual variance of the game is a dramatically high one, and the real limit for the game convergence is on average exceedingly long!
See revised PapaDre(Ancestor)Simulations_*.jpg

To see the extent of the variance, as well as the impact when you artificially limit MAX_ROUNDS (and thus why MAX_ROUNDS needs to be so high to really find convergence)... try these params:
MAX_ROUNDS = 250
TRIAL_COUNT = 1000
as well as these:
MAX_ROUNDS = 5000
TRIAL_COUNT = 1000

All this said, i must conclude:
1) props and many many many thanks to Neal for his superb original simulation code which in itself saved me real work as it functioned quite eloquently. 
2) it can be all too easy to be fooled by statistics, and to arrive at conclusions that more closely support our expectation even with lots of data in hand! Bias can unconciously/unintentionally impact design/implementation (thus the bug). Trust but Verify!! 
3) our ancestors understood that the game was not for them to play and win... but rather for them to keep the kids busy as long they wanted... with a minimal supply of chocolate and clay.
___
(what follows is the original readme.md as posted Jan 6, 2014 per https://github.com/NealJMD/dreidel)
</PapaMarc>

I created this script in November 2013 after playing a Thanksgivukkah game of dreidel with my cousins. Once I realized that the gameplay involves new decision making and that it was going to take forever, I became curious if the game could be expected to converge to one player winning or if it would just go round and round without a victor. I created this script and found that it does in fact converge, after about a hundred rounds around the table for eight starting pieces each. I explored the parameter space and made some graphs. 

The bottom line is if you start with more than eight pieces (10-15 is standard) you're going to be passing that dreidel around the table over a hundred times. I guess it keeps the kids quiet for a long time.