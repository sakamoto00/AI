#Sean Wang
#CSE 415
#Assignment 1
#Winter 2018

import random

#The function to determine the answer to the user's Ask input
#return true if n-k is divisible by m, false elsewise
def is_n_minus_k_divisible_by_m(n, k, m):
    if ((n - k) % m) == 0:
        return True
    return False

#The function to determine if the user's input in Ask part is legal
#Returns true if the input m is less than 1000 and meanwhile prime number, false elsewise
def isPrimeUnder1000(m):
    if m >= 1000:
        return False
    for i in range(2, m-1):
        if m % i == 0:
            return False;
    return True;

#The main module, include the user I/O interaction and system feedback
#Generate the final score printed when the program ends
def run_Guess_My_Number():
    n = random.choice(range(1000))
    print (n)
    round = 0
    score = 100
    while True:
        round = round + 1
        textInput1 = input('You Want To Ask, Guess or Quit?')
        if textInput1 == 'Quit':
            print('Your score is 0!')
            print('Good luck next time')
            return None;
        if textInput1 == 'Ask':
            print('Fill in: If we subtract _ from n, is the result divisible by _ (prime number) ?')
            textInput2 = input('seperate by one single space : ')
            inputList = textInput2.split()
            k = int(inputList[0])
            m = int(inputList[1])
            if isPrimeUnder1000(m) and 0 <= k and k < m:
                if is_n_minus_k_divisible_by_m(n, k, m):
                    print('Yes, the secret number minus', k, 'is divisable by ', m)
                else:
                    print('Ah oh, it does not work')
            else:
                print('The numbers are invalid (should 0 <= first < second and second should be prime)')
        if textInput1 == 'Guess':
            textInput2 = input('Your guess is: ')
            if int(textInput2) == n:
                print('You win! Your score is ', int(score))
                return None
            else:
                print('You are incorrect, try again')   
        score = score * 0.9  

#run main program
if __name__ == '__main__':
  run_Guess_My_Number()
