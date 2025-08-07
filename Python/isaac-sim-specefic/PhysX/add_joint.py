from pxr import Usd, UsdPhysics, Sdf
import omni.usd

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define joint path
joint_path = "/World/asm/r_joint"

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
