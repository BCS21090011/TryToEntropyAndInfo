import math

import numpy
import pandas as pd
from sklearn import tree
from matplotlib import pyplot as plt

def InfoCalc(probability: float) -> float:
    info: float = 0

    if probability > 0:
        info: float = probability * math.log(probability, 2)

    return info

def EntropyCalc(probabilities: list) -> float:
    entro: float = 0

    for prob in probabilities:
        entro -= InfoCalc(probability=prob)

    return entro

class TreeDiagramer():
    def __init__(self,datas:pd.DataFrame,outputColmn:str=None,saveFigFileName:str=None):  #Put in the dataset.
        self.Dataset=datas
        self.GettingInfoFromDataset()
        self.MappingDataset()

        if outputColmn!=None:
            self.TreeDiagramingDataset(outputColmn=outputColmn,absltFileName=saveFigFileName)

    def GettingInfoFromDataset(self):
        self.Colmns: list = self.Dataset.columns.tolist()   #Get the columns.

        #Get the variables in each column:
        self.Variables: list = []

        for clmn in self.Colmns:
            tmp:list=(self.Dataset[clmn].drop_duplicates().tolist())
            self.Variables.append(tmp)

    def MappingDataset(self):
        changesCol:list=[]
        varDict:list=[]
        self.MappedDataset:pd.DataFrame=self.Dataset.copy()

        for i in range(len(self.Colmns)):
            if all(((type(var) is not int) and (type(var) is not float)) for var in self.Variables[i]): #If all variables in the column is neither int nor float:
                changesCol.append(self.Colmns[i])
                numVar:list=list(range(len(self.Variables[i]))) #This will create a list with values from 0 until the number of variables of the column.

                #If the type is bool then make sure True is 1 and False is 0:
                if all((type(var) is bool) for var in self.Variables[i]):
                    if True in self.Variables[i]:
                        numVar[self.Variables[i].index(True)]=1
                    if False in self.Variables[i]:
                        numVar[self.Variables[i].index(False)]=0

                tmpDict:dict=dict(zip(self.Variables[i],numVar))
                varDict.append(tmpDict)
                self.MappedDataset[self.Colmns[i]]=self.MappedDataset[self.Colmns[i]].map(tmpDict)

        #Save all the changes into dictionary:
        self.DataVarStrToNumerc:dict={
            "Column changes":changesCol,
            "Changes":varDict
        }

    def TreeDiagramingDataset(self,outputColmn:str,absltFileName:str=None):
        self.featrs:list=self.Colmns.copy()

        if outputColmn in self.featrs:
            self.featrs.remove(outputColmn) #Remove the output column from the mapped dataset.

            self.treeDgrmXVals=self.MappedDataset[self.featrs]
            self.treeDgrmYVals=self.MappedDataset[outputColmn]

            self.treeDgrm=tree.DecisionTreeClassifier()
            self.treeDgrm=self.treeDgrm.fit(self.treeDgrmXVals.values,self.treeDgrmYVals.values)    #Fit only the values.

            tree.plot_tree(self.treeDgrm,feature_names=self.featrs)

            if absltFileName!=None:
                plt.savefig(absltFileName)

    def Predict(self,inputs:list):  #This method can be used to make predictions using the decision tree.
        return self.treeDgrm.predict(inputs)

    def ReplacedValues(self,clmn:str,var:str)->int:
        if clmn in obj.DataVarStrToNumerc["Column changes"]:  #Check if the column is replaced.
            indeces: int = obj.DataVarStrToNumerc["Column changes"].index(clmn) #Find the index of column in DataVarStrToNumerc.
            index:int= obj.DataVarStrToNumerc["Changes"][indeces][var]  #Find the values represent the variable.
            return index

    def OriginalValues(self,clmn:str,val:int):
        if clmn in obj.DataVarStrToNumerc["Column changes"]:  # Check if the column is replaced.
            indeces: int = obj.DataVarStrToNumerc["Column changes"].index(clmn)
            var=next(k for k,v in obj.DataVarStrToNumerc["Changes"][indeces].items() if v==val) #Use the next() function to find the key with the given value
            return var

#Example for how to use:
if __name__=="__main__":
    #Create a dictionary that contains data, the data needed is in pandas.DataFrame datatype:
    data:dict={
        "Age":[36,24,26,29,24,30,29,24,24,28,55,60,59,60],
        "Years worked":[12,0,1,2,1,4,21,20,2,5,35,40,39,37],
        "Gender":["Male","Female","Male","Male","Female","Male","Male","Female","Female","Male","Male","Female","Female","Male"],
        "Working hour":[12,8,8,10,8.5,8,8,8,8,0,6,7.5,7,7],
        "Able to join the company vacation": ["No","No","Yes","No","Yes","No","Yes","Yes","No","No","Yes","No","Yes","Yes"]
    }

    print("The data is make out by random with no mean to harm anyone:")

    df:pd.DataFrame=pd.DataFrame(data)  #Create a pandas.DataFrame with datas in the dictionary.
    obj=TreeDiagramer(df,outputColmn="Able to join the company vacation",saveFigFileName="TreeDiagram.png")    #Create an object of GetInfoDataFrame with df as Dataset.

    print("The dataset:")
    print(obj.Dataset)

    print("\n\n\nThe variables replaced:")
    reprs:pd.DataFrame=pd.DataFrame(obj.DataVarStrToNumerc)
    print(reprs)

    print("The mapped dataset:")
    print(obj.MappedDataset)

    #Make predictions:
    import IOIwrote as IO
    retryPredict:bool=True

    print("Making predictions:")

    while retryPredict==True:   #If user choose to retry.
        userInput:list=[[]]

        for clmn in obj.featrs: #For every column in features.
            print(f"Column: [{clmn:^16}]:")
            if clmn in obj.DataVarStrToNumerc["Column changes"]:    #Check if the column is replaced.
                for var in obj.Variables[obj.featrs.index(clmn)]:   #For every variable of the column.
                    index:int=obj.ReplacedValues(clmn=clmn,var=var) #Find the replaced value of the variable.
                    print(f"Index: [{index:>3}]:[{var:^16}]")
                userInput[0].append(IO.ReadInt(qstStr="Input the index: ",inMin=0,inMax=len(obj.Variables[obj.featrs.index(clmn)])))
            else:
                userInput[0].append(IO.ReadFloat(qstStr="Input: "))

        predctOutput:int=int(obj.Predict(inputs=userInput))
        predctOutputVar=obj.OriginalValues(clmn="Able to join the company vacation",val=predctOutput)   #Finde the original variable of the replaced value.
        print(f"The prediction output is: {predctOutputVar}")

        retryPredict=IO.YNDecision(decisionStr="Try to predict again? (Y/N)\n")