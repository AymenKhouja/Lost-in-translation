
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np



model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def calculate_score(prompt, guess): 
    sentences = [prompt,guess]
    embeddings = model.encode(sentences)
    embedding1 = embeddings[0]
    embedding2 = embeddings[1]
    similarity_score = cosine_similarity([embedding1], [embedding2])[0][0]
    return np.round(similarity_score*10,0)

class Player:
    def __init__(self, name):
        self.player_name = name
        self.score = {}
        self.prompts = {}
        self.guesses = {}
        

def update_playing_team(current_team, current_round, teams, user_prompt):
    try:
        teams[current_team - 1]["prompts"]["Round " + str(current_round)].append(user_prompt)
        teams[current_team - 1]["score"]["Round " + str(current_round)].append(0)
        teams[current_team - 1]["guesses"]["Round " + str(current_round)].append("---")
    except:
        teams[current_team - 1]["prompts"]["Round " + str(current_round)] = [user_prompt]
        teams[current_team - 1]["score"]["Round " + str(current_round)] = [0]
        teams[current_team - 1]["guesses"]["Round " + str(current_round)] = ["---"]
    return teams

def update_score(teams, current_guesser, current_round, score, guess):
    try:
        teams[current_guesser - 1]["score"]["Round " + str(current_round)].append(score)
        teams[current_guesser - 1]["guesses"]["Round " + str(current_round)].append(guess)
        
    except: # the case in which the guesser haven't played before - we need to initiliase the attributes
        
        teams[current_guesser - 1]["prompts"]["Round " + str(current_round)] = []
        teams[current_guesser - 1]["score"]["Round " + str(current_round)] = [score]
        teams[current_guesser - 1]["guesses"]["Round " + str(current_round)] = [guess]
        
    return teams

facts = [
    "AI image generation involves the use of artificial intelligence techniques to create or manipulate images.",
    "Generative Adversarial Networks (GANs) consist of a generator and a discriminator network competing to create realistic images.",
    "Variational Autoencoders (VAEs) are another AI technique employed for image generation.",
    "AI-generated images find applications in art, entertainment, and design, enabling the creation of unique visual content.",
    "DeepDream, a Google project, uses AI to generate surreal and abstract images from existing ones.",
    "Style transfer algorithms apply the artistic style of one image to another using AI.",
    "In medical imaging, AI image generation is used to generate synthetic MRI scans for training AI models.",
    "AI-generated images aid in data augmentation for computer vision tasks, enhancing the diversity of training data.",
    "Video games utilize AI image generation to create realistic environments and characters.",
    "Models like DALL-E are capable of generating images from textual descriptions.",
    "NVIDIA leverages AI to upscale video game graphics in real-time.",
    "AI image generation assists in restoring and enhancing old or damaged photographs.",
    "Fashion design benefits from AI-generated clothing designs and patterns.",
    "Lifelike avatars for virtual reality and online interactions are created using AI-generated images.",
    "AI image generation contributes to generating maps and landscapes for video games and simulations.",
    "In the automotive industry, AI image generation is employed to simulate and test autonomous driving scenarios.",
    "AI-generated images play a role in creating realistic architectural renderings and designs.",
    "Ethical concerns arise as AI image generation can be used to create deepfake videos and misleading content.",
    "Researchers continually explore new possibilities and challenges in AI image generation.",
]
