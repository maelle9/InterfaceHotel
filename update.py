import pandas as pd

def update(stars_choice,date_choice,adulte_choice,enfant_choice,room_choice):
    df = pd.read_csv("test_carte.csv", sep=";")
    df = df.drop(['gps'], axis=1)
    if stars_choice == 10:
        df = df
    else:
        df = df[(df['stars']==stars_choice)]
    if date_choice == "all" :
        df = df
    else:
        df = df[(df['start_date']==date_choice)]
    if adulte_choice == 10:
        df = df
    else:
        df = df[(df['nb_adulte']==adulte_choice)]
    if enfant_choice ==10:
        df = df
    else:
        df = df[(df['nb_enfant']==enfant_choice)]
    if room_choice == 10:
        df = df
    else:
        df = df[(df['nb_chambre']==room_choice)]
    df = df.drop(['nb_adulte','nb_enfant','nb_chambre'], axis=1)
    data=df.to_dict('records')
    return data