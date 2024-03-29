# -*- coding: utf-8 -*-
"""Logistic regression usign pytorch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CZjWSUu2Ga-pwPi_ZdFn7Sekk7WvQf5G
"""

import torch
import torchvision.transforms as transforms
from torchvision import datasets

train_dataset = datasets.MNIST(root='./data',train = True,
                               transform = transforms.ToTensor(),download = True)
test_dataset = datasets.MNIST(root='./data',train = False,
                              transform = transforms.ToTensor())

print("number of training samples: "+str(len(train_dataset))+"\n"+"number of testing samples: "+str(len(test_dataset)))

print("datatype of the 1st training sample:",train_dataset[0][0].type())
print("size of the 1st training sample:",train_dataset[0][0].size())

#check the label of first two training sample
print("label of the first training sample:",train_dataset[0][1])
print("label of the second training sample:",train_dataset[1][1])

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib
import matplotlib.pyplot as plt
img_5 = train_dataset[0][0].numpy().reshape(28,28)
plt.imshow(img_5,cmap='gray')
plt.show()
img_0=train_dataset[0][1].numpy().reshape(28,28)
plt.imshow(img_0,cmap='gray')
plt.show()

!pip install matplotlib-venn

import matplotlib.pyplot as plt
img_5 = train_dataset[0][0].numpy().reshape(28,28)
plt.imshow(img_5,cmap = 'gray')
plt.show()
img_0 = train_dataset[1][0].numpy().reshape(28,28)
plt.imshow(img_0,cmap = 'gray')
plt.show()

from torch.utils.data import DataLoader
#load train and test data samples into dataloader
batach_size = 32
train_loader = DataLoader(dataset = train_dataset,batch_size =batach_size,shuffle = True)
test_loader = DataLoader(dataset = test_dataset,batch_size=batach_size,shuffle = False)

#build custom module for logistic regression
class LogisticRegression(torch.nn.Module):
  def __init__(self,n_inputs,n_outputs):
    super(LogisticRegression,self).__init__()
    self.linear=torch.nn.Linear(n_inputs,n_outputs)
  def forward(self,x):
    y_pred = torch.sigmoid(self.linear(x))
    return y_pred

n_inputs = 28*28
n_outputs = 10
log_regr = LogisticRegression(n_inputs,n_outputs)

#defining the optimizer
optimizer = torch.optim.SGD(log_regr.parameters(),lr=0.001)
#defining Cross-Entropy loss
criterion = torch.nn.CrossEntropyLoss()

epochs = 50
Loss = []
acc = []
for epoch in range(epochs):
  for i,(images,labels) in enumerate(train_loader):
    optimizer.zero_grad()
    outputs = log_regr(images.view(-1,28*28))
    loss = criterion(outputs,labels)
    #Loss.append(loss.item())
    loss.backward()
    optimizer.step()
  Loss.append(loss.item())
  correct = 0
  for images,labels in test_loader:
    outputs = log_regr(images.view(-1,28*28))
    _,predicted = torch.max(outputs.data,1)
    correct+=(predicted == labels).sum()
  accuracy = 100*(correct.item())/len(test_dataset)
  acc.append(accuracy)
  print('Epoch: {}.Loss: {}.Accuracy:{}'.format(epoch,loss.item(),accuracy))

plt.plot(Loss)
plt.xlabel("no of epochs")
plt.ylabel("total loss")
plt.title("Loss")
plt.show()

plt.plot(acc)
plt.xlabel("no of epochs")
plt.ylabel("total accuracy")
plt.title("Accuracy")
plt.show()