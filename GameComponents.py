# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 19:29:23 2023

@author: aymen
"""
from flask import Flask, render_template, request, redirect, url_for, session


def welcome_screen():
    if request.method == 'POST':
        selected_mode = request.form.get('game-mode')
        if selected_mode == "team":
            return redirect(url_for('welcome_team'))
        elif selected_mode == "individual": 
            return redirect(url_for('welcome_indiv'))
    return render_template('game_type.html')

def team_config():
    if request.method == 'POST':
        initiliase_team_mode()
        print("Teams initiliased!")
        return redirect(url_for("phase1"))
    return render_template('welcome_team.html')