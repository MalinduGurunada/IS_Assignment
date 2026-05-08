#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ISDebugVisualizer.generated.h"

class AISNavigationGraph;

/**
 * UISDebugVisualizer — Role 4 (Oshan): Toggleable Debug Overlay
 *
 * Attach this component to AISNavigationGraph (or any actor).
 * When enabled, it draws the graph edges, search frontiers, and
 * calculated paths directly into the 3D viewport using debug draw calls.
 *
 * Toggle with the F3 key (bind in Level Blueprint or PlayerController).
 */
UCLASS(ClassGroup=(IS), meta=(BlueprintSpawnableComponent), Category="IS Navigation")
class LAB_API UISDebugVisualizer : public UActorComponent
{
    GENERATED_BODY()

public:
    UISDebugVisualizer();

    // True when debug overlay is active
    UPROPERTY(BlueprintReadOnly, Category="IS Debug")
    bool bDebugEnabled = false;

    // How long debug lines persist (seconds; -1 = permanent until cleared)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="IS Debug")
    float LineLifetime = 0.f;

    // Sphere radius for node markers
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="IS Debug")
    float NodeSphereRadius = 30.f;

public:
    // -----------------------------------------------------------------------
    // Role 4 (Oshan) — implement these
    // -----------------------------------------------------------------------

    /** Flip debug overlay on/off. Returns new state. */
    UFUNCTION(BlueprintCallable, Category="IS Debug")
    bool ToggleDebug();

    /** Draw all nodes (spheres) and edges (lines) of the graph. */
    UFUNCTION(BlueprintCallable, Category="IS Debug")
    void DrawGraph(AISNavigationGraph* NavGraph);

    /** Draw the final path as thick green lines with start/goal markers. */
    UFUNCTION(BlueprintCallable, Category="IS Debug")
    void DrawPath(const TArray<int32>& Path, AISNavigationGraph* NavGraph);

    /** Draw the current frontier nodes as orange spheres (called per-step). */
    UFUNCTION(BlueprintCallable, Category="IS Debug")
    void DrawFrontier(const TArray<int32>& FrontierIDs, AISNavigationGraph* NavGraph);

    /** Clear all persistent debug geometry (FlushPersistentDebugLines). */
    UFUNCTION(BlueprintCallable, Category="IS Debug")
    void ClearDebug();
};
