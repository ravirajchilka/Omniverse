#### 1st step
from pxr import Usd, UsdPhysics

# Open the USD stage
stage = Usd.Stage.Open('D:\\DOCUMENTS\\SOLIDWORKS_parts\\622_block.usdc')

# Path to your joint
joint_path = "/World/block_assembly/joint"
joint_prim = stage.GetPrimAtPath(joint_path)

# Set the lower and upper limits in radians
lower_limit = 30
upper_limit = 140
import math
lower_limit_rad = lower_limit
upper_limit_rad = upper_limit

# Set the attributes
joint_prim.GetAttribute('physics:lowerLimit').Set(lower_limit_rad)
joint_prim.GetAttribute('physics:upperLimit').Set(upper_limit_rad)

# Optionally, ensure limits are enabled (custom attribute)
joint_prim.GetAttribute('physxJointLimitsEnabled').Set(True)

# Save changes
stage.GetRootLayer().Save()



#### 2nd step
import omni.usd
from pxr import Usd, UsdPhysics, Sdf
import carb
import sys

def main():
    stage = omni.usd.get_context().get_stage()
    if not stage:
        carb.log_error("No USD stage loaded! Load a USD stage first.")
        sys.exit(1)

    joint_path = "/World/block_assembly/joint"
    joint_prim = stage.GetPrimAtPath(joint_path)
    if not joint_prim.IsValid():
        carb.log_error(f"Joint prim not found at {joint_path}")
        sys.exit(1)

    if not UsdPhysics.RevoluteJoint.HasAPI(joint_prim):
        carb.log_error("Prim is not a revolute joint!")
        sys.exit(1)
    revolute_api = UsdPhysics.RevoluteJoint(joint_prim)

    # Set joint limits in degrees
    # lower_limit = 30.0
    # upper_limit = 180.0
    revolute_api.CreateLowerLimitAttr().Set(lower_limit)
    revolute_api.CreateUpperLimitAttr().Set(upper_limit)
    joint_prim.CreateAttribute("physxJointLimitsEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    joint_prim.CreateAttribute("physxJointLowerLimit", Sdf.ValueTypeNames.Float).Set(lower_limit)
    joint_prim.CreateAttribute("physxJointUpperLimit", Sdf.ValueTypeNames.Float).Set(upper_limit)

    # Add DriveAPI for smooth, motor-like motion
    drive_api = UsdPhysics.DriveAPI.Apply(joint_prim, "angular")
    drive_api.CreateTypeAttr().Set("position")
    drive_api.CreateTargetPositionAttr().Set(upper_limit)      # Move from 0 to 180 degrees
    drive_api.CreateStiffnessAttr().Set(10.0)            # Lower = slower, smoother
    drive_api.CreateDampingAttr().Set(500.0)             # Higher = less overshoot
    drive_api.CreateMaxForceAttr().Set(500.0)            # Limit force for realism

    # (Optional) Set max joint velocity for even more control
    joint_prim.CreateAttribute("physxJoint:maxJointVelocity", Sdf.ValueTypeNames.Float).Set(30.0)  # degrees/sec

    carb.log_info("Joint limits set 0–180°, DriveAPI applied for motor-like motion.")

    output_path = "E:/temp/modified_stage.usd"
    stage.Export(output_path)
    carb.log_info(f"Exported stage to {output_path}")

if __name__ == "__main__":
    main()



#### 3rd step
import omni
from omni.isaac.dynamic_control import _dynamic_control

pendulum_rod_path = "/World/block_assembly/block"
dc = _dynamic_control.acquire_dynamic_control_interface()
rod = dc.get_rigid_body(pendulum_rod_path)
if rod is not None:
    # Apply torque (x, y, z) in Newton-meters; False = global frame, True = local frame
    dc.apply_body_torque(rod, (0.0, 0.0, 0.4), False)
    print("Torque applied to the rod.")
else:
    print("Rod not found. Make sure simulation is running and rod has physics enabled.")
