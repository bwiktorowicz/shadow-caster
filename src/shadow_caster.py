import sys
import time as timer
import math
import numpy as np
from numpy import linalg as lg
from stl import mesh
from shapely.geometry import Polygon, MultiPoint
from shapely.ops import cascaded_union
from mpl_toolkits import mplot3d
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon as poly
from matplotlib.collections import PatchCollection


'''
Tool that returns projected shadow polygon of arbitrary plane or 3D objected on arbitrary plane along
arbitrary solar vector

Required packages: numpy-stl, shapely

Usage:

shadow_instance = Shadow_Caster(file_name=<None|Name of 3D file>, multi_body=<True|False>, debug=<True|False>)
execute cast : Shadow_Caster.shade(<shading_plane>, <shaded_plane>, <solar_vector>)

Where:
        file_name:	name of binary STL file containing mesh for solid(s)
        shd_pln		= list([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3]])
        shding_pln	= list([[x4, y4, z4], [x5, y5, z5], [x6, y6, z6]])
        multi_body:	define as True if 3D file consists of multiple objects; defaults to True
        debug:		plots the 3D image and cast shadow
'''


class Shadow_Caster(object):

    def __init__(self, **kwargs):
        self.file_name = kwargs.pop('file_name', None)
        multi_body = np.array(kwargs.pop('multi_body', False))
        self.debug = kwargs.pop('debug', False)

        if(multi_body and self.file_name is not None):
            self.read_geometry_file()
            sec_time = timer.time()
            print('Processing Geometries...')
            sys.stdout.flush()
            self.isol_geom()
            print('Done ', timer.time() - sec_time, 'sec')
            print(np.size(self.objects, 0), 'solids identified')

            if(self.debug):
                # debugging plot
                figure = plt.figure()
                axes = mplot3d.Axes3D(figure)

                for object_mesh in self.objects:
                    axes.add_collection3d(
                        mplot3d.art3d.Poly3DCollection(object_mesh))

                scale = self.object_mesh.points.flatten(-1)
                axes.set_aspect('equal')
                axes.set_xlabel('x')
                axes.set_ylabel('y')
                axes.set_zlabel('z')
                axes.auto_scale_xyz(scale, scale, scale)
                plt.show()

    # execute shodow casting and return shadow
    def shade(self, shading_plane, shaded_plane, solar_vector):

        dbg_obj = []
        dbg_obj.append(shading_plane)
        dbg_obj.append(shaded_plane)

        self.shaded_plane = np.matrix(shaded_plane)
        self.shading_plane = np.matrix(shading_plane)
        self.solar_vector = np.array(solar_vector)

        shadow_obj = []
        shadow_dislv = []

        if(self.debug and self.file_name is None):
            # debuging plot
            figure = plt.figure()
            axes = mplot3d.Axes3D(figure)

            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(dbg_obj))

            axes.set_aspect('equal')
            axes.set_xlabel('x')
            axes.set_ylabel('y')
            axes.set_zlabel('z')
            plt.show()

        if(self.file_name is not None):
            for obj_mesh in self.objects:
                shadow_obj.append(list(map(self.ray_cast, obj_mesh)))
            for shd in shadow_obj:
                if(shd is not None):
                    shadow_dislv.append(cascaded_union(shd))
        else:
            shade_obj = self.ray_cast(shading_plane)
            if(shade_obj is not None):
                shadow_dislv.append(shade_obj)
