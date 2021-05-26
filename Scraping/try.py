import sys

try:
    x
except:
    print('No x')
    sys.exit(1)
print('Something else!')
