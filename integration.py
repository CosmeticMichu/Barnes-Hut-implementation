import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import quadtree as qt
import timeit
import imageio

#--------------------------------define entities (particles)--------------------------------
class Particle:
    def __init__(self, mass, x, y, vx, vy, ax, ay):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.s = 0 #s parameter in MAC = s/d

    # def draw_particle(self, ax, c = 'k', s = 4):
    #     ax.scatter(self.x, self.y, c = c, s = s)

    def show_particle_properties(self):
        print('Particle properties (mass, x_pos, y_pos, vx, vy): ')
        print('\t', Particle.mass, Particle.x, Particle.y, Particle.vx, Particle.vy)

#------------------------------generate particles-------------------------------
def create_particles(num_particles, xsize, ysize, seed) :
    particles = []
    ii = 0

    np.random.seed(seed)

    while ii < num_particles:
        mass = np.random.uniform(5E+4, 1E+5)
        x = np.random.uniform(0, xsize)
        y = np.random.uniform(0, ysize)
        vx, vy = np.random.uniform(-10.0, 10.0, size = 2)
        #vx, vy = 0, 0
        particles.append(Particle(mass, x, y, vx, vy, 0, 0))

        ii += 1
    return particles

#------------------------------create the tree-----------------------------

def build_quadtree(particles, x_size, y_size):
    root = qt.Rectangle(qt.Point(0,0), xsize, ysize)
    
    QuadTree = qt.TreeNode(root)
    for particle in particles:
        QuadTree.insert(particle)

    #print(f'{len(QuadTree)}/{len(particles)} particles were inserted!')
    return QuadTree

#---------------------------------main method----------------------------------

# if __name__ == '__main__':
#     xsize, ysize = 800, 800
#     NumOfParticles = 4
#     tmax = 60
#     Deltat = 0.1

#     t0 = timeit.default_timer()#timeit
#     #seed = int(1000*np.random.uniform())
#     seed = 424#note that with this seed definition we are able to expand or reduce the number of particles holding some positions 
#     particles = create_particles(NumOfParticles, xsize, ysize, seed)
#     elapsed_particles = timeit.default_timer() - t0#timeit

#     print(f'Particles were created! ({elapsed_particles:.4f}s)')
#     print(f'This sample was generated with seed = {seed}')

#     #Simulation starts
#     print(f'Simulation is running for {NumOfParticles} particles with Delta t = {Deltat} and t_max = {tmax}')
#     DPI = 141
#     fig = plt.figure(figsize=(800/DPI,800/DPI), dpi = DPI)
    
#     ax = plt.subplot()
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.set_facecolor('#030821')
#     ax.set_xticks([])
#     ax.set_yticks([])

#     t = 0
#     count = 1
#     filenames = []
#     while t <= tmax:
#         ax.clear()
#         ax.set_xlim(xsize)
#         ax.set_ylim(ysize)
#         ax.set_title(f't = {t:.2f}')
#         #print(f'iteration: {count}', flush = True)
#         filename = 'figures/gif_data/' + str(t) + '.png'
#         filenames.append(filename)
#         tree = build_quadtree(particles, xsize, ysize)
#         ax.scatter([particle.x for particle in particles],[particle.y for particle in particles], s=6, c = 'w')
#         ax.invert_yaxis()
#         ax.invert_xaxis()

#         #updates positions
#         for particle in particles:
#             particle.ax, particle.ay = tree.ParticleInteraction(particle)
#             #print(particle.ax)
#             particle.vx += particle.ax*Deltat
#             particle.vy += particle.ay*Deltat
#             particle.x += particle.vx*Deltat #+ 0.5*particle.ax*Deltat**2
#             particle.y += particle.vy*Deltat #+ 0.5*particle.ay*Deltat**2

#         plt.tight_layout()
#         plt.savefig(filename, dpi=DPI)

#         del tree#memory clear
#         t += Deltat
#         count += 1

#     elapsed_sim = timeit.default_timer() - t0#timeit
#     print(f'Simulation ended ({elapsed_sim}s) and aux figures were created. Creating .gif')

#     images = []
#     for filename in filenames:
#         images.append(imageio.imread(filename))
#     imageio.mimsave('figures/animation.gif', images, duration = 20)
#     elapsed = timeit.default_timer() - t0#timeit
#     print(f'.gif created. Work donde! ({elapsed}s)')

if __name__ == '__main__':
    xsize, ysize = 800, 800
    NumOfParticles = 10

    t0_particle = timeit.default_timer()#timeit
    seed = int(1000*np.random.uniform())
    #seed = 820
    #note that with this seed definition we are able to expand or reduce the number of particles holding some positions 
    particles = create_particles(NumOfParticles, xsize, ysize, seed)
    elapsed_particles = timeit.default_timer() - t0_particle#timeit

    t0_tree_build = timeit.default_timer()#timeit
    tree = build_quadtree(particles, xsize, ysize)
    elapsed_build_tree = timeit.default_timer() - t0_tree_build#timeit

    print(f'This sample was generated with seed = {seed}')

    #PLOT

    t0_plotting = timeit.default_timer()#timeit
    DPI = 72
    fig = plt.figure(figsize = (700/DPI, 500/DPI), dpi = DPI)
    
    ax = plt.subplot()
    ax.set_title(f'QuadTree visualization for {NumOfParticles} particles with seed = {seed}', fontsize = 18, fontweight = 'bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(xsize)
    ax.set_ylim(ysize)
    ax.set_facecolor('#030821')

    #draw QuadTree
    tree.draw(ax, c = 'w')

    #draw particles
    ax.scatter([particle.x for particle in particles],[particle.y for particle in particles], s=50, c = 'w')
    ax.invert_yaxis()
    ax.invert_xaxis()

    plt.tight_layout()
    plt.savefig('figures/QuadTree_visualization.png', dpi = DPI)

    elapsed_plotting = timeit.default_timer() - t0_plotting#timeit

    total_elapsed = timeit.default_timer() - t0_particle#timeit

    print(f'\nReport:\n\ttime elapsed generating particles: {elapsed_particles:.4f}s ({100*elapsed_particles/total_elapsed:.3f}% of the total)')
    print(f'\ttime elapsed building the tree: {elapsed_build_tree:.4f}s ({100*elapsed_build_tree/total_elapsed:.3f}% of the total)')
    print(f'\ttime elapsed plotting: {elapsed_plotting:.4f}s ({100*elapsed_plotting/total_elapsed:.3f}% of the total)')
    print(f'\ttotal elapsed time: {total_elapsed:.4f}s')

    plt.show()