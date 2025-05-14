from pxr import Usd, UsdGeom, Sdf

def internal_reference(prim: Usd.Prim, ref_target_path: Sdf.Path):
    references: Usd.References = prim.GetReferences()
    references.AddIinternalReference(
        primPath = ref_target_path
    )

def external_reference(prim: Usd.Prim, ref_asset_path: str):
    references: Usd.References = prim.GetReferences()
    references.AddReference(
        assetPath = ref_asset_path
    )

usd_create_path = "E:/Software_Projects/openUSD_Isaac_sim_files/Box/blocks1.usda"

stage = Usd.Stage.CreateNew(usd_create_path)
block1 = UsdGeom.Xform.Define(stage, "/World/Block1")
external_reference(
    block1.GetPrim(),
    "E:/Software_Projects/openUSD_Isaac_sim_files/Box/Assets"   
)

stage.Save()


for prim in stage.Traverse():
    print("prim values {}", prim)


# Folder Structure
# /Block
# ├── Assets
# │ ├── Block_Blue.usd
# └── blocks.usda

