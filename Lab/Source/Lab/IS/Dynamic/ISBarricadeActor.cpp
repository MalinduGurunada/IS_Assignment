#include "IS/Dynamic/ISBarricadeActor.h"
#include "IS/Dynamic/ISGraphModifier.h"
#include "IS/Graph/ISNavigationGraph.h"
#include "Components/BoxComponent.h"

AISBarricadeActor::AISBarricadeActor()
{
    PrimaryActorTick.bCanEverTick = false;

    BarricadeBox = CreateDefaultSubobject<UBoxComponent>(TEXT("BarricadeBox"));
    BarricadeBox->SetBoxExtent(FVector(50.f, 50.f, 100.f));
    RootComponent = BarricadeBox;

    GraphModifier = CreateDefaultSubobject<UISGraphModifier>(TEXT("GraphModifier"));
}

void AISBarricadeActor::BeginPlay()
{
    Super::BeginPlay();
}

// ---------------------------------------------------------------------------
// Role 2 (Malindu) — implementations
// ---------------------------------------------------------------------------

void AISBarricadeActor::PlaceBarricade()
{
    // TODO (Malindu):
    // 1. if (bIsPlaced) return  (already placed, no duplicate action)
    // 2. bIsPlaced = true
    // 3. Show the barricade mesh (SetActorHiddenInGame(false) or enable collision)
    // 4. GraphModifier->SeverEdgesAtPosition(GetActorLocation())
    // 5. if (GraphModifier->NavGraph)
    //        GraphModifier->NavGraph->TriggerRecalculation()
    // 6. OnBarricadePlaced.Broadcast(GetActorLocation())
    // 7. UE_LOG(LogTemp, Log, TEXT("Barricade placed at %s"), *GetActorLocation().ToString())

    UE_LOG(LogTemp, Warning, TEXT("PlaceBarricade not yet implemented (Role 2 - Malindu)"));
}

void AISBarricadeActor::RemoveBarricade()
{
    // TODO (Malindu):
    // 1. if (!bIsPlaced) return
    // 2. bIsPlaced = false
    // 3. Hide the barricade mesh / disable collision
    // 4. GraphModifier->RestoreEdgesAtPosition(GetActorLocation())
    // 5. if (GraphModifier->NavGraph)
    //        GraphModifier->NavGraph->TriggerRecalculation()
    // 6. OnBarricadeRemoved.Broadcast(GetActorLocation())

    UE_LOG(LogTemp, Warning, TEXT("RemoveBarricade not yet implemented (Role 2 - Malindu)"));
}

void AISBarricadeActor::ToggleBarricade()
{
    // TODO (Malindu): bIsPlaced ? RemoveBarricade() : PlaceBarricade()
}
