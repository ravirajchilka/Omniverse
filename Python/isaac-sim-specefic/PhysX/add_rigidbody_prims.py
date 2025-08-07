import omni.usd
from pxr import UsdPhysics, Sdf


stage = omni.usd.get_context().get_stage()

prim_paths_ar = ["/World/asm/disk","/World/asm/mount"]

for path in prim_paths_ar:
    prim = stage.GetPrimAtPath(path)

    if not prim.IsValid():
        print(f"prim is not valid")
        continue

    UsdPhysics.RigidBodyAPI.Apply(prim)
    rigid_body_api = UsdPhysics.RigidBodyAPI.Get(stage,path)
    prim.CreateAttribute("physics:rigidBodyEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    print(f"added rigid body to given prims")
    if path == "/World/asm/mount":
        rigid_body_api.CreateKinematicEnabledAttr().Set(True)