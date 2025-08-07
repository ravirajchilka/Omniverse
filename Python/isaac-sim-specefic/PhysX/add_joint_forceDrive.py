from pxr import Usd, UsdPhysics, Sdf
import omni.usd

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define joint path
joint_path = "/World/asm/joint"

# Create the revolute joint
joint = UsdPhysics.RevoluteJoint.Define(stage, joint_path)

# Set connected bodies
joint.CreateBody0Rel().SetTargets([Sdf.Path("/World/asm/mount")])
joint.CreateBody1Rel().SetTargets([Sdf.Path("/World/asm/disk")])

# Set joint axis
joint.CreateAxisAttr().Set("Z")

# Optionally define anchor points or limits here
# joint.CreateLocalPos0Attr().Set(Gf.Vec3f(0, 0, 0))
# joint.CreateLocalRot0Attr().Set(Gf.Quatf(1, 0, 0, 0))

# Make sure a PhysicsScene exists
UsdPhysics.Scene.Define(stage, Sdf.Path("/World"))



drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")

# Set the drive type: "force" or "acceleration"
# Example for force drive:
drive.CreateTypeAttr().Set("force")
# Alternatively, for acceleration drive:
# drive.CreateTypeAttr().Set("acceleration")

# Set other drive properties (adjust values as needed)
drive.CreateStiffnessAttr().Set(1.0)  # Stiffness for position control
drive.CreateDampingAttr().Set(10.0)     # Damping for velocity control
drive.CreateMaxForceAttr().Set(10000.0)  # Maximum force/torque limit (set to 0 or a large number for unlimited)

# Optionally set target position and velocity
drive.CreateTargetPositionAttr().Set(90.0)  # Target angle in degrees (for revolute joint)
drive.CreateTargetVelocityAttr().Set(3.0)  # Target angular velocity in degrees per