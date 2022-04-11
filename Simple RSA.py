import math
import random
from TextNumberTranslator import *

def probPrimeTest(p): #implements Fermat's Little Theorem probabilistic primality test.
    if (pow(2, p - 1, p) == 1):
        return True
    return False

def randPrime(): #generates a random 50-digit prime number. Uses probabilistic primality test.
    lowerBound = 10**49 + 1
    upperBound = 10**50
    prime = random.randrange(lowerBound, upperBound, 2); #generate random 50-digit odd number
    while (not probPrimeTest(prime)):
        prime = random.randrange(lowerBound, upperBound, 2)
    return prime

#implementation of Euclidean Algorithm. finds the gcd of two integers.
def gcd(a:int, b:int):
    if (a == 0 or b == 0):
        print ("Error: division by 0 in gcd");
        return None
    r = a % b
    if (r == 0):
        return b
    return gcd(b, r);

#implementation of Extended Euclidean Algorithm.
#given two positive integers a and b, finds integers x and y such that ax + by = gcd(a, b).
#returns a list containing x, y, and the gcd.
#A proper implementation of this would be able to handle zeroes and negative integers; but it'll probably
#only get passed positive ints in this program, so it isn't built for those special cases.
def extendedEE(r0, r1):
    if (r1 == 0 or r0 == 0):
        return [1, 0, r0]
    #initial values for "2 steps previously" x and y, "1 step previously" x and y.
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    #compute first remainder and quotient.
    r2 = r0 % r1
    quotient = r0 // r1
    while (r2 != 0):
        #update the xs and ys so that, whatever the current r2 is, it can be written as a linear combination of a and b.
        x0, x1 = x1, x0 - (quotient * x1)
        y0, y1 = y1, y0 - (quotient * y1)
        
        r0 = r1
        r1 = r2
        r2 = r0 % r1
        quotient = r0 // r1
    return [x1, y1, r1]


def primeSieve(n:int):
    #lists all primes up to n, which is a positive integer.
    if (n < 0):
        print("Error: negative number used in prime sieve.")
        return None
    #True marks a prime number; False marks a composite. numbers are presumed prime until shown otherwise.
    boolList = [True] * (n+1)
    #list of all primes seen so far.
    primeList = []
    
    currNum = 2;
    while (currNum <= n):
        primeList.append(currNum)
        #eliminate multiples of currNum by marking them False in boolList.
        i = currNum * 2
        while (i <= n):
            boolList[i] = False
            i += currNum
        #find next prime number, i.e. next one still marked True in boolList.
        i = currNum + 1
        while (i <= n):
            if(boolList[i]):
                currNum = i
                break
            i += 1
        #if the loop above reached the end of the list before breaking, it must have failed to find another prime,
        #so the function should terminate and return the list of primes seen so far.
        if (i > n):
            return primeList
