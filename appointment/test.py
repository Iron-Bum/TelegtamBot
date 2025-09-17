import pandas as pd
import datetime
lst1 = (1,2,3)
lst2 = [4,5,6]
lst3 = (7,8,9)
lst4 = [10,11,12]

a = pd.Series([lst1, lst2], ['B', 'V'], )
b = pd.Series([lst3, lst4], ['B', 'V'])
c = a+b
print(c)


