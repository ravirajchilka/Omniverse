import omni.usd
from pxr import Usd, UsdPhysics, UsdGeom, PhysxSchema, Sdf  # Add Sdf import here

# Get the USD context and stage
usd_context = omni.usd.get_context()
stage = usd_context.get_stage()

# Specify the prim paths for disk and mount
prim_paths = [
    "/World/asm/disk",
    "/World/asm/mount"
]

for prim_path in prim_paths:
    prim = stage.GetPrimAtPath(prim_path)
    
    if not prim.IsValid():
        print(f"Prim at {prim_path} does not exist.")
        continue
    
    # Print prim type and API status for debugging
    print(f"Checking prim {prim_path} (Type: {prim.GetTypeName()}, "
          f"Has CollisionAPI: {prim.HasAPI(UsdPhysics.CollisionAPI)}, "
          f"Has MeshCollisionAPI: {prim.HasAPI(UsdPhysics.MeshCollisionAPI)}, "
          f"Has RigidBodyAPI: {prim.HasAPI(UsdPhysics.RigidBodyAPI)})")
    
    # Ensure convex hull collider is correctly set
    if prim.HasAPI(UsdPhysics.CollisionAPI) and prim.HasAPI(UsdPhysics.MeshCollisionAPI):
        mesh_collision_api = UsdPhysics.MeshCollisionAPI.Get(stage, prim_path)
        mesh_collision_api.CreateApproximationAttr().Set("convexHull")
        prim.CreateAttribute("physics:collisionEnabled", Sdf.ValueTypeNames.Bool).Set(True)  # Use Sdf here
        print(f"Confirmed convex hull collider on {prim_path}")
    else:
        # Apply collider APIs if missing
        UsdPhysics.CollisionAPI.Apply(prim)
        mesh_collision_api = UsdPhysics.MeshCollisionAPI.Apply(prim)
        mesh_collision_api.CreateApproximationAttr().Set("convexHull")
        prim.CreateAttribute("physics:collisionEnabled", Sdf.ValueTypeNames.Bool).Set(True)  # Use Sdf here
        print(f"Applied convex hull collider to {prim_path}")
    
    # Remove redundant PhysxTriangleMeshCollisionAPI and PhysxSDFMeshCollisionAPI
    if prim.HasAPI(PhysxSchema.PhysxTriangleMeshCollisionAPI):
        prim.RemoveAPI(PhysxSchema.PhysxTriangleMeshCollisionAPI)
        print(f"Removed PhysxTriangleMeshCollisionAPI from {prim_path}")
    if prim.HasAPI(PhysxSchema.PhysxSDFMeshCollisionAPI):
        prim.RemoveAPI(PhysxSchema.PhysxSDFMeshCollisionAPI)
        print(f"Removed PhysxSDFMeshCollisionAPI from {prim_path}")
    
    # Apply and enable RigidBodyAPI
    if not prim.HasAPI(UsdPhysics.RigidBodyAPI):
        UsdPhysics.RigidBodyAPI.Apply(prim)
        print(f"RigidBodyAPI applied to {prim_path}")
    rigid_body_api = UsdPhysics.RigidBodyAPI.Get(stage, prim_path)
    prim.CreateAttribute("physics:rigidBodyEnabled", Sdf.ValueTypeNames.Bool).Set(True)  # Use Sdf here
    print(f"Enabled rigid body on {prim_path}")
    
    # Optional: Set mount as kinematic (static)
    if prim_path == "/World/asm/mount":
        rigid_body_api.CreateKinematicEnabledAttr().Set(True)
        print(f"Set {prim_path} as kinematic (static)")
    else:
        rigid_body_api.CreateKinematicEnabledAttr().Set(False)  # Ensure disk is dynamic
    
    # Optional: Set mass properties (uncomment to use)
    # rigid_body_api.CreateMassAttr().Set(1.0)  # Set mass in kg (e.g., 1 kg)
    # OR
    # mass_api = UsdPhysics.MassAPI.Apply(prim)
    # mass_api.CreateDensityAttr().Set(1000.0)  # Density in kg/m^3

# Ensure physics scene exists and gravity is enabled
physics_scene_path = "/physicsScene"  # Adjust if your scene has a different path
physics_scene = UsdPhysics.Scene.Get(stage, physics_scene_path)
if not physics_scene:
    physics_scene = UsdPhysics.Scene.Define(stage, physics_scene_path)
    print(f"Created physics scene at {physics_scene_path}")
physics_scene.CreateGravityDirectionAttr().Set((0, 0, -1))
physics_scene.CreateGravityMagnitudeAttr().Set(9.81)
print("Gravity enabled for physics scene")

# Force stage update to refresh GUI
usd_context.get_stage().GetRootLayer().Save()
omni.usd.get_context().save_stage()
print("Stage saved to refresh GUI")

print("Finished applying rigid body properties to disk and stand.")