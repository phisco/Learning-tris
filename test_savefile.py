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
    
print recovered_history
