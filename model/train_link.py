import pandas as pd
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from utils import get_link_features


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# hyperparameters
input_size = 9
hidden_size = 100
num_classes = 2
num_epochs = 100
batch_size = 32
learning_rate = 0.001

# links = pd.read_csv('data/links_big.csv')
links = pd.read_csv('data/links.csv')
links_features = links['url'].apply(get_link_features).to_list()
links_features_df = pd.DataFrame(links_features, columns=[
    'is_https_in_domain', 'is_https', 'has_double_slash', 'has_at', 'has_numbers_in_domain',
    'count_dots', 'count_slashes', 'count_dashes', 'has_ip'
])
links_features_df['label'] = links['label']

trainX, testX, trainY, testY = train_test_split(
    links_features_df.drop('label', axis=1),
    links_features_df['label'],
    test_size=0.2,
    random_state=42
)

class LinksDataset(Dataset):

    def __init__(self, split: str):
        # data loading
        if split == 'train':
            self.x = torch.from_numpy(trainX.values).to(torch.float32)
            self.y = torch.from_numpy(trainY.values)
        elif split == 'test':
            self.x = torch.from_numpy(testX.values).to(torch.float32)
            self.y = torch.from_numpy(testY.values)
        
        self.n_samples = self.x.shape[0]

    def __getitem__(self, index):
        sample = self.x[index], self.y[index]
        return sample
    
    def __len__(self):
        return self.n_samples
    
train_dataset = LinksDataset(split='train')
test_dataset = LinksDataset(split='test')

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size,
                                           shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size,
                                           shuffle=False)

class NeuralNetLinks(nn.Module):
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
    
model = NeuralNetLinks(input_size=input_size, hidden_size=hidden_size, num_classes=num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for i, (features, labels) in enumerate(train_loader):
        features = features.to(device)
        labels = labels.to(device)

        # forward
        outputs = model(features)
        loss = criterion(outputs, labels)

        # backwards
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f'epoch {epoch+1}/{num_epochs}, loss = {loss.item()}')

# testing
with torch.no_grad():
    n_correct = 0
    n_samples = 0
    for features, labels in test_loader:
        features = features.to(device)
        labels = labels.to(device)
        outputs = model(features)

        _, predictions = torch.max(outputs, -1)
        n_samples += labels.shape[0]
        n_correct += (predictions == labels).sum().item()

    acc = 100* n_correct/n_samples
    print(f'accuracy: {acc}')

torch.save(model.state_dict(), 'model_link/model_link.pt')