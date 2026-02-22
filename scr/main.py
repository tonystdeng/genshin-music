import time
import asyncio
'''if __name__!="__main__":
    raise RuntimeError("This script should be run directly and not imported as a module.")'''

import settings
import play


print("Counting down for", settings.settings["countdown"])
for i in range(settings.settings["countdown"]):
    print(i+1)
    time.sleep(1)


result = asyncio.run(play.play(settings.settings))
if result == 1:
    print("\nAn error encountered, program stoped.")
elif result == 2:
    print("\nProgram exited.")
else:
    print("\nSound sequence finished, program exited.\n")