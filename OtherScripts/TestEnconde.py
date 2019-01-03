from sklearn import preprocessing

le = preprocessing.LabelEncoder()
le.fit(["paris", "paris", "tokyo", "amsterdam"])

print(le.classes_)

label = le.transform(["paris","amsterdam","tokyo"])

print(label)