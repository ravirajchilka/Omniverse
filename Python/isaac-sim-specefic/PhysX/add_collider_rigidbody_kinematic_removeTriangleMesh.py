import omni.usd
from pxr import Sdf, UsdPhysics, PhysxSchema

stage = omni.usd.get_context().get_stage()

prim_paths = ["/World/asm/mount", "/World/asm/disk"]

for path in prim_paths:
    prim = stage.GetPrimAtPath(path)

    if not prim.IsValid():
        print(f"not found a prim")
        continue

    # add colliders
    UsdPhysics.CollisionAPI.Apply(prim)
    UsdPhysics.MeshCollisionAPI.Apply(prim).CreateApproximationAttr().Set("convexHull")
    print(f"applied convex hull prim")

    # add rigid body
    UsdPhysics.RigidBodyAPI.Apply(prim)
    prim.CreateAttribute("physics:rigidBodyEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    print(f"added rigid body")

    # add kinematic rigid body to mount
    if path == "/World/asm/mount":
        UsdPhysics.RigidBodyAPI.Get(stage, "/World/asm/mount").CreateKinematicEnabledAttr().Set(True)
        print(f"set rigid body to kinematic")

    # remove any existign triangle mesh
    if prim.HasAPI(PhysxSchema.PhysxTriangleMeshCollisionAPI):
        prim.RemoveAPI(PhysxSchema.PhysxTriangleMeshCollisionAPI)
        print(f"removed triangle mesh")

