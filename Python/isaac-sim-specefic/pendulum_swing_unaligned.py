from pxr import UsdGeom, Usd, Gf, UsdPhysics, Sdf
import carb
import omni.usd

# Get current stage
stage = omni.usd.get_context().get_stage()

# Define your pendulum part paths
pendulum_rod_path = "/World/PAss/PAss/pendulum_rod"
pendulum_stand_path = "/World/PAss/PAss/pendulum_stand"

# Get rod prim and compute top center point in local space
rod_prim = stage.GetPrimAtPath(Sdf.Path(pendulum_rod_path))
if not rod_prim or not rod_prim.IsValid():
    carb.log_warn(f"Prim {pendulum_rod_path} not found or invalid.")
    top_center = Gf.Vec3f(0.0, 0.0, 0.0)  # Fallback pivot
else:
    # Apply PhysxCollisionAPI and set convexHull approximation to fix PhysX warnings
    from pxr import PhysxSchema
    collision_api = PhysxSchema.PhysxCollisionAPI.Apply(rod_prim)
    # Some versions of Isaac Sim don't have CreateApproximationAttr, so use CreateAttribute fallback
    approx_attr = rod_prim.GetAttribute("physxCollision:approximation")
    if not approx_attr:
        approx_attr = rod_prim.CreateAttribute("physxCollision:approximation", Sdf.ValueTypeNames.Token)
    approx_attr.Set("convexHull")

    imageable = UsdGeom.Imageable(rod_prim)
    bbox = imageable.ComputeLocalBound(Usd.TimeCode.Default(), "default")
    bbox_range = bbox.GetRange()
    min_point = bbox_range.GetMin()
    max_point = bbox_range.GetMax()
    center = (min_point + max_point) * 0.5

    # Calculate top center point (x,z center at max y)
    top_center = Gf.Vec3f(center[0], max_point[1], center[2])

# Define joint prim path
joint_path = "/World/PAss/PAss/RevoluteJoint"
joint_prim = stage.DefinePrim(Sdf.Path(joint_path), "PhysicsRevoluteJoint")
joint = UsdPhysics.RevoluteJoint(joint_prim)

# Attach joint bodies
joint.CreateBody0Rel().SetTargets([Sdf.Path(pendulum_stand_path)])
joint.CreateBody1Rel().SetTargets([Sdf.Path(pendulum_rod_path)])

# Set joint pivots
joint.CreateLocalPos0Attr().Set(Gf.Vec3f(0.0, 0.0, 0.0))  # Stand pivot at origin
joint.CreateLocalPos1Attr().Set(top_center)              # Rod pivot at top center

# Set joint axis to Z (pendulum swings in X-Y plane)
joint.CreateAxisAttr().Set("Z")  # Just a string, no Tf.Token

# Identity rotations - no additional rotation needed if hinge axis Z is default
joint.CreateLocalRot0Attr().Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))
joint.CreateLocalRot1Attr().Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))

print("✅ RevoluteJoint adjusted with top-center pivot and Z-axis hinge (without Tf).")
print("✅ Applied convexHull collision approximation to pendulum rod.")