#            shadow_dislv.append(self.ray_cast(shading_plane))

        if self.debug:
            # debugging plot
            patches = []
            figure = plt.figure()
            axes = figure.add_subplot(111)

            for shd in shadow_dislv:
                x, y = shd.exterior.xy
                x_pt = np.array(x)
                y_pt = np.array(y)
                xy = np.transpose(np.matrix(np.vstack((x_pt, y_pt))))

                patches.append(poly(xy, True))

            p = []

            p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
            axes.add_collection(p)

            axes.set_aspect('equal')
            axes.set_xlabel('x')
            axes.set_ylabel('y')
            axes.autoscale(enable=True, axis='both', tight=None)
            plt.show()

        return(shadow_dislv)

    # function projecting ray along solar vector from shading points of
    # plane/element onto shaded plane
    def ray_cast(self, shading_pln):

        #if(not is_coplanar(np.array(list(shdw.exterior.coords)), shaded_pln)):
        #                   shd_area=0
        self.shd_pts = []

        nrm = np.cross(self.shaded_plane[1][:] - self.shaded_plane[0][:],
                       self.shaded_plane[2][:] - self.shaded_plane[0][:])

        for pt in shading_pln:
            den = np.dot(nrm, self.solar_vector)
            if den == 0:
                print('The provided shaded plane and solar vector do not intersect')
                return(0)
            else:
                param = lg.norm(np.dot(nrm, np.transpose(self.shaded_plane[0][:] - np.array(pt)))) / den

            if(self.solar_vector[0] > 0):
                param*=-1
            self.shd_pts.append(self.solar_vector * param + pt)

        shd_poly = Polygon(MultiPoint(self.shd_pts).convex_hull)

        if(not self.is_coplanar(np.matrix(self.shd_pts), self.shaded_plane)):
            return(None)
        else:
            return(shd_poly)

    # read in mesh from STL file
    def read_geometry_file(self):

        self.object_mesh = mesh.Mesh.from_file(self.file_name)

    # isolate multiple geometries into indipendent objects
    def isol_geom(self):

        self.objects = []
        scene_geom_ini = []

        # combine vectors into individual mesh elements
        for i, vect in enumerate(self.object_mesh.v0):
            scene_geom_ini.append(
                list([list(vect), list(self.object_mesh.v1[i]), list(self.object_mesh.v2[i])]))
            scene_geom = list(scene_geom_ini)

        object_size = 0
        mesh_size = np.size(scene_geom, 0)
        last_object = False

        # isolate geometries by finding continuous element mesh
        while(not last_object):

            isol_geom = False
            self.found_elem = []

            self.found_elem_mat = np.matrix(scene_geom[0])

            self.found_elem.append(scene_geom[0])

            scene_geom[0] = []
            scene_geom.remove([])

            rem_size_scene = np.size(scene_geom, 0)

            while(not isol_geom):

                if(rem_size_scene > 1):

                    found_tmp = list(map(self.find_touch_elem, scene_geom))

                    found_tmp = [iter_elem for iter_elem in found_tmp if iter_elem]

                    if(not any(found_tmp)):
                        isol_geom = True

                elif(rem_size_scene == 1):
                    found_tmp = []
                    found_tmp.append(scene_geom[0])

                self.found_elem = self.found_elem + found_tmp

                for elem in found_tmp:
                    self.found_elem_mat = np.concatenate((self.found_elem_mat, elem), axis=0)

                scene_geom = [elem_rem for elem_rem in scene_geom if elem_rem not in self.found_elem]

                rem_size_scene = np.size(scene_geom, 0)

                if(rem_size_scene == 0):
                    isol_geom = True

            self.objects.append(self.found_elem)

            scene_geom = [elem_rem for elem_rem in scene_geom_ini if elem_rem not in self.found_elem]

            object_size += np.size(self.found_elem, 0)

            if(object_size == mesh_size):
                last_object = True

    # return elements if two test elements are touching, otherwise return None
    def find_touch_elem(self, scene_geom_elem):

        scene_elem = np.matrix(scene_geom_elem)

        res = np.around(self.found_elem_mat * np.transpose(scene_elem) -
                        np.transpose(np.matrix(lg.norm(self.found_elem_mat, axis=1)**2)), decimals=1)

        if not res.all():
            return(scene_geom_elem)
        else:
            return(None)

    def is_coplanar(self, shadow_pln, shaded_pln):

        shadow_pln = np.array(shadow_pln)
        shaded_pln = np.array(shaded_pln)

        eps = 0.0000000001

        def is_coliniear(vec1, vec2):

            if(np.linalg.norm(np.cross(vec1, vec2)) > eps):
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
            if(math.fabs(np.dot(shdw_vec, shaded_nrm)) > eps):
                return(False)

        return(True)
