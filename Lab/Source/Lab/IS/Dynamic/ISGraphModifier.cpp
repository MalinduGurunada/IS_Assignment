#include "IS/Dynamic/ISGraphModifier.h"
#include "IS/Graph/ISNavigationGraph.h"
#include "Kismet/GameplayStatics.h"

UISGraphModifier::UISGraphModifier()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UISGraphModifier::BeginPlay()
{
    Super::BeginPlay();

    // Auto-find the navigation graph in the level
    TArray<AActor*> Found;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AISNavigationGraph::StaticClass(), Found);
    if (Found.Num() > 0)
    {
        NavGraph = Cast<AISNavigationGraph>(Found[0]);
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("ISGraphModifier: No AISNavigationGraph found in level!"));
    }
}

FString UISGraphModifier::MakeEdgeKey(int32 FromID, int32 ToID)
{
    return FString::Printf(TEXT("%d_%d"), FromID, ToID);
}

void UISGraphModifier::ParseEdgeKey(const FString& Key, int32& OutFromID, int32& OutToID)
{
    TArray<FString> Parts;
    Key.ParseIntoArray(Parts, TEXT("_"));
    OutFromID = Parts.Num() > 0 ? FCString::Atoi(*Parts[0]) : -1;
    OutToID   = Parts.Num() > 1 ? FCString::Atoi(*Parts[1]) : -1;
}

// ---------------------------------------------------------------------------
// Role 2 (Malindu) — implementations
// ---------------------------------------------------------------------------

TArray<FString> UISGraphModifier::SeverEdgesAtPosition(FVector Position, float Radius)
{
    // TODO (Malindu):
    // 1. Use Radius > 0 ? Radius : ObstacleRadius
    // 2. Iterate all keys in NavGraph->EdgeWeights
    // 3. For each key, parse FromID and ToID
    // 4. Compute midpoint = (NavGraph->Nodes[FromID].WorldLocation + NavGraph->Nodes[ToID].WorldLocation) / 2
    // 5. If FVector::Dist(midpoint, Position) <= EffectiveRadius: SeverEdge(FromID, ToID), add key to result
    // 6. Return the list of severed keys

    UE_LOG(LogTemp, Warning, TEXT("SeverEdgesAtPosition not yet implemented (Role 2 - Malindu)"));
    return TArray<FString>();
}

bool UISGraphModifier::SeverEdge(int32 FromID, int32 ToID)
{
    // TODO (Malindu):
    // 1. if (!NavGraph || !NavGraph->HasEdge(FromID, ToID)) return false
    // 2. float Weight = NavGraph->GetEdgeWeight(FromID, ToID)
    // 3. SeveredEdges.Add(MakeEdgeKey(FromID, ToID), Weight)
    //    SeveredEdges.Add(MakeEdgeKey(ToID, FromID), Weight)   // store reverse too
    // 4. NavGraph->RemoveEdge(FromID, ToID, true)
    // 5. return true
    return false;
}

bool UISGraphModifier::RestoreEdge(int32 FromID, int32 ToID)
{
    // TODO (Malindu):
    // 1. FString Key = MakeEdgeKey(FromID, ToID)
    //    if (!SeveredEdges.Contains(Key)) return false
    // 2. float OriginalWeight = SeveredEdges[Key]
    // 3. NavGraph->AddEdge(FromID, ToID, OriginalWeight, true)
    // 4. SeveredEdges.Remove(MakeEdgeKey(FromID, ToID))
    //    SeveredEdges.Remove(MakeEdgeKey(ToID, FromID))
    // 5. return true
    return false;
}

TArray<FString> UISGraphModifier::RestoreEdgesAtPosition(FVector Position, float Radius)
{
    // TODO (Malindu): mirror SeverEdgesAtPosition but call RestoreEdge
    UE_LOG(LogTemp, Warning, TEXT("RestoreEdgesAtPosition not yet implemented (Role 2 - Malindu)"));
    return TArray<FString>();
}

TArray<FString> UISGraphModifier::GetSeveredEdges() const
{
    TArray<FString> Keys;
    SeveredEdges.GetKeys(Keys);
    return Keys;
}

bool UISGraphModifier::IsEdgeSevered(int32 FromID, int32 ToID) const
{
    return SeveredEdges.Contains(MakeEdgeKey(FromID, ToID));
}
