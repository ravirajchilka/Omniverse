from pxr import Usd, UsdPhysics, Sdf
import omni.usd

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define joint path
joint_path = "/World/asm/joint"

# Create or get the revolute joint
joint = UsdPhysics.RevoluteJoint.Get(stage, joint_path)
if not joint:
    print(f"Joint at {joint_path} not found!")
    exit()

# Add the drive
drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")

# Configure the drive for position control
drive.CreateTypeAttr().Set("force")  # Use force-based control
"""
The high stiffness value (1000000.0) makes the joint try to reach the target position (45 degrees) very aggressively, which can cause overshooting or oscillations. If damping is too low, the joint may oscillate or "bounce" around the target.
Solution: Increase the damping to smooth out the motion and slightly reduce stiffness to make the response less aggressive.
"""
drive.CreateStiffnessAttr().Set(100000.0)  # Reduced stiffness
drive.CreateDampingAttr().Set(50000.0)     # Increased damping
drive.CreateMaxForceAttr().Set(30.0)    # Maximum force to apply

# Set the target position to 45 degrees
drive.CreateTargetPositionAttr().Set(180.0)  # Target angle in degrees

