import omni
from pxr import UsdPhysics

stage = omni.usd.get_context().get_stage()

pendulum_rod_path = "/World/new/p_rod"
pendulum_stand_path = "/World/new/p_stand"

joint_path = "/World/new/p_rod_joint"
joint = UsdPhysics.RevoluteJoint.Define(stage, joint_path)
joint.CreateBody0Rel().SetTargets([pendulum_stand_path])
joint.CreateBody1Rel().SetTargets([pendulum_rod_path])
joint.CreateAxisAttr().Set("Z")
