import pickle
""" This small test program reads the pickled history from the local file
"savefile" and outputs it through print

""" 
recovered_history = []
savefile = open("savefile.p", "rb")
while True:
    try:
        recovered_history += (pickle.load(savefile))
    except EOFError:
        break

i = 0
print ''
while True:
    try:
        if(recovered_history[i][0] != 0):
            print "Player",recovered_history[i][0], "won."
        else:
            print "The game was a draw."

        
        print "The moves were: ", recovered_history[i][1]
        print ''
        i+=1
    except IndexError:
        break
