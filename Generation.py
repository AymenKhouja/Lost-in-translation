# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 06:20:33 2023

@author: aymen
"""

import requests
from PIL import Image
from io import BytesIO


def get_image_from_response(response):
    try:
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        print("Image creation: error occurred in", e)
        image = None
    return image

def generate(api_key, text):
    url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Send request to Hugging Face API
    data = {"inputs": text}

    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        print("error occurred in", e)

    return response

text = "puppy dog running on grass"
hf_api_key = "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"

response = generate(hf_api_key, "black spiderman")


import json
import requests
import base64
from PIL import Image
from io import BytesIO

key =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTYxNTI5NjMsInVzZXJfaWQiOiI2NTE5M2Q4MjE4ZDNiNzZjMDQyMjk3NmMifQ.0w7LP-iEJOzWi8r6HnZfcmWmPIXQvmWztYrRgwmQZG0"

url = "https://api.wizmodel.com/sdapi/v1/txt2img"

prompt = "a red monkey with an elephant head"

payload = json.dumps({
    "prompt": f"cinematic film still, 4k, realistic, ((cinematic photo:1.3)) of {prompt}, Fujifilm XT3, long shot, ((low light:1.4)), ((looking straight at the camera:1.3)),  somber, shallow depth of field, vignette, highly detailed, high budget Hollywood movie, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
    "steps": 30,
    "denoising_strength" : 0.5,
    "ngative_promot" : "worst quality, normal quality, low quality, low res, blurry, text, watermark, logo, banner, extra digits, cropped, jpeg artifacts, signature, username, error, sketch, duplicate, ugly, monochrome, horror, geometry, mutation, disgusting.",
    'sd_model_name' : "sd_xl_base_1.0"
})

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + key
}

response = requests.post(url, headers=headers, data=payload)

# Check if the response is successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    response_data = response.json()

    # Extract the list of base64 encoded images
    images_list = response_data.get('images', [])

    # Check if there are images in the list
    if images_list:
        # Convert each base64 encoded image to bytes and open it as an image
        for i, base64_image in enumerate(images_list):
            try:
                image_data = base64.b64decode(base64_image)
                img = Image.open(BytesIO(image_data))
                  # Display the image
            except Exception as e:
                print(f"Error displaying image {i + 1}: {str(e)}")
    else:
        print("No images found in the API response")
else:
    print(f"Request failed with status code: {response.status_code}")
