from pxr import UsdPhysics, Usd
import omni.usd, math

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Define the joint path
joint_path = "/World/asm/joint"
joint = UsdPhysics.RevoluteJoint.Get(stage, joint_path)

# Apply angular drive
drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")
drive.CreateTypeAttr().Set("force")
drive.CreateStiffnessAttr().Set(100000.0)  # Reduced stiffness
drive.CreateDampingAttr().Set(50000.0)     # Increased damping
drive.CreateMaxForceAttr().Set(30.0)  
#drive.CreateTargetVelocityAttr().Set(1.0)  # constant speed (rad/s)

# This function is called every frame by the Script Node
def compute(db):
    # Get input angle (degrees) from Script Node input
    target_angle_deg = db.inputs.in_float_angle
    if target_angle_deg is None:
        return

    # Set the joint target position
    drive.CreateTargetPositionAttr().Set(target_angle_deg)

    # Optionally write the angle back to output (if needed)
    db.outputs.out_float_angle = target_angle_deg

