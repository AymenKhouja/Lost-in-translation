from GameLogic import Player
from flask import  request, session



def initiliase_team_mode(): 
    num_teams = int(request.form['num-teams'])
    num_players = int(request.form['num-players'])
    num_rounds = int(request.form['num-rounds'])
    teams = [Player(f"Team {i + 1}").__dict__ for i in range(num_teams)]  # Change to 2 players
    session["teams"] = teams
    session["num_players"] = num_players
    session["num_rounds"] = num_rounds


def initiliase_player_mode():
    num_players = int(request.form['num-players'])
    num_rounds = int(request.form['num-rounds'])
    players = [Player(f"Team {i + 1}").__dict__ for i in range(num_players)]  # Change to 2 players
    session["players"] = players
    session["num_rounds"] = num_rounds

def restore_session(elements= [],initial_values = [], elements_values_dict = {}): 
    if type(elements) is list and any(elements):
        values = ()
        with_init = type(initial_values) is list and any(initial_values)
        if with_init: 
            assert len(elements) == len(initial_values), "Initial values list length should be equal to the number of elements"
        for i, var in enumerate(elements):
            if with_init :
                if var in session:
                    value = session.get(var)
                    values += (value,)
                else:
                    value = initial_values[i]
                    session[i] = value
                    values += (value,)
            else:
                value = session.get(var, f"{var} not in session")
                values += (value,)
        return values
    if elements == None or elements == []:
        assert initial_values == None or initial_values == [], "Initial values provided but elements list is empty"
        assert any(elements_values_dict), "No elements provided"
        values = ()
        for key,item in elements_values_dict.items():
            if key in session:
                value = session.get(key)
                values += (value,)
            else: 
                session[key] = item
                values += (item,)
        return values
    elif type(elements) is str:
        with_init = initial_values != None
        if with_init: 
            if elements in session:
                var = session.get(elements)
            else:
                var = initial_values
                session[i] = var
                values += (var,)
        else:
            var = session.get(elements, f"{var} not in session")
        return var
    
def update_session(elements = [],values = [], elements_values_dict = {}):
    
    if type(elements) is list and any(elements):
        for i, item in enumerate(elements):
            session[item] = values[i]
            
    if elements == None or elements == []:
        assert values == None or values == [], "values list provided but elements list is empty"
        assert any(elements_values_dict), "No elements provided"

        for key,item in elements_values_dict.items():
            session[key] = item
            
    if type(elements) is str:
        session[elements] = values
