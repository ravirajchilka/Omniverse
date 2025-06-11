from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.Open(r"D:\DOCUMENTS\isaac-sim_PARTS\my_pendulum.usdc")
prim_path = "/World/PAss/PAss"  # changed from "/World/PAss"
prim = stage.GetPrimAtPath(prim_path)

if not prim:
    print(f"Prim {prim_path} not found.")
else:
    xform = UsdGeom.Xformable(prim)
    
    ops = {op.GetOpName(): op for op in xform.GetOrderedXformOps()}

    # Translate 5 units up along Z
    if "xformOp:translate" in ops:
        ops["xformOp:translate"].Set(Gf.Vec3d(0.0, 0.0, 5.0))
    else:
        xform.AddTranslateOp().Set(Gf.Vec3d(0.0, 0.0, 5.0))

    # Rotate 90 degrees around Z axis
    if "xformOp:rotateXYZ" in ops:
        ops["xformOp:rotateXYZ"].Set(Gf.Vec3f(90.0, 0.0, 90.0))
    else:
        xform.AddRotateXYZOp().Set(Gf.Vec3f(0.0, 0.0, 90.0))

    stage.GetRootLayer().Save()

    print(f"Applied translation and rotation to {prim_path}")


