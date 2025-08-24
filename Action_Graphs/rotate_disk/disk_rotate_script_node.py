from pxr import Usd, UsdPhysics, Sdf, UsdGeom, Gf
import omni.usd

def compute(db):
    # Get the USD stage
    stage = omni.usd.get_context().get_stage()
    if not stage:
        print("Stage not available")
        return False

    # Define paths
    joint_path = "/World/asm/joint"
    disk_prim_path = "/World/asm/disk"

    # Create or get the revolute joint
    joint = UsdPhysics.RevoluteJoint.Get(stage, joint_path)
    if joint and joint.GetPrim().IsValid():
        # Add the drive
        drive = UsdPhysics.DriveAPI.Apply(joint.GetPrim(), "angular")
        drive.CreateTypeAttr().Set("force")
        drive.CreateStiffnessAttr().Set(0.05)
        drive.CreateDampingAttr().Set(0.5)
        drive.CreateMaxForceAttr().Set(30000.0)
        # Set angular velocity for continuous rotation
        drive.CreateTargetVelocityAttr().Set(db.inputs.in_float_angular_velocity if hasattr(db.inputs, "in_float_angular_velocity") else 500.0)
    else:
        print(f"Invalid or missing joint at {joint_path}")
        return False

    # Read current angle from disk prim
    current_angle = 0.0
    disk_prim = stage.GetPrimAtPath(disk_prim_path)
    if disk_prim and disk_prim.IsValid():
        # Get the transform using UsdGeom.Xformable
        xform = UsdGeom.Xformable(disk_prim)
        time = Usd.TimeCode.Default()  # Current frame
        transform = xform.ComputeLocalTransform(time)
        
        # Extract Z-axis rotation
        rotation = transform.ExtractRotation()
        euler_angles = rotation.Decompose(Gf.Vec3d(0, 0, 1))  # Decompose around Z-axis
        current_angle = euler_angles[2]  # Z rotation in degrees
        print(f"Computed angle: {current_angle}")

        # Debug: Check xformOp:rotateXYZ if it exists
        attr = disk_prim.GetAttribute("xformOp:rotateXYZ")
        if attr and attr.IsAuthored():
            angle_vec = attr.Get(time)
            print(f"xformOp:rotateXYZ value: {angle_vec}")
        else:
            print("xformOp:rotateXYZ not authored or missing")
    else:
        print(f"Invalid or missing disk prim at {disk_prim_path}")
        return False

    # Set output for Script Node
    db.outputs.out_float_current_angle = current_angle
    print(f"Output angle: {current_angle}")
    return True
