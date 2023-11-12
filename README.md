# Lost in translation 

## Introduction 🎉

Welcome to the Lost in Translation game Repository! 🚀 This repository contains a fun game laveraging generative AI, specifically Stable-diffusion and Stable Diffusion XL to provide an engaging and fun adversial, gartic-style game.

The primary aim of this repository is to share a game that showcases the capability of Generative AI and collaborate on improving a fun game that involve state of the art models in AI 🌟


Lost in translation gets its name from the fact that the stable diffusion model may not always be accurate and the generated image at times may not represent the prompt as accurately as possible, therefore there is information lost in translation procss (the translation in this case being text to image)

## Description 📑

### Game Modes:
Lost in Translation offers two distinct modes of play. In Individual Mode, players navigate the challenge on their own, while Team Mode introduces a collaborative dimension. In Team Mode, players decide team sizes and the number of rounds, setting the stage for an engaging collective experience.

### Team Mode Setup:
Team Mode puts the decision-making in the hands of players. Choose how many members will form each team and determine the number of rounds per game. A round, defined by a sequence of turns, adds an element of strategy to the gameplay.

### The Loop of Lost in translation:
Lost in translation's core revolves around a continuous loop of communication and prediction. A player from a team begins by providing an enigmatic prompt to the AI. The opposing team then uses the generated image to predict the original prompt, earning points based on the accuracy of their sentence. This process alternates until every team member has contributed a prompt at least once.

### Scoring and Strategy:
After each round, scores for each prompt are revealed. This dual scoring system highlights both the team's ability to craft challenging prompts and their adeptness at interpreting AI-generated images. The game concludes with an overall score presentation, showcasing each team's cumulative performance.

### Repository files: 
The repository contains many files, all created to make the distinction between different elements that are then joined together in the LostInTranslation.py
  * GameLogic.py : contains important functionalities such as how to calculate scores, and how to update scores, as well as a Player class in which relevant information is stored for the player or the team (in team mode) 
  * ServerLogic.py : Contains important functionalities that allows the webapp to function such as storing important info in session to use later and updating session when necessary.
  * ImageGeneration.py : Contains important Functionalities regarding the image generation process, in it there are different functions to generate images using two different APIs - Hugging face's api or WizModel's api, as well as generating using the diffusers package if a powerful gpu is available.
  * LostInTranslation: Contains the structure of the web app, and brings everything together nicely to make the game funtion. Keep in mind that in this file, we are assuming that to generate the image you are using Wizmodel's apî (as seen through the code) this could be changed however through the code, or by further tuning to the code in ImageGeneration.py to allow further flexibility, or by changing the arguments that the function gets.
## Usage 🚀

To use this app, simply make a pull request or download the app, after providing a wizmodel api key you can enjoy the game with your friends. 📝

## Requirements 🛠️

The projects in this repository are implemented using Python, leveraging the diffusers, sentence_transformers, sklearn and Flask libraries (as well as libraries such as numpy, os, random, PIL, requests and more). Ensure that you have the necessary libraries and dependencies installed before running the LostInTranslation.py file.

## Contributions 🤝

Contributions, suggestions, and bug reports are highly encouraged! If you have any feedback or wish to contribute to the project, please open an issue or submit a pull request. Your collaboration is valued! 🙌


