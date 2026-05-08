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
    FISGraphNode NewNode;
    NewNode.NodeID = NodeID;
    NewNode.WorldLocation = Location;
    Nodes.Add(NodeID, NewNode);
}

bool AISNavigationGraph::HasNode(int32 NodeID) const
{
    return Nodes.Contains(NodeID);
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
    if (!Nodes.Contains(FromID) || !Nodes.Contains(ToID)) return;
    EdgeWeights.Add(MakeEdgeKey(FromID, ToID), Weight);
    Nodes[FromID].NeighborIDs.AddUnique(ToID);
    if (bBidirectional)
    {
        EdgeWeights.Add(MakeEdgeKey(ToID, FromID), Weight);
        Nodes[ToID].NeighborIDs.AddUnique(FromID);
    }
}

void AISNavigationGraph::RemoveEdge(int32 FromID, int32 ToID, bool bBidirectional)
{
    EdgeWeights.Remove(MakeEdgeKey(FromID, ToID));
    if (Nodes.Contains(FromID)) Nodes[FromID].NeighborIDs.Remove(ToID);
    if (bBidirectional)
    {
        EdgeWeights.Remove(MakeEdgeKey(ToID, FromID));
        if (Nodes.Contains(ToID)) Nodes[ToID].NeighborIDs.Remove(FromID);
    }
}

bool AISNavigationGraph::HasEdge(int32 FromID, int32 ToID) const
{
    return EdgeWeights.Contains(MakeEdgeKey(FromID, ToID));
}

float AISNavigationGraph::GetEdgeWeight(int32 FromID, int32 ToID) const
{
    const float* Weight = EdgeWeights.Find(MakeEdgeKey(FromID, ToID));
    return Weight ? *Weight : TNumericLimits<float>::Max();
}

TArray<FISEdgePair> AISNavigationGraph::GetNeighbors(int32 NodeID) const
{
    TArray<FISEdgePair> Result;
    const FISGraphNode* Node = Nodes.Find(NodeID);
    if (!Node) return Result;
    for (int32 NID : Node->NeighborIDs)
    {
        FISEdgePair Pair;
        Pair.NeighborID = NID;
        Pair.Weight = GetEdgeWeight(NodeID, NID);
        Result.Add(Pair);
    }
    return Result;
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
    Nodes.Empty();
    EdgeWeights.Empty();

    TArray<AActor*> TargetPoints;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), ATargetPoint::StaticClass(), TargetPoints);

    for (int32 i = 0; i < TargetPoints.Num(); i++)
        AddNode(i, TargetPoints[i]->GetActorLocation());

    for (int32 i = 0; i < TargetPoints.Num(); i++)
    {
        for (int32 j = i + 1; j < TargetPoints.Num(); j++)
        {
            float Dist = FVector::Dist(Nodes[i].WorldLocation, Nodes[j].WorldLocation);
            if (Dist <= ProximityThreshold)
                AddEdge(i, j, Dist, true);
        }
    }

    UE_LOG(LogTemp, Log, TEXT("ISNavigationGraph: extracted %d nodes, %d directed edges"),
           GetNodeCount(), GetEdgeCount());
    TriggerRecalculation();
}

// ---------------------------------------------------------------------------
// Recalculation trigger
// ---------------------------------------------------------------------------

void AISNavigationGraph::TriggerRecalculation()
{
    OnGraphChanged.Broadcast();
}
