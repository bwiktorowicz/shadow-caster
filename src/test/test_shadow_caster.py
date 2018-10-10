import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from shadow_caster import Shadow_Caster
from shapely.geometry import Polygon


def is_coplanar(shadow_pln, shaded_pln):

    def is_coliniear(vec1, vec2):

        if(np.linalg.norm(np.cross(vec1, vec2)) > 0.000000001):
            return(False)
        else:
            return(True)

    shadow_pt_num, _ = shadow_pln.shape
    shaded_pt_num, _ = shaded_pln.shape

    shadow_vec = np.array([shadow_pln[0,:]-shadow_pln[i,:] for i in range(1, shadow_pt_num)])
    shaded_vec = np.array([shaded_pln[0,:]-shaded_pln[i,:] for i in range(1, shaded_pt_num)])

    shaded_vec1 = shaded_vec[0,:]

    i=1
    while(is_coliniear(shaded_vec1, shaded_vec[i,:])):
        i+=1

    shaded_vec2 = shaded_vec[i,:]

    shaded_nrm = np.cross(shaded_vec1, shaded_vec2)

    for shdw_vec in shadow_vec:
        if(math.fabs(np.dot(shdw_vec, shaded_nrm)) > 0.00000000001):
            return(False)

    return(True)


def plot_planes(shaded_pln, shading_pln, shadow_plane):

    shading_pln = np.array(shading_pln)
    shaded_pln = np.array(shaded_pln)
    geom = shadow_plane[0].exterior.coords
    shadow_pln = np.array(list(geom))

    trk_verts = [list(zip(shaded_pln[:,0], shaded_pln[:,1], shaded_pln[:,2]))]
    veg_verts = [list(zip(shading_pln[:,0], shading_pln[:,1], shading_pln[:,2]))]
    shd_verts = [list(zip(shadow_pln[:,0], shadow_pln[:,1], shadow_pln[:,2]))]

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.add_collection3d(Poly3DCollection(trk_verts))
    ax.add_collection3d(Poly3DCollection(veg_verts, facecolor='g'))
    ax.add_collection3d(Poly3DCollection(shd_verts, facecolor='r'))
    plt.show()


def calc_area(shaded_pln, shadow_plane):

    shaded_obj = Polygon(shaded_pln).convex_hull
    shd_trk = shadow_plane[0].intersection(shaded_obj)
    print(shd_trk.area)

    #plot_planes(shaded_pln, shaded_pln, [shd_trk])


sol_vec = [0.85887074, 0.14255308, 0.49195494]

shading_pln = [[1.0046, -2.315, -1.73984504],
               [1.0046, -2.315, -1.43984504],
               [1.0046, -2.285, -1.43984504],
               [1.0046, -2.285, -1.73984504]]

shaded_pln = [[-0.9985, -2.40055, 1.72945273],
              [-0.9985, 2.40055, 1.72945273],
              [-1.0045, -2.39935, 1.73984504],
              [-1.0045, 2.39935, 1.73984504],
              [1.0045, -2.39935, -1.73984504],
              [1.0045, 2.39935, -1.73984504],
              [0.9985, -2.40055, -1.72945273],
              [0.9985, 2.40055, -1.72945273]]

shadow = Shadow_Caster()
shadow_plane = shadow.shade(shading_pln, shaded_pln, sol_vec)

if(len(shadow_plane) > 0):
    plot_planes(shaded_pln, shading_pln, shadow_plane)
    calc_area(shaded_pln, shadow_plane)
else:
    print('No shadow cast\n')

#shadow_pln = np.array(list(shadow_plane[0].exterior.coords))
#print(is_coplanar(shadow_pln, np.array(shaded_pln)))

sol_vec = [-0.89566576, 0.21339957, 0.3901839]

shading_pln = [[-1.0046, -2.315, -1.73984504],
               [-1.0046, -2.315, -1.43984504],
               [-1.0046, -2.285, -1.43984504],
               [-1.0046, -2.285, -1.73984504]]

shaded_pln = [[-1.0045, -2.39935, -1.73984504],
              [-1.0045, 2.39935, -1.73984504],
              [-0.9985, -2.40055, -1.72945273],
              [-0.9985, 2.40055, -1.72945273],
              [0.9985, -2.40055, 1.72945273],
              [0.9985, 2.40055, 1.72945273],
              [1.0045, -2.39935, 1.73984504],
              [1.0045, 2.39935, 1.73984504]]

shadow = Shadow_Caster()
shadow_plane = shadow.shade(shading_pln, shaded_pln, sol_vec)
shadow_pln = np.array(list(shadow_plane[0].exterior.coords))

if(len(shadow_pln) > 0):
    plot_planes(shaded_pln, shading_pln, shadow_plane)
    calc_area(shaded_pln, shadow_plane)
else:
    print('No shadow cast\n')

#shadow_pln = np.array(list(shadow_plane[0].exterior.coords))
#print(is_coplanar(shadow_pln, np.array(shaded_pln)))

sol_vec = [0.90352608, 0.41689683, 0.09918492]

shading_pln = [[1.98116247, -2.315, -0.33387498],
               [1.98116247, -2.315, -0.36387498],
               [1.98116247, -2.285, -0.36387498],
               [1.98116247, -2.285, -0.33387498]]

shaded_pln = [[1.98106247, -2.39935, -0.33387498],
              [1.98106247, 2.39935, -0.33387498],
              [1.96922934, -2.40055, -0.3318807],
              [1.96922934, 2.40055, -0.3318807],
              [-1.96922934, -2.40055, 0.3318807],
              [-1.96922934, 2.40055, 0.3318807],
              [-1.98106247, -2.39935, 0.33387498],
              [-1.98106247, 2.39935, 0.33387498]]

shadow = Shadow_Caster()
shadow_plane = shadow.shade(shading_pln, shaded_pln, sol_vec)

if(len(shadow_plane) > 0):
    plot_planes(shaded_pln, shading_pln, shadow_plane)
    calc_area(shaded_pln, shadow_plane)
else:
    print('No shadow cast\n')

#shadow_pln = np.array(list(shadow_plane[0].exterior.coords))
#print(is_coplanar(shadow_pln, np.array(shaded_pln)))
