#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "IS/ISTypes.h"
#include "ISAStarSearch.generated.h"

class AISNavigationGraph;

/**
 * UISAStarSearch — Role 3 (Shazaan): A* Search & Heuristic Design
 *
 * A Blueprint Function Library — all functions are static and can be called
 * from any Blueprint without needing an object reference.
 *
 * Algorithm complexity: O((V + E) log V) with the sorted-array priority queue.
 */
UCLASS(Category="IS Navigation")
class LAB_API UISAStarSearch : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    // -----------------------------------------------------------------------
    // Role 3 (Shazaan) — implement these
    // -----------------------------------------------------------------------

    /**
     * Run A* from StartID to GoalID on the given navigation graph.
     *
     * Algorithm outline:
     *   f(n) = g(n) + h(n)
     *   g(n) = cost from start to n (along best known path)
     *   h(n) = EuclideanHeuristic(n, goal)   <- admissible, never overestimates
     *
     * @return FISPathResult with optimal Path, TotalCost, NodesExplored, bFound
     */
    UFUNCTION(BlueprintCallable, Category="IS Search|A*")
    static FISPathResult Search(AISNavigationGraph* NavGraph, int32 StartID, int32 GoalID);

    /**
     * Euclidean (straight-line) distance heuristic.
     * Admissible: h(n) <= h*(n) for any graph where edge weights = 3D distances.
     * Consistent: h(n) <= cost(n,n') + h(n') by triangle inequality.
     */
    UFUNCTION(BlueprintPure, Category="IS Search|A*")
    static float EuclideanHeuristic(FVector A, FVector B);

    /**
     * Reconstruct the path by tracing CameFrom back from GoalID to StartID.
     * Returns the path in forward order (Start -> ... -> Goal).
     */
    UFUNCTION(BlueprintCallable, Category="IS Search|A*")
    static TArray<int32> ReconstructPath(const TMap<int32, int32>& CameFrom,
                                          int32 StartID, int32 GoalID);

private:
    // Internal sorted-array priority queue helpers
    // Entry format: TPair<float, int32> where Key=FScore, Value=NodeID

    static void PQPush(TArray<TPair<float, int32>>& PQ, int32 NodeID, float FScore);
    static TPair<float, int32> PQPop(TArray<TPair<float, int32>>& PQ);
    static bool PQContains(const TArray<TPair<float, int32>>& PQ, int32 NodeID);
    static void PQUpdateScore(TArray<TPair<float, int32>>& PQ, int32 NodeID, float NewFScore);
};
