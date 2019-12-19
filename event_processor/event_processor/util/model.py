import torch.nn.functional as F
import torch.autograd as auto
import torch.nn as nn
import numpy as np

CATEGORIES = [
    'Arts and Culture',
    'Animals',
    'Advocacy and Human Rights',
    'Education and Literacy',
    'Women',
    'Homeless and Housing',
    'Health and Medicine',
    'Seniors',
    'Children and Youth',
    'Community'
]

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.w1 = nn.Linear(vocab_size, 1000)
        self.w2 = nn.Linear(vocab_size, 100)
        self.w3 = nn.Linear(100, 2)

    def forward(self, x):
        x = F.relu(self.w1(x))
        x = F.relu(self.w2(x))
        return F.log_softmax(self.w3(x))

to_torch = lambda x: auto.Variable(torch.from_numpy(x))

def predict_event_category(event_description, vectorizer, models):
    transformed = vectorizer.transform(event_description).todense()
    input_vec = to_torch(np.array(transformed)[0]).float()
    preds = [model(input_vec).data.numpy() for model in models]
    probs = []
    for i, pred in enumerate(preds[:-1]): # omits "Community"
        if pred[0] <= pred[1]:
            probs.append(pred[1])
        else:
            probs.append(0)
    return CATEGORIES[probs.index(probs.max())]