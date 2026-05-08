#include "IS/Search/ISAStarSearch.h"
#include "IS/Graph/ISNavigationGraph.h"

// ---------------------------------------------------------------------------
// Priority queue helpers (sorted TArray — ascending FScore)
// ---------------------------------------------------------------------------

void UISAStarSearch::PQPush(TArray<TPair<float, int32>>& PQ, int32 NodeID, float FScore)
{
    // TODO (Shazaan):
    // 1. Remove any existing entry for NodeID (use RemoveAll with lambda)
    // 2. Add TPair<float, int32>(FScore, NodeID)
    // 3. Sort ascending by Key: PQ.Sort([](auto& A, auto& B){ return A.Key < B.Key; })
}

TPair<float, int32> UISAStarSearch::PQPop(TArray<TPair<float, int32>>& PQ)
{
    // TODO (Shazaan): Remove and return the first element (lowest FScore)
    // TPair<float,int32> Top = PQ[0]; PQ.RemoveAt(0); return Top;
    return TPair<float, int32>(0.f, -1);
}

bool UISAStarSearch::PQContains(const TArray<TPair<float, int32>>& PQ, int32 NodeID)
{
    // TODO (Shazaan): return PQ.ContainsByPredicate([NodeID](auto& E){ return E.Value == NodeID; })
    return false;
}

void UISAStarSearch::PQUpdateScore(TArray<TPair<float, int32>>& PQ, int32 NodeID, float NewFScore)
{
    // TODO (Shazaan): find entry by NodeID and update Key, then re-sort
}

// ---------------------------------------------------------------------------
// Heuristic — Role 3 (Shazaan)
// ---------------------------------------------------------------------------

float UISAStarSearch::EuclideanHeuristic(FVector A, FVector B)
{
    // TODO (Shazaan): return FVector::Dist(A, B)
    // Admissibility proof: straight-line distance <= any path along graph edges.
    return 0.f;
}

// ---------------------------------------------------------------------------
// A* Search — Role 3 (Shazaan)
// ---------------------------------------------------------------------------

FISPathResult UISAStarSearch::Search(AISNavigationGraph* NavGraph, int32 StartID, int32 GoalID)
{
    FISPathResult Result;

    if (!NavGraph)
    {
        UE_LOG(LogTemp, Error, TEXT("ISAStarSearch::Search — NavGraph is null!"));
        return Result;
    }

    // Edge case: start == goal
    if (StartID == GoalID)
    {
        Result.Path.Add(StartID);
        Result.bFound = true;
        Result.TotalCost = 0.f;
        return Result;
    }

    // TODO (Shazaan — implement A*):
    //
    // Data structures:
    //   TArray<TPair<float,int32>> OpenSet;          // priority queue (f-score, node)
    //   TMap<int32, float> GScores;                  // best g-cost to each node
    //   TMap<int32, int32> CameFrom;                 // parent map for path reconstruction
    //   TSet<int32> ClosedSet;                       // fully-explored nodes
    //
    // Initialise:
    //   GScores.Add(StartID, 0.f);
    //   FVector GoalPos = NavGraph->Nodes[GoalID].WorldLocation;
    //   float H = EuclideanHeuristic(NavGraph->Nodes[StartID].WorldLocation, GoalPos);
    //   PQPush(OpenSet, StartID, H);
    //
    // Main loop:
    //   while (OpenSet is not empty)
    //       auto [FCurrent, CurrentID] = PQPop(OpenSet);
    //       Result.NodesExplored++;
    //
    //       if (CurrentID == GoalID)
    //           Result.Path = ReconstructPath(CameFrom, StartID, GoalID);
    //           Result.TotalCost = GScores[GoalID];
    //           Result.bFound = true;
    //           return Result;
    //
    //       ClosedSet.Add(CurrentID);
    //
    //       for (FISEdgePair& Edge : NavGraph->GetNeighbors(CurrentID))
    //           if (ClosedSet.Contains(Edge.NeighborID)) continue;
    //           float TentativeG = GScores[CurrentID] + Edge.Weight;
    //           if (!GScores.Contains(Edge.NeighborID) || TentativeG < GScores[Edge.NeighborID])
    //               GScores.Add(Edge.NeighborID, TentativeG);  // or FindOrAdd
    //               CameFrom.Add(Edge.NeighborID, CurrentID);
    //               float H2 = EuclideanHeuristic(NavGraph->Nodes[Edge.NeighborID].WorldLocation, GoalPos);
    //               PQPush(OpenSet, Edge.NeighborID, TentativeG + H2);
    //
    // return Result;  (bFound stays false if no path exists)

    UE_LOG(LogTemp, Warning, TEXT("ISAStarSearch::Search not yet implemented (Role 3 - Shazaan)"));
    return Result;
}

// ---------------------------------------------------------------------------
// Path reconstruction
// ---------------------------------------------------------------------------

TArray<int32> UISAStarSearch::ReconstructPath(const TMap<int32, int32>& CameFrom,
                                               int32 StartID, int32 GoalID)
{
    // TODO (Shazaan):
    // TArray<int32> Path;
    // int32 Current = GoalID;
    // while (Current != StartID)
    //     Path.Add(Current);
    //     Current = CameFrom[Current];
    // Path.Add(StartID);
    // Algo::Reverse(Path);
    // return Path;
    return TArray<int32>();
}
