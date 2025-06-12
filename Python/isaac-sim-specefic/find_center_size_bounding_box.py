
from pxr import UsdGeom, Usd, Gf, UsdPhysics
import carb

rod_prim = stage.GetPrimAtPath(pendulum_rod_path)
if not rod_prim or not rod_prim.IsValid():
    carb.log_warn(f"Prim {pendulum_rod_path} not found or invalid.")
else:
    imageable = UsdGeom.Imageable(rod_prim)
    bbox = imageable.ComputeLocalBound(Usd.TimeCode.Default(), "default")
    bbox_range = bbox.GetRange()
    min_point = bbox_range.GetMin()
    max_point = bbox_range.GetMax()
    center = (min_point + max_point) * 0.5
    size = max_point - min_point

    print("Bounding Box Min:", min_point)
    print("Bounding Box Max:", max_point)
    print("Center:", center)
    print("Size (Extent):", size)
