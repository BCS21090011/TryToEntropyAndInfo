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

#Example for how to use:
if __name__=="__main__":
    #Create a dictionary that contains data, the data needed is in pandas.DataFrame datatype:
    data:dict={
        "Age":[36,24,26,29,24,30,29,24,24,28,55,60,59,60],
        "Years worked":[12,0,1,2,1,4,21,20,2,5,35,40,39,37],
        "Gender":["Male","Female","Male","Male","Female","Male","Male","Female","Female","Male","Male","Female","Female","Male"],
        "Working hour":[12,8,8,10,8.5,8,8,8,8,0,6,7.5,7,7],
        "Able to join the company vacation":[False,False,True,False,True,True,False,True,False,False,True,False,True,True]
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

    predct:numpy.ndarray=obj.Predict(inputs=[[26,2,1,8]])

    print(f"The prediction is: {int(predct)}")