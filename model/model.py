from transformers import pipeline
import torch
from torchvision import transforms
import torch.nn as nn
import numpy as np
from PIL import Image
from typing import Optional, Tuple
from model.utils import get_img_text, get_link_features

device = torch.device("cpu")

class NeuralNetLinks(nn.Module):
    """
    Neural network for link features
    """
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNetLinks, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, hidden_size)
        self.linear4 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.linear1(x)
        out = self.relu(out)
        out = self.linear2(out)
        out = self.relu(out)
        out = self.linear3(out)
        out = self.relu(out)
        out = self.linear4(out)
        return out

# text model
text_model = pipeline("sentiment-analysis", model="model/model_text/model_text")

# resnet model
resnet_model = torch.load('model/model_res/model_res.pt').to(device)
resnet_model.eval()

# link model
link_model = NeuralNetLinks(9, 100, 2).to(device)
link_model.load_state_dict(torch.load('model/model_link/model_link.pt'))
link_model.eval()

mean = np.array([0.5, 0.5, 0.5])
std = np.array([0.25, 0.25, 0.25])

id2label = {0: "good", 1: "bad"}

resnet_preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
])


def predict_text(text: str) -> Tuple[str, float]:
    """
    Get classification of text
    :param text: text to classify
    :return: label and confidence
    """
    return text_model(text)[0]['label'], text_model(text)[0]['score']


def predict_res(img: str) -> Tuple[str, float]:
    """
    Get classification of image
    :param img: path to image
    :return: label and confidence
    """
    img = Image.open(img).convert('RGB')
    img_preprocessed = resnet_preprocess(img)
    img_tesor = torch.unsqueeze(img_preprocessed, 0)
    out = resnet_model(img_tesor)
    out = torch.nn.functional.softmax(out, dim=1)
    confidence, preds = torch.max(out, 1) 
    return id2label[abs(preds[0].item() - 1)], confidence.item()


def predict_link(link: str) -> Tuple[str, float]:
    """
    Get classification of link
    :param link: link to classify
    :return: label and confidence
    """
    link_tensor = torch.from_numpy(np.array(get_link_features(link))).to(torch.float32)
    out = link_model(torch.unsqueeze(link_tensor, 0))
    out = torch.nn.functional.softmax(out, dim=1)
    confidence, preds = torch.max(out, 1)
    return id2label[preds[0].item()], confidence.item()


def predict(
    img: str, # image path
    link: str, # dst link
    add_text: Optional[str] = None, # additional text (if facebook post)
) -> Tuple[str, float]:
    """
    Get classification based on image, text and link
    :param img: path to image
    :param link: link to classify
    :param add_text: additional text (if facebook post)
    :return: label and confidence
    """
    res_label, res_confidence = predict_res(img)
    img_text = get_img_text(img)
    if add_text:
        img_text += " " + add_text
    text_label, text_confidence = predict_text(img_text)
    link_label, link_confidence = predict_link(link)
    # print("resnet:", res_label, res_confidence)
    # print("text:", text_label, text_confidence)
    # print("link:", link_label, link_confidence)
    res_confidence = res_confidence * 0.5
    if res_label == text_label and text_label == link_label:
        final_label = res_label
        final_confidence = (res_confidence + text_confidence + link_confidence) / 2.5
    else:
        if res_label == text_label:
            final_label = res_label
            final_confidence = (res_confidence + text_confidence - link_confidence) / 2.5
        elif res_label == link_label:
            final_label = res_label
            final_confidence = (res_confidence + link_confidence - text_confidence) / 2.5
        elif text_label == link_label:
            final_label = text_label
            final_confidence = (text_confidence + link_confidence - res_confidence) / 2.5
    return final_label, final_confidence
