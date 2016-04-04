import log_update
import time

f = log_update.stdout

f('x')
time.sleep(0.25)

f('y')
time.sleep(0.25)

f('z')
time.sleep(0.25)

f('''    a
    b
    c''')
time.sleep(0.25)

f('g')
time.sleep(0.25)

spin = log_update.spinner()
for i in range(100):
    f(spin())
    time.sleep(80 / 1000)
