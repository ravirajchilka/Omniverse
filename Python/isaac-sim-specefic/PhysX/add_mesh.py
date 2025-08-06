import omni.usd
from pxr import UsdPhysics

# Get the current stage
stage = omni.usd.get_context().get_stage()

# Specify the path to your existing mesh cube prim
prim_path = "/World/asm/disk"  # Replace with your actual prim path if different
prim = stage.GetPrimAtPath(prim_path)

if not prim.IsValid():
    print(f"Prim at {prim_path} does not exist. Please create it first.")
else:
    # Apply the base Collision API if not already present
    UsdPhysics.CollisionAPI.Apply(prim)
    
    # Apply the Mesh Collision API and set approximation to convex hull
    mesh_collision_api = UsdPhysics.MeshCollisionAPI.Apply(prim)
    mesh_collision_api.CreateApproximationAttr().Set("convexHull")
    
    print(f"Convex hull collider assigned to prim at {prim_path}.")
    