#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "IS/ISTypes.h"
#include "ISSecondarySearch.generated.h"

class AISNavigationGraph;

/**
 * UISSecondarySearch — Role 4 (Oshan): Secondary Search Algorithms
 *
 * Implements BFS (fewest hops) and UCS (minimum cost) as static Blueprint
 * functions. Results can be compared against A* to verify optimality.
 *
 * BFS  time complexity: O(V + E)
 * UCS  time complexity: O((V + E) log V)
 */
UCLASS(Category="IS Navigation")
class LAB_API UISSecondarySearch : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    // -----------------------------------------------------------------------
    // Role 4 (Oshan) — implement these
    // -----------------------------------------------------------------------

    /**
     * Breadth-First Search — finds the path with the fewest edges (hops).
     * Uses a FIFO queue. Does NOT minimise total edge weight.
     */
    UFUNCTION(BlueprintCallable, Category="IS Search|BFS")
    static FISPathResult BreadthFirstSearch(AISNavigationGraph* NavGraph,
                                             int32 StartID, int32 GoalID);

    /**
     * Uniform-Cost Search (Dijkstra) — finds the minimum-cost path.
     * Uses a min-heap (sorted array). Equivalent to A* with h(n) = 0.
     */
    UFUNCTION(BlueprintCallable, Category="IS Search|UCS")
    static FISPathResult UniformCostSearch(AISNavigationGraph* NavGraph,
                                            int32 StartID, int32 GoalID);

private:
    static TArray<int32> ReconstructPath(const TMap<int32, int32>& CameFrom,
                                          int32 StartID, int32 GoalID);

    static float ComputePathCost(AISNavigationGraph* NavGraph, const TArray<int32>& Path);
};
