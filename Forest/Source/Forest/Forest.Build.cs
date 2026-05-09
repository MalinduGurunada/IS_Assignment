using UnrealBuildTool;

public class Forest : ModuleRules
{
    public Forest(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicIncludePaths.Add(ModuleDirectory);

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "NavigationSystem",   // UNavigationSystemV1, ARecastNavMesh
            "AIModule"            // UAIBlueprintHelperLibrary
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Slate",
            "SlateCore"
        });
    }
}
