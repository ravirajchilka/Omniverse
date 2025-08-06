
import omni.usd
from pxr import UsdPhysics, PhysxSchema

# Get the USD context and stage
usd_context = omni.usd.get_context()
stage = usd_context.get_stage()

# Check if stage is valid
if not stage:
    print("Error: No valid USD stage found.")
else:
    # Specify the path for the physics scene prim
    physics_scene_path = "/physicsScene"  # Adjust if needed, e.g., "/World/PhysicsScene"

    try:
        # Check if the physics scene already exists; if not, define it
        physics_scene = UsdPhysics.Scene.Get(stage, physics_scene_path)
        if not physics_scene:
            physics_scene = UsdPhysics.Scene.Define(stage, physics_scene_path)
            print(f"Created physics scene at {physics_scene_path}")
        else:
            print(f"Physics scene already exists at {physics_scene_path}")

        # Set gravity direction (downward along Z-axis) and magnitude (9.81 m/s² for Earth gravity)
        physics_scene.CreateGravityDirectionAttr().Set((0, 0, -1))
        physics_scene.CreateGravityMagnitudeAttr().Set(9.81)
        print("Gravity set for physics scene")

        # Optional: Apply PhysxSceneAPI for Isaac Sim-specific settings
        physx_scene_api = PhysxSchema.PhysxSceneAPI.Apply(physics_scene)
        physx_scene_api.CreateSolverTypeAttr().Set("PGS")  # Position-based solver (or "TGS" for Temporal Gauss-Seidel)
        physx_scene_api.CreateNumSubstepsAttr().Set(4)  # Increase for stability
        print("Applied PhysxSceneAPI with solver settings")

        # Force stage update to refresh GUI
        usd_context.get_stage().GetRootLayer().Save()
        omni.usd.get_context().save_stage()
        print("Stage saved to refresh GUI")

    except Exception as e:
        print(f"Error setting up physics scene: {e}")