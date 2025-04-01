#define NOMINMAX
#include <windows.h>




#include "pxr/usd/usd/stage.h"  
#include "pxr/usd/usdGeom/cube.h"  
#include "pxr/usd/usdGeom/xform.h"  
#include "pxr/base/gf/vec3d.h"  
#include "pxr/usd/usd/timeCode.h"  
#include <iostream>  
  
PXR_NAMESPACE_USING_DIRECTIVE  
  
int main() {  
    // Create a new USD stage  
    UsdStageRefPtr stage = UsdStage::CreateNew("move_box_animated.usda");  
      
    // Set up a default prim  
    UsdGeomXform root = UsdGeomXform::Define(stage, SdfPath("/World"));  
    stage->SetDefaultPrim(root.GetPrim());  
      
    // Create a box (cube)  
    UsdGeomCube box = UsdGeomCube::Define(stage, SdfPath("/World/Box"));  
    box.GetSizeAttr().Set(0.5); // Set the size of the cube to 0.5 units  
      
    // Get the Xformable interface for the box to handle transformations  
    UsdGeomXformable boxXform(box.GetPrim());  
      
    // Add a translation op to the xform stack  
    UsdGeomXformOp translateOp = boxXform.AddTranslateOp();  
      
    // Setup animation time codes  
    double startTime = 1.0;  
    double endTime = 100.0;  
    stage->SetStartTimeCode(startTime);  
    stage->SetEndTimeCode(endTime);  
      
    // Animate the box along the x-axis: move 0.05 units per frame over 100 frames.  
    for (int frame = 1; frame <= 100; frame++) {  
        double xPos = (frame - 1) * 0.05;  
        // Setting the translation keyframe for the current frame.  
        translateOp.Set(GfVec3d(xPos, 0.0, 0.0), UsdTimeCode(frame));  
    }  
      
    // Save the stage  
    stage->GetRootLayer()->Save();  
      
    std::cout << "Animated USD file created: move_box_animated.usda" << std::endl;  
      
    return 0;  
}  
