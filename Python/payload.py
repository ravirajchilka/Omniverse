from pxr import Usd, Sdf, UsdGeom

def add_payload(prim: Usd.Prim, payload_asset_path: str):
    payloads: Usd.Payloads = prim.GetPayloads()
    payloads.AddPayload(
        assetPath = payload_asset_path
    )

stage = Usd.Stage.CreateNew("E:/Software_Projects/openUSD_Isaac_sim_files/Box/blocks.usda")
block1 = UsdGeom.Xform.Define(stage,'/World/Block1')

add_payload(block1.GetPrim(), "./Assets") # relative path

stage.Save()

# Folder Structure
# /Block
# ├── Assets
# │ ├── Block_Blue.usd
# └── blocks.usda
