import math
import pandas as pd
from sklearn import tree

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

class GetInfoDataFrame():
    def __init__(self,datas:pd.DataFrame):  #Put in the dataset.
        self.Dataset=datas

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

    def TreeDiagramingDataset(self,outputColmn:str):
        self.featrs:list=self.Colmns

        if outputColmn in self.featrs:
            self.featrs.remove(outputColmn) #Remove the output column from the mapped dataset.

            self.treeDgrmXVals=self.MappedDataset[self.featrs]
            self.treeDgrmYVals=self.MappedDataset[outputColmn]

            self.treeDgrm=tree.DecisionTreeClassifier()
            self.treeDgrm=self.treeDgrm.fit(self.treeDgrmXVals,self.treeDgrmYVals)

            tree.plot_tree(self.treeDgrm,feature_names=self.featrs)