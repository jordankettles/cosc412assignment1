from operator import mod
from sympy import *

init_printing() 
p = 190836086241037
q = 569824609824697

e = 436217

secret_message = 98400072373862522893031464992

# Compute d so that de = 1 mod N

N = (p * q)
phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)

print("d: ", d)
# The secret_message m^e mod pq where m is a positive integer less than pq.
# What is m?

m = pow(secret_message, d, mod=N)

# m = Mod(v, N)
# m = Mod(v, N)
print("m: ", m)