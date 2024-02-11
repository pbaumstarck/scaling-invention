
import pylab
import torch

import numpy as np
import matplotlib.pyplot as plt

# Create a loss function

# Create some data
# x = torch.randn(100, 1)
# y = torch.randn(100, 1)


n = 50
x = np.array(np.random.randn(n), dtype=np.float32)
# x = 3 * np.random.random(n) - 1
# y = x * x + 2 * x + 1 + 0.1
y = x * x + 1.0 * x + 2.0 # + 0.1 * np.random.random(n, dtype=np.float32)
# y = -4.0 * x + 7.0 # + 0.1 * np.random.random(n, dtype=np.float32)
y += 0.3 * np.random.randn(n)

if False:
  plt.scatter(x, y, facecolors='none', edgecolors='b')
  plt.scatter(x, y, c='r')
  plt.show()


# # Calculate the loss
# loss = loss_fn(x, y)

# # Plot the loss
# plt.plot(x, loss)
# plt.show()

# board_array = np.array(board, dtype=np.float32)
# fig, ax = plt.subplots()
# i = ax.imshow(board_array, cmap=cm.jet, interpolation='nearest')
# fig.colorbar(i)
# plt.show()

# Calculate the loss in parameter space ...


loss_fn = torch.nn.MSELoss()
loss_fn = torch.nn.L1Loss()
loss_fn = torch.nn.HuberLoss()
loss_fn = torch.nn.SmoothL1Loss()

# LOSS_MAP_ORIGIN = -5
# LASS_MAP_SCALE = 18

# weight and bias
def get_loss_map(loss_fn, x, y):
  losses = [[0.0] * 100 for _ in range(100)]
  x = torch.from_numpy(x)
  y = torch.from_numpy(y)
  for wi in range(100):
    for wb in range(100):
      w = -5.0 + 13.0 * wi / 100.0
      b = -5.0 + 13.0 * wb / 100.0
      ywb = x * w + b

      # breakpoint()
      # x = bias, y = weight
      # breakpoint()
      losses[wi][wb] = loss_fn(ywb, y).item()

  # import pylab
  # cm = pylab.get_cmap('RdYlGn')
  # fig, ax = plt.subplots()
  # i = ax.imshow(losses, cmap=cm, interpolation='nearest')
  # fig.colorbar(i)
  # plt.show()
  # breakpoint()
  return losses
  # return list(reversed(losses))
  # breakpoint()


# class linearRegression(torch.nn.Module):
#   def __init__(self, inputSize, outputSize):
#     super(linearRegression, self).__init__()
#     self.linear = torch.nn.Linear(inputSize, outputSize)

#   def forward(self, x):
#     return self.linear(x)

# LEARN!
def learn(criterion, x, y, lr=0.1, epochs=100):
  model = torch.nn.Linear(1, 1)
  # model.weight.data.fill_(-1.0)
  # model.bias.data.fill_(-1.0)
  # Y axis of image = WEIGHT
  model.weight.data.fill_(6.0)
  # X axis of image = BIAS
  model.bias.data.fill_(7.0)
  models = [[model.weight.item(), model.bias.item()]]

  optimizer = torch.optim.SGD(model.parameters(), lr=lr)
  for epoch in range(epochs):
    inputs = torch.from_numpy(x).requires_grad_().reshape(-1, 1)
    labels = torch.from_numpy(y).reshape(-1, 1)

    # Clear gradients w.r.t. parameters
    optimizer.zero_grad()
    # outputs = model[0] + model[1] * inputs
    outputs = model(inputs)

    # print(inputs, outputs)
    # import pdb; pdb.set_trace()
    # models.append([_.item() for _ in outputs])

    # Calculate Loss
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    # breakpoint()

    print('epoch {}, loss {}'.format(epoch, loss.item()))
    models.append([model.weight.item(), model.bias.item()])

  return models


epochs = 100
learning_rate = 0.1
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
for loss_fn, ax in [
  (torch.nn.MSELoss(), ax1),
  (torch.nn.L1Loss(), ax2),
  (torch.nn.HuberLoss(), ax3),
  (torch.nn.SmoothL1Loss(), ax4),
]:
  # loss_fn = loss_fns[0]
  losses_mse = get_loss_map(loss_fn, x, y)
  models_mse = learn(loss_fn, x, y, lr=learning_rate, epochs=epochs)
  # breakpoint()

  cm = pylab.get_cmap('RdYlGn')
  cm = pylab.get_cmap('terrain')
  # fig, ax = plt.subplots()
  i = ax.imshow(losses_mse, cmap=cm, interpolation='nearest')

  # breakpoint()
  loss_correction_fnx = lambda x: (x + 5.0) * 100.0 / 13.0
  loss_correction_fny = lambda y: (y + 5.0) * 100.0 / 13.0
  loss_x = [loss_correction_fnx(_[1]) for _ in models_mse]
  loss_y = [loss_correction_fny(_[0]) for _ in models_mse]

  ax.scatter(loss_x, loss_y, c='r')
  ax.plot(loss_x, loss_y, c='r')

  # test_x = [-4.0, -4.0, 7.0]
  # test_y = [-4.0, 1.5, 7.0]
  # ax.scatter(list(map(loss_correction_fnx, test_x)), list(map(loss_correction_fny, test_y)))
  # ax.plot(test_y, test_x)

  print(loss_fn)
  print(models_mse[0])
  print(models_mse[-1])
  # fig.colorbar(i)

plt.show()

