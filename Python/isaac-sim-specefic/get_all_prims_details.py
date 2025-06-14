from pxr import Usd, Sdf

def print_prim_details(stage, root_path="/World"):
    root_prim = stage.GetPrimAtPath(Sdf.Path(root_path))
    if not root_prim or not root_prim.IsValid():
        print(f"Root prim '{root_path}' not found or invalid.")
        return

    def recurse_print(prim, level=0):
        indent = "  " * level
        print(f"{indent}Prim path: {prim.GetPath()}")
        print(f"{indent}  Type: {prim.GetTypeName()}")
        print(f"{indent}  IsActive: {prim.IsActive()}")
        print(f"{indent}  IsValid: {prim.IsValid()}")
        print()

        # Recursively print children
        for child in prim.GetChildren():
            recurse_print(child, level + 1)

    recurse_print(root_prim)

# Usage example:
import omni.usd
stage = omni.usd.get_context().get_stage()
print_prim_details(stage, "/World")  # Change "/World" to any root path you want
