using UnrealBuildTool;
using System.Collections.Generic;

public class LabTarget : TargetRules
{
    public LabTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5Latest;
        ExtraModuleNames.Add("Lab");
    }
}
