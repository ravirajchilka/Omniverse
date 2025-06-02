from pxr import Usd, UsdGeom, Gf

usd_path = "D:\\DOCUMENTS\\BLENDER_parts\\sphereBA.usdc"
stage = Usd.Stage.Open(usd_path)

# Print all prims to check the correct path
for prim in stage.Traverse():
    print(prim.GetPath())


# Use the correct path as printed above, e.g., "/Root/Sphere"
xform_prim = stage.GetPrimAtPath("/root/Sphere")
if not xform_prim or not xform_prim.IsValid():
    print("Prim not found or invalid!")
    exit()

xformable = UsdGeom.Xformable(xform_prim)
if not xformable:
    print("Prim is not Xformable!")
    exit()

xformable.ClearXformOpOrder()

xformable.AddTranslateOp()
xformable.AddOrientOp()
xformable.AddScaleOp()

xform_ops = xformable.GetOrderedXformOps()
for op in xform_ops:
    print(op.GetOpName())

# Set the ops with correct types
xform_ops[0].Set(Gf.Vec3d(0, 0, 0)) # Translate
xform_ops[1].Set(Gf.Quatf(1, 0, 0, 0)) # Orient (quaternion)
xform_ops[2].Set(Gf.Vec3d(1, 1, 1)) # Scale

# Save changes if needed
stage.GetRootLayer().Save()
