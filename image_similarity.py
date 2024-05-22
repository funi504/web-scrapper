import requests
from PIL import Image
from io import BytesIO
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
import numpy as np

# Function to download image
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    return img

# Function to preprocess the image
def preprocess_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
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

# Load pre-trained ResNet model and remove the final classification layer
resnet_model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
resnet_model = nn.Sequential(*list(resnet_model.children())[:-1])  # Remove the classification layer

# Example usage
amazon_image_url = 'https://m.media-amazon.com/images/I/61TFeIzdtgL._AC_UL320_.jpg'
image_url2 = 'https://m.media-amazon.com/images/I/71mwjqWWUxL._AC_UL320_.jpg'

# Download and preprocess images
amazon_image = preprocess_image(download_image(amazon_image_url))
other_store_image = preprocess_image(download_image(image_url2))

# Get image embeddings
amazon_embedding = get_image_embedding(resnet_model, amazon_image)
other_store_embedding = get_image_embedding(resnet_model, other_store_image)

# Compare embeddings
similarity_score = compare_embeddings(amazon_embedding, other_store_embedding)
print(f"Cosine Similarity: {similarity_score}")

# Define a threshold for similarity (1 means identical, 0 means completely different)
similarity_threshold = 0.8  # Adjust based on your needs
if similarity_score >= similarity_threshold:
    print("The images are likely the same.")
else:
    print("The images are different.")



