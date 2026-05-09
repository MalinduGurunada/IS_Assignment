using UnrealBuildTool;
using System.Collections.Generic;

public class ForestTarget : TargetRules
{
    public ForestTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("Forest");
    }
}
