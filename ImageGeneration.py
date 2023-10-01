import requests
from PIL import Image
from io import BytesIO
import os
import json
import base64


instructions = "((masterpiece)), ((beautiful)), 4k, realistic, ((cinematic photo:1.3)),((best quality)), long shot, ((low light:1.4)), vignette, highly detailed, high budget Hollywood movie, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy"
negative_prompt = "worst quality, normal quality, low quality, low res, blurry, text, watermark, logo, banner, extra digits, cropped, jpeg artifacts, signature, username, error, sketch, duplicate, ugly, monochrome, horror, geometry, mutation, disgusting."



def generate_wizmodel_api(key, text, n_steps, instructions, negative_prompt, high_noise_frac):

    url = "https://api.wizmodel.com/sdapi/v1/txt2img"
    prompt = text + instructions
    payload = json.dumps({
        "prompt": f"{prompt}",
        "steps": n_steps,
        "denoising_strength" : high_noise_frac,
        "ngative_promot" : negative_prompt,
        'sd_model_name' : "sd_xl_base_1.0"
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
    except Exception as e:
        print("error occurred in", e)
    image = get_image_from_response(response, "wizmodel")
    return image
    


def get_image_from_response(response, api):
    assert api == "hugging face" or api == "wizmodel", "Only supported APIs are the hugging face api and the wizmodel API"
    if api == "hugging face":
        if response.status_code == 200:
            try:
                image = Image.open(BytesIO(response.content))
            except Exception as e:
                print("Image creation: error occurred in", e)
                image = None
    else:
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
                        image = Image.open(BytesIO(image_data))
                          
                    except Exception as e:
                        print(f"Image creation : error occured in {e}")
            else:
                print("No images found in the API response")
        else:
            print(f"Request failed with status code: {response.status_code}")
    return image

def generate_hf_api(api_key, text):
    url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Send request to Hugging Face API
    data = {"inputs": text}

    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        print("error occurred in", e)

    image = get_image_from_response(response, "hugging face")
    return image


def generate_image(api_key, user_prompt, IMAGE_FOLDER, instructions = instructions, negative_prompt = negative_prompt,
                   n_steps = None, model = None, refiner = None, high_noise_frac = 0.5, api = None, **kwargs):
    prompt = user_prompt
    if model == None and api != None:
        if api  == "hugging face":
            image = generate_hf_api(api_key, prompt)
        else:
            image = generate_wizmodel_api(api_key, prompt, n_steps, instructions, negative_prompt, high_noise_frac)
    else: 
        assert n_steps != None, "provide number of inference steps"
        if refiner == None:
            image = model(prompt = prompt,
                        num_inference_steps=n_steps,
                        **kwargs
                        ).images[0]
        else:
            image = model(
                prompt=prompt + instructions,
                num_inference_steps=n_steps,
                negative_prompt = negative_prompt,
                denoising_end=high_noise_frac,
                output_type="latent",
                **kwargs
            ).images
            image = refiner(
                prompt=prompt + instructions,
                num_inference_steps=n_steps,
                negative_prompt = negative_prompt,
                denoising_start=high_noise_frac,
                **kwargs,
                image=image,
            ).images[0]
    full_filepath = os.path.join(IMAGE_FOLDER, f"{user_prompt}.jpg")
    image.save(full_filepath)
    
    return full_filepath