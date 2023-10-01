# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 19:36:46 2023

@author: aymen
"""
from ImageGeneration import generate_image
from GameLogic import *
from ServerLogic import *
from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import random
import os


api_key = "<YOUR_HF_OR_WIZMODEL_API_KEY>"



app = Flask(__name__)
app.secret_key = "My_very_awesome_key" + str(np.random.randint(0, 19000))
IMAGE_FOLDER = os.path.join('static', 'image')
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER




    
@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        selected_mode = request.form.get('game-mode')
        if selected_mode == "team":
            return redirect(url_for('welcome_team'))
        elif selected_mode == "individual": 
            return redirect(url_for('welcome_indiv'))
    return render_template('game_type.html')


@app.route('/team_config', methods=['GET', 'POST'])
def welcome_team():
    if request.method == 'POST':
        initiliase_team_mode()
        print("Teams initiliased!")
        return redirect(url_for("phase1"))
    return render_template('welcome_team.html')

@app.route('/indiv_config', methods=['GET', 'POST'])
def welcome_indiv():
    if request.method == 'POST':
        initiliase_player_mode()
        return "game stared on indiv mode"
    return render_template('welcome_indiv.html')

@app.route('/phase1', methods=['GET', 'POST'])
def phase1():
    
    teams, current_team, current_prompts, current_round = restore_session(elements_values_dict = {"teams":2,
                                                                         "current_team":1,
                                                                         "current_round_prompt":[],
                                                                         "current_round":1})
    i = np.random.randint(0, 19)
    if request.method == 'POST':
        # get the prompt from the html form
        user_prompt = request.form.get('prompt')
        # append the prompt chosen to the list of prompts that the player made
        current_prompts += [user_prompt]
        update_playing_team(current_team, current_round,teams,user_prompt)
        full_filepath = generate_image(api_key, user_prompt,IMAGE_FOLDER,n_steps = 30,api="wizmodel")
        
        
        update_session(elements = ["current_round_prompts", "prompt", "img_path", "teams", "current_team", "current_guesser"],
            values = [current_prompts, user_prompt, full_filepath, teams, current_team, 1 if current_team != 1 else 2])
        return redirect(url_for('phase2'))
    return render_template('phase1.html', current_player=current_team, fact = facts[i])

    

@app.route('/phase2', methods=['GET', 'POST'])
def phase2():
    
    img, prompt, current_team, teams, num_players, current_guesser = restore_session(elements=['img_path','prompt',
                                                                             'current_team', "teams", "num_players", "current_guesser"])
    current_player, prompts, current_round = restore_session(elements_values_dict = {"current_player":1,"prompts" : {}, "current_round" :1 })
    
    if current_guesser > len(teams):  # Change to 2 players
        current_team += 1
        if current_team > len(teams):
            current_team = 1
            current_player +=1 
            if current_player > num_players:
                current_team = 1
                current_player = 1
                prompts["Round " + str(current_round)] = session.get("current_round_prompts")
                current_round += 1
                update_session(elements=["current_round_prompts","current_round","current_team","current_player"],
                               values=[[], current_round, current_team, current_player])
                return redirect(url_for('roundover'))
        update_session(elements = ["current_team", "current_player", "current_round"],
                       values = [current_team, current_player, current_round])
        return redirect(url_for('phase1'))
    
    
    if request.method == 'POST':
        user_guess = request.form.get('guess')
        score = calculate_score(prompt, user_guess)
        teams = update_score(teams, current_guesser, current_round, score, user_guess)
        current_guesser += 1
        if current_guesser == current_team:
            current_guesser += 1
        
        update_session(elements = ["current_guesser","teams"],
                       values = [current_guesser, teams])
        return redirect(url_for('phase2'))

    return render_template('phase2.html', img=img, current_guesser=current_guesser)


@app.route('/gameover', methods=['GET', 'POST'])
def gameover():
    
    teams, prompts = restore_session(elements = ["teams", "prompts"])
    if request.method == "POST": 
        return(redirect(url_for('gallery')))
    return render_template('gameover.html', players=teams, prompts = prompts)

@app.route('/roundover', methods=['GET', 'POST'])
def roundover():
    
    teams, current_round, prompts, num_rounds = restore_session(elements = ["teams", "current_round", "prompts", "num_rounds"])
    current_prompts = prompts["Round " + str(current_round - 1)]
    print(teams,current_round,prompts,num_rounds)
    if request.method == 'POST':
        if current_round > num_rounds: 
            return redirect(url_for('gameover'))
        else: 
            return redirect(url_for('phase1'))
    
    return render_template('roundover.html', players=teams, current_round = current_round -1, prompts = current_prompts)

@app.route('/gallery', methods = ["GET", "POST"])
def gallery():
    prompts = session["prompts"]
    if request.method == "POST": 
        app.secret_key = str(random.randint(1,100000))
        return(redirect(url_for('welcome')))
    return render_template("gallery.html", prompts = prompts)


if __name__ == "__main__":
    app.run(debug = True)
