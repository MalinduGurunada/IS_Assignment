#include "IS/Graph/ISNavigationGraph.h"
#include "Engine/TargetPoint.h"
#include "Kismet/GameplayStatics.h"

AISNavigationGraph::AISNavigationGraph()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AISNavigationGraph::BeginPlay()
{
    Super::BeginPlay();
    ExtractFromTargetPoints();
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

FString AISNavigationGraph::MakeEdgeKey(int32 FromID, int32 ToID)
{
    return FString::Printf(TEXT("%d_%d"), FromID, ToID);
}

// ---------------------------------------------------------------------------
// Node operations
// ---------------------------------------------------------------------------

void AISNavigationGraph::AddNode(int32 NodeID, FVector Location)
{
    // TODO (Hesara):
    // Create an FISGraphNode with the given NodeID and Location.
    // Add it to the Nodes map: Nodes.Add(NodeID, NewNode)
    // Tip: FISGraphNode NewNode; NewNode.NodeID = NodeID; NewNode.WorldLocation = Location;
}

bool AISNavigationGraph::HasNode(int32 NodeID) const
{
    // TODO (Hesara): return Nodes.Contains(NodeID)
    return false;
}

int32 AISNavigationGraph::GetNodeCount() const
{
    return Nodes.Num();
}

// ---------------------------------------------------------------------------
// Edge operations
// ---------------------------------------------------------------------------

void AISNavigationGraph::AddEdge(int32 FromID, int32 ToID, float Weight, bool bBidirectional)
{
    // TODO (Hesara):
    // 1. Check both nodes exist with HasNode(); log a warning and return if not
    // 2. Get pointer to FromNode: FISGraphNode* FromNode = Nodes.Find(FromID)
    // 3. Add ToID to FromNode->NeighborIDs if not already present
    // 4. Store: EdgeWeights.Add(MakeEdgeKey(FromID, ToID), Weight)
    // 5. If bBidirectional, repeat steps 2-4 in the reverse direction
}

void AISNavigationGraph::RemoveEdge(int32 FromID, int32 ToID, bool bBidirectional)
{
    // TODO (Malindu — called by ISGraphModifier):
    // 1. Remove MakeEdgeKey(FromID, ToID) from EdgeWeights
    // 2. Remove ToID from Nodes[FromID].NeighborIDs
    // 3. If bBidirectional, remove the reverse as well
}

bool AISNavigationGraph::HasEdge(int32 FromID, int32 ToID) const
{
    // TODO (Hesara): return EdgeWeights.Contains(MakeEdgeKey(FromID, ToID))
    return false;
}

float AISNavigationGraph::GetEdgeWeight(int32 FromID, int32 ToID) const
{
    // TODO (Hesara):
    // const float* Weight = EdgeWeights.Find(MakeEdgeKey(FromID, ToID));
    // return Weight ? *Weight : TNumericLimits<float>::Max();
    return TNumericLimits<float>::Max();
}

TArray<FISEdgePair> AISNavigationGraph::GetNeighbors(int32 NodeID) const
{
    // TODO (Hesara):
    // 1. const FISGraphNode* Node = Nodes.Find(NodeID); if nullptr, return empty
    // 2. For each NeighborID in Node->NeighborIDs:
    //      FISEdgePair Pair; Pair.NeighborID = NeighborID; Pair.Weight = GetEdgeWeight(NodeID, NeighborID);
    //      Result.Add(Pair)
    // 3. Return Result
    return TArray<FISEdgePair>();
}

int32 AISNavigationGraph::GetEdgeCount() const
{
    return EdgeWeights.Num();
}

// ---------------------------------------------------------------------------
// Graph extraction — ROLE 1 (Hesara)
// ---------------------------------------------------------------------------

void AISNavigationGraph::ExtractFromTargetPoints()
{
    // TODO (Hesara — core Role 1 implementation):
    //
    // Step 1: Clear existing graph data
    //   Nodes.Empty();
    //   EdgeWeights.Empty();
    //
    // Step 2: Collect all TargetPoint actors in the level
    //   TArray<AActor*> TargetPoints;
    //   UGameplayStatics::GetAllActorsOfClass(GetWorld(), ATargetPoint::StaticClass(), TargetPoints);
    //
    // Step 3: Add a node for each TargetPoint
    //   for (int32 i = 0; i < TargetPoints.Num(); i++)
    //       AddNode(i, TargetPoints[i]->GetActorLocation());
    //
    // Step 4: Connect nearby nodes with weighted edges
    //   for (int32 i = 0; i < TargetPoints.Num(); i++)
    //       for (int32 j = i + 1; j < TargetPoints.Num(); j++)
    //           float Dist = FVector::Dist(Nodes[i].WorldLocation, Nodes[j].WorldLocation);
    //           if (Dist <= ProximityThreshold)
    //               AddEdge(i, j, Dist);
    //
    // Step 5: Log the result
    //   UE_LOG(LogTemp, Log, TEXT("ISNavigationGraph: built %d nodes, %d directed edges"),
    //          GetNodeCount(), GetEdgeCount());

    UE_LOG(LogTemp, Warning, TEXT("ISNavigationGraph: ExtractFromTargetPoints() not yet implemented (Role 1 - Hesara)"));
}

// ---------------------------------------------------------------------------
// Recalculation trigger
// ---------------------------------------------------------------------------

void AISNavigationGraph::TriggerRecalculation()
{
    OnGraphChanged.Broadcast();
}
