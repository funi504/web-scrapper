import requests
from PIL import Image
from io import BytesIO
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
import time

# Function to download image
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    return img

# Function to preprocess the image
def preprocess_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(250),  # EfficientNet-B7 expects larger images
        transforms.CenterCrop(250),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return preprocess(image).unsqueeze(0)

# Function to get image embeddings using a pre-trained ResNet model
def get_image_embedding(model, image):
    with torch.no_grad():
        model.eval()
        embedding = model(image)
    return embedding

# Function to compare embeddings using cosine similarity
def compare_embeddings(embedding1, embedding2):
    cosine_similarity = nn.CosineSimilarity(dim=1, eps=1e-6)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity.item()

# Load pre-trained EfficientNet-B7 model and remove the final classification layer
efficientnet_model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
resnet_model = nn.Sequential(*list(efficientnet_model.children())[:-1])  # Remove the classification layer

# Example usage
amazon_image_url = 'https://i5-images.massmart.co.za/asr/57c94410-9433-4c4c-82fd-064fa8d297e5.1ea0f9768bc3599a3663a16af55c00c2.jpeg'
makro_image_url = 'https://i5-images.massmart.co.za/asr/3a067d37-284a-4c5a-928b-210c9e285e7c.5ea820a7226e6ca1797098d522b6e746.jpeg'

# Download and preprocess images
amazon_image = preprocess_image(download_image(amazon_image_url))
other_store_image = preprocess_image(download_image(makro_image_url))

similar_products = []
def get_similar_products(reference_product , all_products):

    reference_image_embedding = get_image_embedding(resnet_model ,preprocess_image(download_image(reference_product['image_url'])))

    for product in all_products:
        image_embedding = get_image_embedding(resnet_model,preprocess_image(download_image(product['image_url'])))
        similarity_score = compare_embeddings(reference_image_embedding , image_embedding)

        if similarity_score >= 0.8:
            similar_products.append(product)

        elif similarity_score >= 0.5 and product['store'] != reference_product['store']:
            similar_products.append(product)

    return similar_products

"""
start = time.time()
# Get image embeddings
amazon_embedding = get_image_embedding(resnet_model, amazon_image)
other_store_embedding = get_image_embedding(resnet_model, other_store_image)
end = time.time()

print(f'finished with ai stuff : {end - start} ')
# Compare embeddings
similarity_score = compare_embeddings(amazon_embedding, other_store_embedding)
print(f"Cosine Similarity: {similarity_score}")
print(f'finished comparing : {time.time() - end }')
# Define a threshold for similarity (1 means identical, 0 means completely different)
similarity_threshold = 0.8  # Adjust based on your needs
if similarity_score >= similarity_threshold:
    print("The images are likely the same.")
else:
    print("The images are different.")

"""

