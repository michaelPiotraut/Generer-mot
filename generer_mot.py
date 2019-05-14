#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random as rd


# In[2]:


#Extraction des données
dictionnaire = pd.read_csv("lexique382.tsv", sep ="\t")


# In[3]:


# Création du vecteur contenant tous les mots (on supprime les valeurs manquantes et les doublons)
mots = dictionnaire.ortho.dropna().unique()

# Ajout du caractère ' ' à la fin des mots pour marquer la fin
for i in range(mots.shape[0]):
    mots[i] = mots[i] + ' '

# Cleaning de la data en remplacant les caractères spéciaux ou rares par des caractères plus communs
mots_clean = []
for mot in mots:
    mot_clean = mot
    for lettre in mot:
        if lettre == 'ã' or lettre == 'â' or lettre == 'à':
            mot_clean = mot_clean.replace(lettre, 'a')
        if lettre == 'ï' or lettre == 'î' or lettre == 'ï':
            mot_clean = mot_clean.replace(lettre, 'i')
        if lettre == 'û' or lettre == 'ù' or lettre == 'ü':
            mot_clean = mot_clean.replace(lettre, 'u')
        if lettre == '-' or lettre == '.':
            mot_clean = mot_clean.replace(lettre, '')
        if lettre == 'ö' or lettre == 'ô':
            mot_clean = mot_clean.replace(lettre, 'o')
        if lettre == 'ñ':
            mot_clean = mot_clean.replace(lettre, 'n')
    mots_clean.append(mot_clean)
#print(mots_clean)


# In[4]:


# Création d'une liste regroupant les caractères utilisés
carac = set()
for mot in mots_clean:
    for lettre in mot:
        carac.add(lettre)
carac = list(carac)
ind_fin = carac.index(' ')
#print(carac)
#print(ind_fin)


# In[5]:


# Création d'un tenseur de dimension 2, les lignes et les colonnes représentent les lettres dans l'ordre de carac
# À l'intersection [i][j] se trouve le nombre de fois que la lettre en j se trouve après la lettre en i
arr1 = np.zeros([len(carac), len(carac)])
for mot in mots_clean:
    for i in range(len(mot) - 1):
        indice_lettre = carac.index(mot[i])
        indice_suivante = carac.index(mot[i + 1])
        arr1[indice_lettre][indice_suivante] += 1


# In[6]:


# Création d'un tenseur de dimension 3, les dimensions représentent les lettres dans l'ordre de carac
# À l'intersection [i][j][k] se trouve le nombre de fois que la lettre en k se trouve après la lettre en i et j
arr2 = np.zeros([len(carac), len(carac), len(carac)])
for mot in mots_clean:
    if len(mot) > 2:
        for i in range(len(mot) - 2):
            indice_lettre = carac.index(mot[i])
            indice_plus1 = carac.index(mot[i + 1])
            indice_plus2 = carac.index(mot[i + 2])
            arr2[indice_lettre][indice_plus1][indice_plus2] += 1


# In[7]:


# Modification de arr1 en divisant chaque entrée par la somme de la ligne
# afin d'avoir une somme qui vaut 1 
i = 0
arr_fin1 = []
for row in arr1:
    arr_temp = []
    somme = sum(row)
    if somme != 0:
        for item in row:
            arr_temp.append(item/somme)
        arr_fin1.append(arr_temp)
    else:
        arr_fin1.append(row)
arr_fin1 = np.array(arr_fin1)


# In[8]:


# Modification de arr2 en divisant chaque entrée par la somme de la rangée
# afin d'avoir une somme qui vaut 1 
i = 0
arr_fin2 = []
for col in arr2:
    arr_temp2 = []
    for row in col:
        arr_temp1 = []
        somme = sum(row)
        if somme != 0:
            for item in row:
                arr_temp1.append(item/somme)
            arr_temp2.append(arr_temp1)
        else:
            arr_temp2.append(row)
    arr_fin2.append(arr_temp2)
arr_fin2 = np.array(arr_fin2)
#print(arr_fin2[0][2])
#print(arr2[0][2])


# In[9]:


# Création de deux listes qui regroupent la proba cumulée des lettre et leur indice dans carac pour vision 1
arr_cum1 = []
arr_ind1 = []
for i, row in enumerate(arr_fin1):
    arr_ind_temp = []
    arr_cum_temp = []
    som = 0
    for j, item in enumerate(row):
        if item > 0:
            som += item
            arr_ind_temp.append(j)
            arr_cum_temp.append(som)
    arr_ind1.append(arr_ind_temp)
    arr_cum1.append(arr_cum_temp)
#print(arr_ind1)
#print(arr_cum1)


# In[10]:


# Création de deux matrices qui regroupent la proba cumulée des lettre et leur indice dans carac pour vision 2
arr_cum2 = []
arr_ind2 = []
for i, col in enumerate(arr_fin2):
    arr_ind_temp2 = []
    arr_cum_temp2 = []
    for j, row in enumerate(col):
        arr_ind_temp1 = []
        arr_cum_temp1 = []
        som = 0
        for k, item in enumerate(row):
            if item > 0:
                som += item
                arr_ind_temp1.append(k)
                arr_cum_temp1.append(som)
        arr_ind_temp2.append(arr_ind_temp1)
        arr_cum_temp2.append(arr_cum_temp1)
    arr_ind2.append(arr_ind_temp2)
    arr_cum2.append(arr_cum_temp2)
#print(arr_ind2)
#print(arr_cum2)


# In[11]:


# Création d'une liste des caractères par lesquels commencent un mot
arr_temp = np.zeros([len(carac)])
for mot in mots_clean:
    indice = carac.index(mot[0])
    arr_temp[indice] += 1
arr_deb = arr_temp/sum(arr_temp)

arr_ind_pre = []
arr_cum_pre = []
somme = 0
for i, el in enumerate(arr_deb):
    if el != 0:
        somme += el
        arr_ind_pre.append(i)
        arr_cum_pre.append(somme)
#print(arr_deb)
#print(arr_cum_pre)
#print(arr_ind_pre)


# In[12]:


# Génération des mots aléatoires

def generer():
    word = []

    # Génération première lettre
    alea = rd.random()
    for i, car in enumerate(arr_cum_pre):
        if alea <= car:
            seed = arr_ind_pre[i]
            break
    word.append(carac[seed])

    # Génération deuxième lettre
    alea = rd.random()
    for i, car in enumerate(arr_cum1[seed]):
        if alea <= car:
            seed = arr_ind1[seed][i]
            break

    # Génération lettres suivantes

    cond = True
    while cond:
        word.append(carac[seed])
        let_prec1 = carac.index(word[-1])
        let_prec2 = carac.index(word[-2])
        alea = rd.random()
        for i, car in enumerate(arr_cum2[let_prec2][let_prec1]):
            if alea <= car:
                seed = arr_ind2[let_prec2][let_prec1][i]
                break
        if seed == ind_fin:
            cond = False
    
    for let in word:
        print(let, end = '')


# In[16]:


generer()

