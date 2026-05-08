#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "IS/ISTypes.h"
#include "ISNavigationGraph.generated.h"

/**
 * AISNavigationGraph — Role 1 (Hesara): Custom Graph Formulation
 *
 * Place one instance of this actor in the level.
 * At BeginPlay it reads all ATargetPoint actors and builds the
 * navigation graph automatically (ExtractFromTargetPoints).
 *
 * Other students access this actor to run their search algorithms.
 */
UCLASS(BlueprintType, Blueprintable, Category="IS Navigation")
class FOREST_API AISNavigationGraph : public AActor
{
    GENERATED_BODY()

public:
    AISNavigationGraph();

    // -----------------------------------------------------------------------
    // Graph data — stored as adjacency list
    // -----------------------------------------------------------------------

    // All nodes keyed by NodeID
    UPROPERTY(BlueprintReadWrite, Category="IS Graph")
    TMap<int32, FISGraphNode> Nodes;

    // Edge weights keyed by "FromID_ToID"
    UPROPERTY(BlueprintReadWrite, Category="IS Graph")
    TMap<FString, float> EdgeWeights;

    // Maximum world-unit distance between two nodes to auto-connect them
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="IS Graph")
    float ProximityThreshold = 300.f;

protected:
    virtual void BeginPlay() override;

public:
    // -----------------------------------------------------------------------
    // Node operations
    // -----------------------------------------------------------------------

    UFUNCTION(BlueprintCallable, Category="IS Graph")
    void AddNode(int32 NodeID, FVector Location);

    UFUNCTION(BlueprintCallable, Category="IS Graph")
    bool HasNode(int32 NodeID) const;

    UFUNCTION(BlueprintPure, Category="IS Graph")
    int32 GetNodeCount() const;

    // -----------------------------------------------------------------------
    // Edge operations
    // -----------------------------------------------------------------------

    UFUNCTION(BlueprintCallable, Category="IS Graph")
    void AddEdge(int32 FromID, int32 ToID, float Weight = 1.f, bool bBidirectional = true);

    UFUNCTION(BlueprintCallable, Category="IS Graph")
    void RemoveEdge(int32 FromID, int32 ToID, bool bBidirectional = true);

    UFUNCTION(BlueprintPure, Category="IS Graph")
    bool HasEdge(int32 FromID, int32 ToID) const;

    UFUNCTION(BlueprintPure, Category="IS Graph")
    float GetEdgeWeight(int32 FromID, int32 ToID) const;

    UFUNCTION(BlueprintCallable, Category="IS Graph")
    TArray<FISEdgePair> GetNeighbors(int32 NodeID) const;

    UFUNCTION(BlueprintPure, Category="IS Graph")
    int32 GetEdgeCount() const;

    // -----------------------------------------------------------------------
    // Graph extraction — Role 1 (Hesara) implements this
    // -----------------------------------------------------------------------

    /**
     * Reads all ATargetPoint actors in the level, creates a GraphNode for each,
     * then connects nearby nodes (distance <= ProximityThreshold) with weighted edges.
     * Called automatically at BeginPlay.
     */
    UFUNCTION(BlueprintCallable, Category="IS Graph|Extraction")
    void ExtractFromTargetPoints();

    // -----------------------------------------------------------------------
    // Recalculation trigger — called by Malindu after edge changes
    // -----------------------------------------------------------------------

    // Bind this in Blueprint to call A* whenever the graph changes
    UPROPERTY(BlueprintAssignable, Category="IS Graph")
    FSimpleDynamicMulticastDelegate OnGraphChanged;

    UFUNCTION(BlueprintCallable, Category="IS Graph")
    void TriggerRecalculation();

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------

    static FString MakeEdgeKey(int32 FromID, int32 ToID);
};
