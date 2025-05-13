from pxr import Usd, UsdGeom
import os

usda_path = "E:/Software_Projects/openUSD_Isaac_sim_files/sphere2.usda"

stage = Usd.Stage.CreateNew(usda_path)

world_prim = UsdGeom.Xform.Define(stage, '/World')
xform_prim = UsdGeom.Xform.Define(stage, '/World/Xform')
sphere_prim = UsdGeom.Sphere.Define(stage, '/World/Sphere')

stage.GetRootLayer().Save()

# iterate over stage
for prim in stage.Traverse():
    print("path values ", prim.GetPath().pathString)


# remove prim
succesful = stage.RemovePrim('/World/Xform')

if succesful:
    print("after sucess \n")
    for prim in stage.Traverse():
        print("path values ", prim.GetPath().pathString)
    
