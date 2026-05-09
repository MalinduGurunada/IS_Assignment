using UnrealBuildTool;
using System.Collections.Generic;

public class LabEditorTarget : TargetRules
{
    public LabEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("Lab");
    }
}
