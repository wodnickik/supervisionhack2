from transformers import AutoTokenizer, DataCollatorWithPadding
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from torch.utils.data import Dataset, DataLoader
import evaluate
import torch
import numpy as np
import pandas as pd
import os

from utils import *

DATA_DIR = './data/'
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

class ImgsDataset(Dataset):

    def __init__(self, split: str):
        # data loading
        if split == 'train':
            df = pd.read_csv(DATA_DIR + 'train_text.csv')
        elif split == 'test':
            df = pd.read_csv(DATA_DIR + 'test_text.csv')

        df = df.dropna(subset=['text'])
        df = df[df['text'].str.len() > 5]

        self.text = list(df['text'])
        self.label = list(df['label'])
        tokenized = tokenizer(self.text, truncation=True)
        self.input_ids = tokenized["input_ids"] 
        self.attention_mask = tokenized["attention_mask"]
        self.n_samples = len(df)

    def __getitem__(self, index):
        return {
            "text": self.text[index],
            "label": self.label[index],
            "input_ids": self.input_ids[index],
            "attention_mask": self.attention_mask[index],
        }

    def __len__(self):
        return self.n_samples

tokenized_dataset_train = ImgsDataset('train')
tokenized_dataset_test= ImgsDataset('test')
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

accuracy = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)

id2label = {0: "good", 1: "bad"}
label2id = {"good": 0, "bad": 1}

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2, id2label=id2label, label2id=label2id
)

training_args = TrainingArguments(
    output_dir="model_text",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    weight_decay=0.01,
    evaluation_strategy="no",
    save_strategy="no",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset_train,
    eval_dataset=tokenized_dataset_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
print(trainer.evaluate())
trainer.save_model("model_text/model_text")
