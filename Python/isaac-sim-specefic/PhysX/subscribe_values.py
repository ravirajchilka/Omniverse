from pxr import Usd, UsdPhysics, Sdf
import omni.usd
import omni.physx as _physx
import omni.timeline
import math

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define joint path (adjust if needed)
joint_path = "/World/asm/joint"

# Create or get the revolute joint
joint = UsdPhysics.RevoluteJoint.Get(stage, joint_path)
if not joint:
    joint = UsdPhysics.RevoluteJoint.Define(stage, joint_path)
    joint.CreateBody0Rel().SetTargets([Sdf.Path("/World/asm/mount")])
    joint.CreateBody1Rel().SetTargets([Sdf.Path("/World/asm/disk")])
    joint.CreateAxisAttr().Set("Z")

# Ensure disk is a dynamic rigid body
disk_prim = stage.GetPrimAtPath("/World/asm/disk")
UsdPhysics.RigidBodyAPI.Apply(disk_prim)
mass_api = UsdPhysics.MassAPI.Apply(disk_prim)
mass_api.CreateMassAttr().Set(1.0)  # Reasonable mass

# Make sure a PhysicsScene exists
physics_scene = UsdPhysics.Scene.Get(stage, "/World")
if not physics_scene:
    physics_scene = UsdPhysics.Scene.Define(stage, Sdf.Path("/World"))
physics_scene.CreateTimeStepsPerSecondAttr().Set(60.0)  # Smooth simulation

# Apply or get DriveAPI for angular drive
drive = UsdPhysics.DriveAPI.Get(joint.GetPrim(), "angular")
if not drive:
    drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")
drive.CreateTypeAttr().Set("force")  # Force-based drive
drive.CreateStiffnessAttr().Set(0.0)  # No position correction for velocity drive
drive.CreateDampingAttr().Set(500.0)  # High damping for smooth motion
drive.CreateMaxForceAttr().Set(1000.0)  # Limit force

# Global variables for subscription (to keep it alive) and tracking time
_physics_subscription = None
_start_time = 0.0

def on_physics_step(step: float):
    global _start_time
    timeline = omni.timeline.get_timeline_interface()
    
    # Get current simulation time (in seconds)
    current_time = timeline.get_current_time()
    
    # Example: Vary velocity sinusoidally for slow oscillation (amplitude 1 deg/s, period ~10 seconds)
    # Adjust the formula for your desired changes, e.g.:
    # - For a step change: if current_time > 5.0: drive.GetTargetVelocityAttr().Set(0.5)
    velocity = math.sin(current_time * 0.628)  # sin(2*pi*f*t) with f=0.1 Hz
    drive.GetTargetVelocityAttr().Set(velocity)
    
    # Optional: Print for debugging (visible in Console)
    print(f"Updated velocity to {velocity} at time {current_time}")

# Subscribe to physics steps (runs only when simulation is playing)
_physics_subscription = _physx.get_physx_interface().subscribe_physics_step_events(on_physics_step)

# To unsubscribe later (e.g., in another script): _physics_subscription = None
print("Subscribed to physics steps. Press Play to start simulation and see dynamic changes.")