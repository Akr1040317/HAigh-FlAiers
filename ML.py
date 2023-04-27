import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GAE
from torch_geometric.data import Data

# define the model
class GAE(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, embedding_dim):
        super(GAE, self).__init__()
        self.encoder_l1 = GCNConv(input_dim, hidden_dim)
        self.encoder_l2 = GCNConv(hidden_dim, hidden_dim)
        self.encoder_l3 = GCNConv(hidden_dim, embedding_dim)
        self.decoder_l1 = GCNConv(embedding_dim, hidden_dim)
        self.decoder_l2 = GCNConv(hidden_dim, hidden_dim)
        self.decoder_l3 = GCNConv(hidden_dim, input_dim)
    # encodes the input graph into a smaller dimension
    def encode(self, x, edge_index):
        x = F.relu(self.encoder_l1(x, edge_index))
        x = F.relu(self.encoder_l2(x, edge_index))
        x = self.encoder_l3(x, edge_index)

        return x
    #decode from the smaller dimension back to the original dimension
    def decode(self, x, edge_index):
        x = F.relu(self.decoder_l1(x, edge_index))
        x = F.relu(self.decoder_l2(x, edge_index))
        x = self.decoder_l3(x, edge_index)

        return x
    # forward pass (encode then decode)
    def forward(self, x, edge_index):
        x = self.encode(x, edge_index)
        x = self.decode(x, edge_index)

        return x

# load the data
edge_list = []
with open("routes.txt", 'r') as file:
    for line in file:
        node1, node2, weight = line.strip().split(',')
        edge = (node1, node2, int(weight))
        edge_list.append(edge)
nodes = sorted(list(set([edge[0] for edge in edge_list] + [edge[1] for edge in edge_list])))
node_indices = {node: i for i, node in enumerate(nodes)}
edges = [(node_indices[edge[0]], node_indices[edge[1]]) for edge in edge_list]
weights = [edge[2] for edge in edge_list]
edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
edge_attr = torch.tensor(weights, dtype=torch.float)
x = torch.ones(len(nodes), 1) # set initial node features
data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
model = GAE(input_dim=1, hidden_dim=64, embedding_dim=16)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

#define loss function and train the model
loss_fn = nn.MSELoss()
model.train()
for epoch in range(100):
    optimizer.zero_grad()
    out = model(data.x, edge_index)
    print(out.shape)
    loss = loss_fn(out, data.x)
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch+1}, loss: {loss:.4g}')

# save the embeddings
embeddings = model.encode(data.x, edge_index)
torch.save(embeddings, 'embeddings.pt')