import time
from pistonapi import PistonAPI
start = time.time()
# Create a new Piston API instance
piston = PistonAPI()
# Execute your own code!
code = 'print("Hello, World!")'
print(piston.execute(language="py", version="3.10.0", code=code))
end= time.time()
print(f"Execution time: {end - start} seconds")