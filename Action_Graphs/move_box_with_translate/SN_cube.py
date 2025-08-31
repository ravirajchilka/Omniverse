import omni.usd
from pxr import Gf

def compute(db):
    """
    Moves the cube along Y-axis using the float input from TokenToFloat node.
    """

    y_value = db.inputs.velocity_value  # must exactly match the input attribute

    prim_path = "/World/Cube"
    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath(prim_path)

    if prim.IsValid():
        if not prim.HasAttribute("xformOp:translate"):
            prim.AddTranslateOp()

        current_transform = prim.GetAttribute("xformOp:translate").Get() or Gf.Vec3d(0,0,0)
        new_transform = Gf.Vec3d(current_transform[0], y_value, current_transform[2])
        prim.GetAttribute("xformOp:translate").Set(new_transform)

        print(f"[Cube Script Node] Applied Y={y_value}")

    return True

