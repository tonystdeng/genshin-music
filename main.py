import sys

'''if __name__!="__main__":
    raise RuntimeError("This script should be run directly and not imported as a module.")'''

# make sure console argument are valid
if len(sys.argv)!=2:
    print("One Command Line Arguments Expected: \"main.py <filename>\"")
    sys.exit()
else:
    import play
    if play.play(sys.argv[1]):
        print("\nAn error encountered, program stoped.")
    else:
        print("\nSound sequence finished, program exited.\n")