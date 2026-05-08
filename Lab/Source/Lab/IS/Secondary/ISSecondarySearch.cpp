#include "IS/Secondary/ISSecondarySearch.h"
#include "IS/Graph/ISNavigationGraph.h"

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

TArray<int32> UISSecondarySearch::ReconstructPath(const TMap<int32, int32>& CameFrom,
                                                   int32 StartID, int32 GoalID)
{
    // TODO (Oshan): same as AStarSearch::ReconstructPath — walk CameFrom backwards, reverse
    return TArray<int32>();
}

float UISSecondarySearch::ComputePathCost(AISNavigationGraph* NavGraph, const TArray<int32>& Path)
{
    // TODO (Oshan):
    // float Total = 0.f;
    // for (int32 i = 0; i < Path.Num() - 1; i++)
    //     Total += NavGraph->GetEdgeWeight(Path[i], Path[i+1]);
    // return Total;
    return 0.f;
}

// ---------------------------------------------------------------------------
// BFS — Role 4 (Oshan)
// ---------------------------------------------------------------------------

FISPathResult UISSecondarySearch::BreadthFirstSearch(AISNavigationGraph* NavGraph,
                                                      int32 StartID, int32 GoalID)
{
    FISPathResult Result;

    if (!NavGraph) return Result;

    if (StartID == GoalID)
    {
        Result.Path.Add(StartID);
        Result.bFound = true;
        return Result;
    }

    // TODO (Oshan — implement BFS):
    //
    // TQueue<int32> Queue;                          // FIFO queue
    // TSet<int32> Visited;
    // TMap<int32, int32> CameFrom;
    //
    // Queue.Enqueue(StartID);
    // Visited.Add(StartID);
    //
    // while (!Queue.IsEmpty())
    //     int32 Current;
    //     Queue.Dequeue(Current);
    //     Result.NodesExplored++;
    //
    //     for (FISEdgePair& Edge : NavGraph->GetNeighbors(Current))
    //         if (Visited.Contains(Edge.NeighborID)) continue;
    //         Visited.Add(Edge.NeighborID);
    //         CameFrom.Add(Edge.NeighborID, Current);
    //         if (Edge.NeighborID == GoalID)
    //             Result.Path = ReconstructPath(CameFrom, StartID, GoalID);
    //             Result.TotalCost = ComputePathCost(NavGraph, Result.Path);
    //             Result.bFound = true;
    //             return Result;
    //         Queue.Enqueue(Edge.NeighborID);
    //
    // return Result;  (no path found)

    UE_LOG(LogTemp, Warning, TEXT("BreadthFirstSearch not yet implemented (Role 4 - Oshan)"));
    return Result;
}

// ---------------------------------------------------------------------------
// UCS — Role 4 (Oshan)
// ---------------------------------------------------------------------------

FISPathResult UISSecondarySearch::UniformCostSearch(AISNavigationGraph* NavGraph,
                                                     int32 StartID, int32 GoalID)
{
    FISPathResult Result;

    if (!NavGraph) return Result;

    if (StartID == GoalID)
    {
        Result.Path.Add(StartID);
        Result.bFound = true;
        return Result;
    }

    // TODO (Oshan — implement UCS / Dijkstra):
    //
    // TArray<TPair<float,int32>> PQ;               // min-heap: (cost, nodeID)
    // TMap<int32, float> CostSoFar;
    // TMap<int32, int32> CameFrom;
    // TSet<int32> Explored;
    //
    // CostSoFar.Add(StartID, 0.f);
    // PQ.Add(TPair<float,int32>(0.f, StartID));
    //
    // while (!PQ.IsEmpty())
    //     PQ.Sort([](auto& A, auto& B){ return A.Key < B.Key; });
    //     auto [Cost, Current] = PQ[0]; PQ.RemoveAt(0);
    //
    //     if (Explored.Contains(Current)) continue;
    //     Explored.Add(Current);
    //     Result.NodesExplored++;
    //
    //     if (Current == GoalID)
    //         Result.Path = ReconstructPath(CameFrom, StartID, GoalID);
    //         Result.TotalCost = CostSoFar[GoalID];
    //         Result.bFound = true;
    //         return Result;
    //
    //     for (FISEdgePair& Edge : NavGraph->GetNeighbors(Current))
    //         float NewCost = Cost + Edge.Weight;
    //         if (!CostSoFar.Contains(Edge.NeighborID) || NewCost < CostSoFar[Edge.NeighborID])
    //             CostSoFar.Add(Edge.NeighborID, NewCost);
    //             CameFrom.Add(Edge.NeighborID, Current);
    //             PQ.Add(TPair<float,int32>(NewCost, Edge.NeighborID));
    //
    // return Result;

    UE_LOG(LogTemp, Warning, TEXT("UniformCostSearch not yet implemented (Role 4 - Oshan)"));
    return Result;
}
