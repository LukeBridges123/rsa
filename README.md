# rsa
This is a simple demo of the RSA encryption system. It can encrypt and decrypt numbers and small amounts of text (size limited by the size of the key), as well as create and verify digital signatures. The modulus is generated using user-chosen primes or 2 randomly-generated 50-digit primes, both generated using the Fermat primality test, and then the public and private exponents are generated using the Euclidean and Extended Euclidean Algorithms. 


This is, of course, not particularly secure; the keys aren't very long compared to the keys one might use in an actual implementation of RSA, and the Python documentation explicitly recommends that you do not use the "random" module's pseudorandom number generator for cryptographic purposes. However, since it was made purely for fun and not for any actual use, I'm content to just leave in those flaws.
