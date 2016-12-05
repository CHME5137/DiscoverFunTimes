print("This will show up in your output.log file")
import sys
print("This will show up in your error.log file",file=sys.stderr)
raise Exception("This error message will show up in your error.log file")
