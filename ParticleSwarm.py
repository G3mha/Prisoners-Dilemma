import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Non-convex function with many local maxima often used as a performance test for optimization problems
def rastrigin(x):
    A = 10
    return A * len(x) + sum([(xi ** 2 - A * np.cos(2 * np.pi * xi)) for xi in x])

class Particle:
    def __init__(self, dim, bounds):
        self.position = np.random.uniform(bounds[:, 0], bounds[:, 1], dim)
        self.velocity = np.random.uniform(-1, 1, dim)
        self.best_position = np.copy(self.position)
        self.best_value = rastrigin(self.position)

    def update_velocity(self, global_best, w, c1, c2):
        inertia = w * self.velocity
        cognitive = c1 * np.random.rand(len(self.position)) * (self.best_position - self.position)
        social = c2 * np.random.rand(len(self.position)) * (global_best - self.position)
        self.velocity = inertia + cognitive + social

    def move(self, bounds):
        self.position += self.velocity
        self.position = np.clip(self.position, bounds[:, 0], bounds[:, 1])
        value = rastrigin(self.position)
        if value < self.best_value:
            self.best_value = value
            self.best_position = np.copy(self.position)

def particle_swarm_optimization(dim, bounds, num_particles=30, max_iter=100, w=0.5, c1=1.5, c2=1.5):
    bounds = np.array(bounds)
    particles = [Particle(dim, bounds) for _ in range(num_particles)]
    global_best_position = max(particles, key=lambda p: p.best_value).best_position
    
    fig, ax = plt.subplots()
    X, Y = np.meshgrid(np.linspace(bounds[0, 0], bounds[0, 1], 100), np.linspace(bounds[1, 0], bounds[1, 1], 100))
    Z = np.array([[rastrigin([x, y]) for x in X[0]] for y in Y[:, 0]])
    ax.contourf(X, Y, Z, levels=50, cmap='viridis')
    particles_scatter = ax.scatter([], [], color='red', marker='o')
    
    def update(frame):
        nonlocal global_best_position
        for particle in particles:
            particle.update_velocity(global_best_position, w, c1, c2)
            particle.move(bounds)
        global_best_position = max(particles, key=lambda p: p.best_value).best_position
        positions = np.array([p.position for p in particles])
        particles_scatter.set_offsets(positions)
        ax.set_title(f'Iteration {frame}')
        return particles_scatter,
    
    anim = animation.FuncAnimation(fig, update, frames=max_iter, interval=100, blit=False)
    anim.save("pso_animation.mp4", writer="ffmpeg", fps=10)

    plt.show()
    return global_best_position, rastrigin(global_best_position)

dim = 2
bounds = np.array([(-5.12, 5.12), (-5.12, 5.12)])  # Rastrigin function domain
best_pos, best_val = particle_swarm_optimization(dim, bounds)
print("Best Position:", best_pos)
print("Best Value:", best_val)

