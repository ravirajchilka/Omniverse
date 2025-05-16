from pxr import Gf, Usd, UsdGeom, Sdf

stage = Usd.Stage.CreateNew("E:\Software_Projects\openUSD_Isaac_sim_files\Ch03/AddReference.usda")

default_prim: Usd.Prim = UsdGeom.Xform.Define(stage,Sdf.Path("/World")).GetPrim()

stage.SetDefaultPrim(default_prim)

object_prim = stage.DefinePrim("/World/object", "Xform")

object_prim.GetReferences().AddReference("./Assets/Cube.usda")

xform = UsdGeom.Xformable(object_prim)
xform.AddTranslateOp().Set(Gf.Vec3d(100,10,0))
xform.AddRotateXYZOp().Set(Gf.Vec3d(0,50,0))
xform.AddScaleOp().Set(Gf.Vec3d(1,1,1))

xform.AddRotateXYZOp(opSuffix="rotateMore").Set(Gf.Vec3d(20,20,3)) # add extra rotation to existing one

stage.Save()