def factorizeModulus(modulus:int):
    #finds the two prime factors of a modulus; returns them in a list.
    
    #gets a list of primes up to the square root of the modulus; these will be used for trial division.
    root = math.floor(math.sqrt(modulus))
    primes = primeSieve(root)
    
    #trial division on the modulus; first, finds the prime less than the root which divides the modulus, then uses that
    #to find the other prime. Returns a list containing both prime factors.
    factors = [];
    i = 0
    while (i < len(primes)):
        if (modulus % primes[i] == 0):
            factors.append(primes[i])
            factors.append(modulus // primes[i])
            break
        i += 1
    return factors
def findPublicExponent(p:int, q:int):
    #find public exponent, a number relatively prime to (p-1)(q-1)
    pqProd = (p-1) * (q-1)
    public = 3
    while (gcd(public, pqProd) != 1):
        public += 2
    return public

def findPrivateExponent(public:int, p:int, q:int):
    #find private exponent, a number D providing a solution to the linear Diophantine equation:
    #          ED = 1 + k(p-1)(q-1)
    #where E is the public exponent and k is a natural number; uses the Extended Euclidean Algorithm.
    pqProd = (p-1) * (q-1)
    euclidAlgOutput = extendedEE(public, pqProd)
    private = euclidAlgOutput[0]
    #a negative private key won't work. Thankfully, for linear Diophantine equations, given some number x0 such that
    #ax0 + by0 = c
    #we can always find other solutions by adding (b / gcd(a, b)) to x0.
    while (private < 0):
        private += pqProd
    return private

def genKeys(p:int, q:int):
    #find public exponent, a number relatively prime to (p-1)(q-1)
    public = findPublicExponent(p, q)
    #find private exponent, a number D providing a solution to the linear Diophantine equation:
    #          ED = 1 + k(p-1)(q-1)
    #where E is the public exponent and k is a natural number; uses the Extended Euclidean Algorithm.
    private = findPrivateExponent(public, p, q)
    modulus = p * q
    print("Your public key is {}. Your public modulus is {}. Your private key is {}.".format(public, modulus, private))
def encryptDecrypt (key:int, modulus:int, message:int):
    #takes in a key, the public modulus (pq), and a message (a natural number less than the modulus).
    #can be used for encryption or decryption--operations are the same either way.
    
    #checks that the parameters fit the conditions above.
    if (message < 0):
        print("Message is a negative number. Please try again with a positive number.")
    if (message >= modulus):
        print("Message too large. Please try again with a message smaller than the modulus.")
        return None
    if (key < 0):
        print("Key is negative. Try again with a positive key.")
        return None
    if (modulus < 0):
        print("Modulus is negative. Try again with a positive modulus.")
        return None
    #raises the message to power given by the key, then reduces with the modulus.
    #returns the resulting value.
    return pow(message, key, modulus)

def breakEncryption(public:int, modulus:int, message:int):
    #given a message, modulus, and public exponent, decodes the message. Begins by factoring the modulus to find
    #the 2 primes that were used to generate it. Then uses those primes and the public key to generate a working
    #private key. Finally, uses the private key to return a decrypted message.
    if (message < 0):
        print("Message is a negative number. Please try again with a positive number.")
    if (message >= modulus):
        print("Message too large. Please try again with a message smaller than the modulus.")
        return None
    if (public < 0):
        print("Key is negative. Try again with a positive key.")
        return None
    if (modulus < 0):
        print("Modulus is negative. Try again with a positive modulus.")
        return None
    #factorizes modulus.
    modFactors = factorizeModulus(modulus)
    #generates private exponent.
    privateKey = findPrivateExponent(public, modFactors[0], modFactors[1])
    #decrypts message and returns it.
    return (message**privateKey) % modulus

isRunning = True;
while (isRunning):
    userChoice = input("Welcome to Simple RSA! Enter 'gen' to generate keys, 'enc' to encrypt, 'dec' to decrypt, 'brk' to break, 'q' to quit.");
    if (userChoice == 'gen'):
        userChoice = input("Enter 'rand' to randomly generate your primes, and 'choose' to enter primes of your choice.");
        if (userChoice == 'rand'):
            prime1 = randPrime()
            prime2 = randPrime()
            print("Your secret primes are: {}, {}".format(prime1, prime2))
            genKeys(prime1, prime2)
        elif(userChoice == 'choose'):
            prime1 = int(input("Enter first prime..."))
            while ((not probPrimeTest(prime1)) or (prime1 <= 0)):
                print("Value entered is not positive or not prime. Please try again.")
                prime1 = int(input("Enter first prime..."))
            prime2 = int(input("Enter second prime..."));
            while ((not probPrimeTest(prime2)) or (prime2 <= 0)):
                print("Value entered is not positive or not prime. Please try again.")
                prime2 = int(input("Enter second prime..."))
            genKeys(prime1, prime2);
        else:
            print("Invalid input. Please try again.");
    elif (userChoice == 'enc'):
        pubKey = int(input("Enter public key/public exponent..."))
        pubMod = int(input("Enter public modulus..."))
        userChoice = input("Enter 'text' to encrypt text and anything else to encrypt a number.")
        if (userChoice == 'text'):
            textInput = input("Enter text message (only letters and space are allowed)...")
            plaintext = translateIntoNum(textInput)
        else:
            plaintext = int(input("Enter numerical message..."))
        print("Your encrypted message is:")
        print(encryptDecrypt(pubKey, pubMod, plaintext));
    elif (userChoice == 'dec'):
        privKey = int(input("Enter private key/private exponent..."))
        pubMod = int(input("Enter public modulus..."))
        userChoice = input("Enter 'text' if message should be translated into text, and anything else if not.")
        ciphertext = int(input("Enter message..."))
        print("Your decrypted message is:")
        if (userChoice == 'text'):
            print(translateIntoText(encryptDecrypt(privKey, pubMod, ciphertext)))
        else:
            print(encryptDecrypt(privKey, pubMod, ciphertext))
    elif (userChoice == 'brk'):
        pubKey = int(input("Enter public key/public exponent..."))
        pubMod = int(input("Enter public modulus..."))
        ciphertext = int(input("Enter message..."))
        print("Your decrypted message is:")
        print(breakEncryption(pubKey, pubMod, ciphertext));
    elif (userChoice == 'sign'):
        privKey = int(input("Enter private key/private exponent..."))
        pubMod = int(input("Enter public modulus..."))
        toSign = int(input("Enter message to be signed..."))
        print("Your signed message is:")
            print(encryptDecrypt(privKey, pubMod, toSign))
    elif (userChoice == 'ver'):
        pubKey = int(input("Enter public key/public exponent..."))
        pubMod = int(input("Enter public modulus..."))
        expected = int(input("Enter the message that was sent to be signed..."))
        signed = int(input("Enter the signed message..."))
        if (encryptDecrypt(pubKey, pubMod, signed) == expected):
            print("Verified; sender of the signed message must have had the relevant private key.")
        else:
            print("Not verified; sender of the signed message may not have had the relevant private key.")
    elif (userChoice == 'q'):
        isRunning = False
    else:
        print("Invalid input. Please try again.")
        
