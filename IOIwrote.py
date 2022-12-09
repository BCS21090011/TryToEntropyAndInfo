'''IOIwrote.py is a Python script that contains several functions for reading and validating user input. The script
defines four functions: ReadInt, ReadFloat, ReadStr, and YNDecision.

The ReadInt function is used to read an integer from the user. The function takes an optional prompt string and optional
minimum and maximum values as arguments. If the user enters a value that is not an integer or is outside the specified
range, the function will display an error message and prompt the user to try again.

The ReadFloat function is similar to the ReadInt function, but it is used to read a floating-point number from the user.
The function takes the same arguments as ReadInt and has the same validation and error-handling behavior.

The ReadStr function is used to read a string from the user. The function takes an optional prompt string and a list of
valid strings as arguments. If the user enters a string that is not in the list of valid strings, the function will
display an error message and prompt the user to try again.

The YNDecision function is used to ask the user to make a yes/no decision. The function takes an optional prompt string
as an argument and returns a boolean value indicating whether the user chose "yes" or "no".

The if __name__ == "__main__" block at the end of the script contains an example of how to use these functions. It
repeatedly prompts the user to enter an integer and a floating-point number, and then asks the user if they want to exit
the program. If the user chooses "no", the loop will continue and the user will be prompted to enter new values. If the
user chooses "yes", the loop will exit and the program will end.

Overall, the functions in IOIwrote.py provide a convenient way to read and validate user input in a Python program. They
can be useful for ensuring that the user enters valid data and for handling errors gracefully.

By: ChatGPT
Date: 2022/12/09 18:59
'''

def ReadInt(qstStr:str="",inMin:int=None,inMax:int=None)->int:
    valid:bool=False
    userInput:int

    while valid==False:
        try:
            userInput=int(input(qstStr))
            valid=True

            if inMin!=None:
                if userInput<inMin:
                    valid=False

            if inMax!=None:
                if userInput>inMax:
                    valid=False

        except ValueError:
            valid=False

        if valid==False:
            print("Invalid input!")

    return userInput

def ReadFloat(qstStr:str="",inMin:float=None,inMax:float=None)->float:
    valid:bool=False
    userInput:float

    while valid==False:
        try:
            userInput=float(input(qstStr))
            valid=True

            if inMin!=None:
                if userInput<inMin:
                    valid=False

            if inMax!=None:
                if userInput>inMax:
                    valid=False

        except ValueError:
            valid=False

        if valid==False:
            print("Invalid input!")

    return userInput

def ReadStr(qstStr:str="", validStr:list=None)->str:
    valid:bool=False
    userInput:str=""

    while valid==False:

        userInput=input(qstStr)

        if userInput in validStr:
            valid=True

        else:
            print("Invalid input!")

    return userInput

def YNDecision(decisionStr:str="")->bool:
    userInput:str=ReadStr(qstStr=decisionStr,validStr=['y','Y','n','N'])

    if userInput in ['y','Y']:
        return True

    else:
        return False

if __name__ == "__main__":

    exit:bool=False

    while exit==False:

        userInput = ReadInt("int Input: ")
        print("User's int inputed: ", userInput)
        userInput = ReadFloat("float Input: ")
        print("User's float inputed: ", userInput)
        exit=YNDecision(decisionStr="Exit? (Y/N)\n")

    input()