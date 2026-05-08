#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "IS/ISTypes.h"
#include "ISGraphModifier.generated.h"

class AISNavigationGraph;

/**
 * UISGraphModifier — Role 2 (Malindu): Dynamic Adaptation
 *
 * Attach this component to any actor that needs to modify the graph
 * (e.g., AISBarricadeActor). It severs or restores edges in response
 * to environment events, remembering severed edges so they can be
 * restored when an obstacle is removed.
 */
UCLASS(ClassGroup=(IS), meta=(BlueprintSpawnableComponent), Category="IS Navigation")
class FOREST_API UISGraphModifier : public UActorComponent
{
    GENERATED_BODY()

public:
    UISGraphModifier();

    // Reference to the shared navigation graph in the level
    UPROPERTY(BlueprintReadWrite, Category="IS Dynamic")
    AISNavigationGraph* NavGraph = nullptr;

    // Search radius (world units) used to find edges near an obstacle position
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="IS Dynamic")
    float ObstacleRadius = 150.f;

protected:
    virtual void BeginPlay() override;

    // Stores severed edges: key="FromID_ToID", value=original weight
    UPROPERTY()
    TMap<FString, float> SeveredEdges;

public:
    // -----------------------------------------------------------------------
    // Role 2 (Malindu) — implement these
    // -----------------------------------------------------------------------

    /**
     * Find all edges whose midpoint falls within ObstacleRadius of Position,
     * sever them, and return the list of severed edge keys.
     */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    TArray<FString> SeverEdgesAtPosition(FVector Position, float Radius = -1.f);

    /**
     * Sever a specific edge by node IDs. Returns true if the edge existed.
     * Stores the original weight so it can be restored later.
     */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    bool SeverEdge(int32 FromID, int32 ToID);

    /**
     * Restore a previously severed edge. Returns true if restored.
     */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    bool RestoreEdge(int32 FromID, int32 ToID);

    /**
     * Restore all severed edges whose midpoint is within Radius of Position.
     */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    TArray<FString> RestoreEdgesAtPosition(FVector Position, float Radius = -1.f);

    UFUNCTION(BlueprintPure, Category="IS Dynamic")
    TArray<FString> GetSeveredEdges() const;

    UFUNCTION(BlueprintPure, Category="IS Dynamic")
    bool IsEdgeSevered(int32 FromID, int32 ToID) const;

private:
    static FString MakeEdgeKey(int32 FromID, int32 ToID);
    static void ParseEdgeKey(const FString& Key, int32& OutFromID, int32& OutToID);
};
