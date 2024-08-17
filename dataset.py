import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import torch.nn.functional as F
from datasets import load_dataset
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from models import EnhancedCNN
import pandas as pd

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device found: {device}")

def log_transform(df, numeric_features, non_log_features):
    df_logs = np.log10(df[list(set(numeric_features) - set(non_log_features))] + 1)
    df_combined = pd.concat([df_logs, df[non_log_features]], axis=1)
    return df_combined

def normalize_data(tensor, mean, std):
    return (tensor - mean) / std

def preprocess_data(dataset):
    print("Preprocessing Dataset.")
    df_train = pd.DataFrame(dataset['train'])
    df_test = pd.DataFrame(dataset['test'])

    non_numeric = ['is_sm_ips_ports', 'is_ftp_login']
    features = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl', 'sload', 
                'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 
                'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth', 
                'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 
                'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 
                'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports']

    numeric_features = list(set(features) - set(non_numeric))
    non_log = ['sttl', 'dttl', 'swin', 'dwin', 'trans_depth', 'ct_state_ttl', 'ct_flw_http_mthd']

    df_train_numeric = log_transform(df_train, numeric_features, non_log)
    df_test_numeric = log_transform(df_test, numeric_features, non_log)

    X_train_tensor = torch.tensor(df_train_numeric.values, dtype=torch.float32)
    X_test_tensor = torch.tensor(df_test_numeric.values, dtype=torch.float32)

    train_mean = X_train_tensor.mean(dim=0)
    train_std = X_train_tensor.std(dim=0)

    X_train_tensor = normalize_data(X_train_tensor, train_mean, train_std)
    X_test_tensor = normalize_data(X_test_tensor, train_mean, train_std)

    y_train_tensor = torch.tensor((df_train['attack_cat'] != 'Normal').astype(int).values, dtype=torch.float32)
    y_test_tensor = torch.tensor((df_test['attack_cat'] != 'Normal').astype(int).values, dtype=torch.float32)

    return X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor

# DataLoader creation
def create_dataloaders(X_train, y_train, X_test, y_test, batch_size=64):
    print("Creating Dataloader.")
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader

# Model Training
def train_model(model, train_loader, num_epochs=10, learning_rate=0.002):
    print("Training Model.")
    model = model.to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.unsqueeze(1).to(device), labels.unsqueeze(1).to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)

        epoch_loss = running_loss / len(train_loader.dataset)
        print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}')

# Model Evaluation
def evaluate_model(model, test_loader):
    print("Evaluating Model.")
    model.eval()
    y_pred = []
    y_true = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.unsqueeze(1).to(device), labels.to(device)
            outputs = model(inputs)
            predicted = (outputs > 0.5).float()
            y_pred.extend(predicted.squeeze().tolist())
            y_true.extend(labels.tolist())

    y_pred = np.array(y_pred)
    y_true = np.array(y_true)

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

# Main Execution
if __name__ == "__main__":
    dataset = load_dataset("Mouwiya/UNSW-NB15-small")
    X_train, X_test, y_train, y_test = preprocess_data(dataset)
    train_loader, test_loader = create_dataloaders(X_train, y_train, X_test, y_test)

    model = EnhancedCNN()
    train_model(model, train_loader)
    evaluate_model(model, test_loader)

    torch.save(model.state_dict(), 'models/enhanced_cnn_model.pth')
