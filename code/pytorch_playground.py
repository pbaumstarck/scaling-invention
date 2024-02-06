import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
import pylab
import torch
import torch.nn as nn

n = 50
x = np.random.randn(n)
# x = 3 * np.random.random(n) - 1
y = x * x + 2 * x + 1

x_train = np.array(x, dtype=np.float32).reshape(-1, 1)
x_train.reshape
y_train = np.array(y, dtype=np.float32).reshape(-1, 1)
y_train.reshape

# plt.scatter(x, y, c=np.random.rand(n))
# plt.show()


class LinearRegressionModel(nn.Module):
  def __init__(self, input_dim, output_dim):
    super(LinearRegressionModel, self).__init__()
    self.linear = nn.Linear(input_dim, output_dim)  

  def forward(self, x):
    return self.linear(x)


class HiddenLayerModel(nn.Module):
  def __init__(self, input_dim, output_dim):
    super().__init__()
    # self.flatten = nn.Flatten()
    middle_layer = 10
    self.linear_relu_stack = nn.Sequential(
      # nn.Linear(28*28, 512),
      nn.Linear(input_dim, middle_layer),
      nn.ReLU(),
      nn.Linear(middle_layer, output_dim),
      # nn.ReLU(),
      # nn.Linear(512, 10),
    )

  def forward(self, x):
    # x = self.flatten(x)
    return self.linear_relu_stack(x)


input_dim = 1
output_dim = 1

model = LinearRegressionModel(input_dim, output_dim)
# model = LinearRegressionModel(input_dim, output_dim)
# model = HiddenLayerModel(input_dim, output_dim)
criterion = nn.MSELoss()
learning_rate = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

epochs = 100

ys = []  # y[:]]
for epoch in range(epochs):
    epoch += 1
    # Convert numpy array to torch Variable
    inputs = torch.from_numpy(x_train).requires_grad_()
    labels = torch.from_numpy(y_train)

    # Clear gradients w.r.t. parameters
    optimizer.zero_grad()

    # Forward to get output
    outputs = model(inputs)
    # print(inputs, outputs)

    # import pdb; pdb.set_trace()
    ys.append([_.item() for _ in outputs])

    # Calculate Loss
    loss = criterion(outputs, labels)

    # Getting gradients w.r.t. parameters
    loss.backward()

    # Updating parameters
    optimizer.step()

    print('epoch {}, loss {}'.format(epoch, loss.item()))

cm = pylab.get_cmap('RdYlGn')
for i, yy in enumerate(ys):
  plt.scatter(x, yy, c=cm((i + 1.0) / len(ys)))

plt.scatter(x, y, c='k')
plt.show()

# print('model.linear.weight,bias:', model.linear.weight.item(), model.linear.bias.item())
breakpoint()



# Autograd example
if False:
  device = torch.device('cpu')

  x = torch.randn(2, 3, requires_grad=True)
  y = torch.rand(2, 3, requires_grad=True)
  z = torch.ones(2, 3, requires_grad=True)

  with torch.autograd.profiler.profile(use_cuda=False) as prf:
      for _ in range(1000):
          z = (z / x) * y

  print(prf.key_averages().table(sort_by='self_cpu_time_total'))


