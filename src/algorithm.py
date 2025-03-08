import numpy as np


class Particle:
  def __init__(self, dim, bounds, reward_function):
    self.position = np.random.uniform(bounds[:, 0], bounds[:, 1], dim)
    self.velocity = np.random.uniform(-1, 1, dim)
    self.best_position = np.copy(self.position)
    self.reward_function = reward_function
    self.best_value = self.reward_function(self.position)

  def update_velocity(self, global_best, w, c1, c2):
    inertia = w * self.velocity
    cognitive = c1 * np.random.rand(len(self.position)) * (self.best_position - self.position)
    social = c2 * np.random.rand(len(self.position)) * (global_best - self.position)
    self.velocity = inertia + cognitive + social

  def move(self, bounds):
    self.position += self.velocity
    self.position = np.clip(self.position, bounds[:, 0], bounds[:, 1])
    value = self.reward_function(self.position)
    if value < self.best_value:
      self.best_value = value
      self.best_position = np.copy(self.position)


def particle_swarm_optimization(dim, bounds, reward_function, num_particles=30, max_iter=100, w=0.5, c1=1.5, c2=1.5):
  bounds = np.array(bounds)
  particles = [Particle(dim, bounds, reward_function) for _ in range(num_particles)]
  global_best_position = max(particles, key=lambda p: p.best_value).best_position

  for _ in range(max_iter):
    for particle in particles:
      particle.update_velocity(global_best_position, w, c1, c2)
      particle.move(bounds)
    global_best_position = max(particles, key=lambda p: p.best_value).best_position
  
  return global_best_position, reward_function(global_best_position)
