#include "IS/Secondary/ISDebugVisualizer.h"
#include "IS/Graph/ISNavigationGraph.h"
#include "DrawDebugHelpers.h"

UISDebugVisualizer::UISDebugVisualizer()
{
    PrimaryComponentTick.bCanEverTick = false;
}

// ---------------------------------------------------------------------------
// Role 4 (Oshan) — implementations
// ---------------------------------------------------------------------------

bool UISDebugVisualizer::ToggleDebug()
{
    // TODO (Oshan):
    // bDebugEnabled = !bDebugEnabled;
    // if (!bDebugEnabled) ClearDebug();
    // return bDebugEnabled;
    return false;
}

void UISDebugVisualizer::DrawGraph(AISNavigationGraph* NavGraph)
{
    // TODO (Oshan):
    // if (!bDebugEnabled || !NavGraph) return;
    //
    // UWorld* World = GetWorld();
    // for (auto& Pair : NavGraph->Nodes)
    //     FISGraphNode& Node = Pair.Value;
    //     DrawDebugSphere(World, Node.WorldLocation, NodeSphereRadius, 8,
    //                     FColor::White, false, LineLifetime);
    //
    //     DrawDebugString(World, Node.WorldLocation + FVector(0,0,40),
    //                     FString::Printf(TEXT("N%d"), Node.NodeID), nullptr,
    //                     FColor::White, LineLifetime);
    //
    //     for (int32 NeighborID : Node.NeighborIDs)
    //         if (NavGraph->Nodes.Contains(NeighborID))
    //             FVector NeighborLoc = NavGraph->Nodes[NeighborID].WorldLocation;
    //             DrawDebugLine(World, Node.WorldLocation, NeighborLoc,
    //                           FColor::Blue, false, LineLifetime, 0, 2.f);
}

void UISDebugVisualizer::DrawPath(const TArray<int32>& Path, AISNavigationGraph* NavGraph)
{
    // TODO (Oshan):
    // if (!bDebugEnabled || !NavGraph || Path.Num() == 0) return;
    //
    // UWorld* World = GetWorld();
    // for (int32 i = 0; i < Path.Num() - 1; i++)
    //     FVector From = NavGraph->Nodes[Path[i]].WorldLocation;
    //     FVector To   = NavGraph->Nodes[Path[i+1]].WorldLocation;
    //     DrawDebugLine(World, From, To, FColor::Green, false, LineLifetime, 0, 5.f);
    //
    // // Start node = Yellow, Goal node = Red
    // DrawDebugSphere(World, NavGraph->Nodes[Path[0]].WorldLocation,       50.f, 12, FColor::Yellow, false, LineLifetime);
    // DrawDebugSphere(World, NavGraph->Nodes[Path.Last()].WorldLocation,   50.f, 12, FColor::Red,    false, LineLifetime);
}

void UISDebugVisualizer::DrawFrontier(const TArray<int32>& FrontierIDs, AISNavigationGraph* NavGraph)
{
    // TODO (Oshan):
    // if (!bDebugEnabled || !NavGraph) return;
    //
    // for (int32 NodeID : FrontierIDs)
    //     if (NavGraph->Nodes.Contains(NodeID))
    //         DrawDebugSphere(GetWorld(), NavGraph->Nodes[NodeID].WorldLocation,
    //                         40.f, 8, FColor::Orange, false, 0.1f);  // 0.1s lifetime
}

void UISDebugVisualizer::ClearDebug()
{
    FlushPersistentDebugLines(GetWorld());
}
