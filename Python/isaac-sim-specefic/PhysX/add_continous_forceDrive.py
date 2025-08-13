from pxr import Usd, UsdPhysics, Sdf
import omni.usd

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define joint path
joint_path = "/World/asm/joint"

# Create the revolute joint
joint = UsdPhysics.RevoluteJoint.Get(stage, joint_path)

# Add the drive
drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")

drive.CreateTypeAttr().Set("force")
drive.CreateStiffnessAttr().Set(0.05)
drive.CreateDampingAttr().Set(0.5)
drive.CreateMaxForceAttr().Set(30000.0)

# Set angular velocity for continuous rotation
drive.CreateTargetVelocityAttr().Set(20.0) # Adjust this value as needed for slow or fast rotation

