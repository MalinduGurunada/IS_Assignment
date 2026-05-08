#pragma once

#include "CoreMinimal.h"
#include "ISTypes.generated.h"

// ---------------------------------------------------------------------------
// FISGraphNode — represents one navigable point in the 3D world
// Role 1 (Hesara): used as the core data structure of the navigation graph
// ---------------------------------------------------------------------------
USTRUCT(BlueprintType)
struct FISGraphNode
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    int32 NodeID = -1;

    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    FVector WorldLocation = FVector::ZeroVector;

    // IDs of directly connected nodes (populated by AddEdge)
    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    TArray<int32> NeighborIDs;
};

// ---------------------------------------------------------------------------
// FISEdgePair — a neighbor node with its associated edge weight
// Returned by AISNavigationGraph::GetNeighbors()
// ---------------------------------------------------------------------------
USTRUCT(BlueprintType)
struct FISEdgePair
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    int32 NeighborID = -1;

    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    float Weight = 1.f;
};

// ---------------------------------------------------------------------------
// FISPathResult — output of any search algorithm (A*, BFS, UCS)
// Role 3 (Shazaan) and Role 4 (Oshan) both return this struct
// ---------------------------------------------------------------------------
USTRUCT(BlueprintType)
struct FISPathResult
{
    GENERATED_BODY()

    // Ordered node IDs from start to goal (empty if no path found)
    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    TArray<int32> Path;

    // Sum of edge weights along the path
    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    float TotalCost = 0.f;

    // Number of nodes popped from the frontier during search
    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    int32 NodesExplored = 0;

    // True if a valid path was found
    UPROPERTY(BlueprintReadWrite, Category="IS Navigation")
    bool bFound = false;
};
