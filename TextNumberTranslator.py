textToNum = {'A': 10, 'B': 11, 'C': 12, 'D':13, 'E':14, 'F': 15, 'G': 16, 'H':17, 'I':18, 'J':19, 'K':20, 'L':21, 'M':22, 'N':23, 'O':24,
             'P':25, 'Q':26, 'R':27, 'S':28,'T':29, 'U':30, 'V': 31, 'W':32, 'X':33, 'Y':34, 'Z':35, ' ':36};
numToText = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
             'Y', 'Z', ' '];
def translateIntoNum(text:str):
    text = text.upper();
    numString = "";
    for char in text:
        if char not in numToText:
            print("Error: invalid character. Please use only letters and space.");
            return None;
        numString = str(textToNum[char]) + numString;
    return int(numString);
        
def translateIntoText(num:int):
    text = "";
    while (num > 0):
        charNum = num % 100;
        #adjust to match up with how numToText is indexed
        charNum -= 10;
        if (charNum < 0 or charNum >= len(numToText)):
            print("Error: invalid character. Please use properly encoded text.");
            return None;
        text += numToText[charNum];
        num = num // 100;
    return text;