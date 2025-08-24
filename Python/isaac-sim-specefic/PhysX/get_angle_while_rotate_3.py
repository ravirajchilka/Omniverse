from pxr import Usd, UsdGeom, Gf
import omni.usd
import omni.physx as _physx
import math

# Get the USD stage
stage = omni.usd.get_context().get_stage()

# Prim paths
body0_path = "/World/asm/mount"
body1_path = "/World/asm/disk"

# Get prims
body0_prim = stage.GetPrimAtPath(body0_path)
body1_prim = stage.GetPrimAtPath(body1_path)

if not body0_prim or not body0_prim.IsValid():
    print(f"Invalid prim path: {body0_path}")
if not body1_prim or not body1_prim.IsValid():
    print(f"Invalid prim path: {body1_path}")

# Xformable interfaces
body0_xf = UsdGeom.Xformable(body0_prim)
body1_xf = UsdGeom.Xformable(body1_prim)

# Joint axis (adjust if different)
joint_axis = Gf.Vec3d(0, 0, 1)

# Variables for unwrapping
_last_angle = None
_cumulative_angle = 0.0

# Function to compute joint angle each physics step
def compute_joint_angle():
    global _last_angle, _cumulative_angle

    # Current world transforms from simulation
    T0 = body0_xf.ComputeLocalToWorldTransform(0)
    T1 = body1_xf.ComputeLocalToWorldTransform(0)

    # Relative rotation
    rel_rotation = (T0.GetInverse() * T1).ExtractRotation().GetQuat()

    # Instant angle in radians
    half_angle = math.acos(rel_rotation.GetReal())
    angle_radians = 2.0 * half_angle

    # Rotation axis
    axis = rel_rotation.GetImaginary().GetNormalized() if rel_rotation.GetImaginary().GetLength() > 1e-6 else joint_axis

    # Signed angle along joint axis
    sign = 1.0 if axis * joint_axis >= 0 else -1.0
    angle_degrees = math.degrees(angle_radians * sign)

    # Angle unwrapping for continuous rotation
    if _last_angle is not None:
        delta = angle_degrees - _last_angle
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        _cumulative_angle += delta

    _last_angle = angle_degrees

    print(f"Instant: {angle_degrees:.2f}°, Cumulative: {_cumulative_angle:.2f}°")

# Hook into PhysX simulation steps
physx = _physx.get_physx_interface()
subscription = physx.subscribe_physics_step_events(lambda dt: compute_joint_angle())

# To stop printing later:
# physx.unsubscribe_physics_step_events(subscription)

