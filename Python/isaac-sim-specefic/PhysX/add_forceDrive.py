
from pxr import Usd, UsdPhysics, Sdf
import omni.usd

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define joint path
joint_path = "/World/asm/joint"

# Create the revolute joint
joint = UsdPhysics.RevoluteJoint.Get(stage, joint_path)

drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")

# Set the drive type: "force" or "acceleration"
# Example for force drive:
drive.CreateTypeAttr().Set("force")
# Alternatively, for acceleration drive:
# drive.CreateTypeAttr().Set("acceleration")

# Set other drive properties (adjust values as needed)
drive.CreateStiffnessAttr().Set(0.5)  # Stiffness for position control
drive.CreateDampingAttr().Set(0.5)     # Damping for velocity control
drive.CreateMaxForceAttr().Set(20000.0)  # Maximum force/torque limit (set to 0 or a large number for unlimited)

# Optionally set target position and velocity
drive.CreateTargetPositionAttr().Set(90.0)  # Target angle in degrees (for revolute joint)
drive.CreateTargetVelocityAttr().Set(5.0)  # Target angular velocity in degrees per