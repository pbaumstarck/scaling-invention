#!/usr/bin/env python3

import jax
import jax.numpy as jnp

x = jnp.arange(10)
print(x)

long_vector = jnp.arange(int(1e7))

# %timeit
# jnp.dot(long_vector, long_vector).block_until_ready()


def identity(x):
  return x

def sum_of_squares(x):
  return jnp.sum(x ** 2)


sum_of_squares_dx = jax.grad(sum_of_squares)

x = jnp.asarray([1.0, 2.0, 3.0, 4.0])

print(sum_of_squares(x))

print(sum_of_squares_dx(x))


def sum_squared_error(x, y):
  return jnp.sum((x - y) ** 2)

sum_squared_error_dx = jax.grad(sum_squared_error)

y = jnp.asarray([1.1, 2.1, 3.1, 4.1])

print(sum_squared_error_dx(x, y))

print(jax.value_and_grad(sum_squared_error)(x, y))
# breakpoint()


import numpy as np
import matplotlib.pyplot as plt

xs = np.random.normal(size=(100,))
noise = np.random.normal(scale=0.1, size=(100,))
ys = xs * 3 - 1 + noise

# plt.scatter(xs, ys);
# plt.show()

def model(theta, x):
  """Computes wx + b on a batch of input x."""
  # w, b = theta
  # return w * x + b
  return theta[0] * x + theta[1]


def loss_fn(theta, x, y):
  # prediction = model(theta, x)
  # return jnp.mean((prediction - y) ** 2)
  return jnp.mean((model(theta, x) - y) ** 2)


def update(theta, x, y, lr=0.1):
  # return theta - lr * jax.grad(loss_fn)(theta, x, y)
  return theta - lr * jax.grad(loss_fn)(theta, x, y)


# breakpoint()
# theta = jax.random.random(2)  # jnp.array([-1., 1.])
theta = np.random.rand(2)

import pylab
cm = pylab.get_cmap('RdYlGn')
for i in range(100):
  plt.scatter(xs, model(theta, xs), c=cm(i / 10.0))
  theta = update(theta, xs, ys)

plt.plot(xs, model(theta, xs), c='k')  # cm(10.0))
plt.show()
w, b = theta
print(f"w: {w:<.2f}, b: {b:<.2f}")



def selu(x, alpha=1.67, lambda_=1.05):
  return lambda_ * jnp.where(x > 0, x, alpha * jnp.exp(x) - alpha)

x = jnp.arange(1000000)
selu(x)




breakpoint()



