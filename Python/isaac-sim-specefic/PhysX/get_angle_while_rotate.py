from pxr import Usd, UsdGeom, Gf
import omni.usd
import math

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Adjust these paths to your actual body prim paths connected by the joint
body0_path = "/World/asm/mount"
body1_path = "/World/asm/disk"

# Get prims
body0_prim = stage.GetPrimAtPath(body0_path)
body1_prim = stage.GetPrimAtPath(body1_path)

if not body0_prim or not body0_prim.IsValid():
    print(f"Invalid prim path: {body0_path}")

if not body1_prim or not body1_prim.IsValid():
    print(f"Invalid prim path: {body1_path}")

# Get Xformable interfaces to access local transforms
body0_xform = UsdGeom.Xformable(body0_prim)
body1_xform = UsdGeom.Xformable(body1_prim)

# Use current simulation time or default
time_code = Usd.TimeCode.Default()

# Get the local transformation matrix for each body
body0_transform = body0_xform.GetLocalTransformation(time_code)
body1_transform = body1_xform.GetLocalTransformation(time_code)

# Calculate relative transform from body0 to body1
relative_transform = body0_transform.GetInverse() * body1_transform

# Extract rotation (Gf.Rotation) from the relative transform
rotation = relative_transform.ExtractRotation()

# Convert to quaternion (Gf.Quatd)
rel_rotation = rotation.GetQuat()

# Extract quaternion components
real = rel_rotation.GetReal()
imag = rel_rotation.GetImaginary()  # Gf.Vec3d

# Calculate half angle and full angle (radians)
half_angle = math.acos(real)
angle_radians = 2.0 * half_angle

# Normalize imaginary part to get rotation axis
axis = imag.GetNormalized()

# Define your joint's rotation axis (adjust depending on your joint setup)
joint_axis = Gf.Vec3d(0, 0, 1)  # Example: Z axis

# Determine the sign of the angle based on closeness of axes
if (axis - joint_axis).GetLength() < 1e-3:
    angle_along_joint = angle_radians
else:
    angle_along_joint = -angle_radians

# Convert angle to degrees
angle_degrees = angle_along_joint * (180.0 / math.pi)

print(f"Revolute joint angle around axis {joint_axis}: {angle_degrees} degrees")


