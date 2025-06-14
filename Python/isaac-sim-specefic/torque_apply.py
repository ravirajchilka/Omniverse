# max angular velocity set to 5000 or 4000 and dmaping set to 0.0
# start simulation then apply torque

import omni
from omni.isaac.dynamic_control import _dynamic_control

pendulum_rod_path = "/World/new/p_rod"
dc = _dynamic_control.acquire_dynamic_control_interface()
rod = dc.get_rigid_body(pendulum_rod_path)
if rod is not None:
    # Apply torque (x, y, z) in Newton-meters; False = global frame, True = local frame
    dc.apply_body_torque(rod, (0.0, 0.0, 5.0), False)
    print("Torque applied to the rod.")
else:
    print("Rod not found. Make sure simulation is running and rod has physics enabled.")
