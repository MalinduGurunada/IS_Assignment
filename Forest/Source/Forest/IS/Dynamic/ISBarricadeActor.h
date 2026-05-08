#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ISBarricadeActor.generated.h"

class UBoxComponent;
class UISGraphModifier;
class AISNavigationGraph;

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnBarricadeEvent, FVector, BarricadePosition);

/**
 * AISBarricadeActor — Role 2 (Malindu): Environment Event Source
 *
 * Place in the level. When activated by the player, it fires
 * OnBarricadePlaced / OnBarricadeRemoved events which sever or
 * restore graph edges via UISGraphModifier.
 */
UCLASS(BlueprintType, Blueprintable, Category="IS Navigation")
class FOREST_API AISBarricadeActor : public AActor
{
    GENERATED_BODY()

public:
    AISBarricadeActor();

    // Physical collision box representing the barricade obstacle
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="IS Dynamic")
    UBoxComponent* BarricadeBox;

    // The graph modifier component that handles edge severing
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="IS Dynamic")
    UISGraphModifier* GraphModifier;

    // True when this barricade is currently placed/active
    UPROPERTY(BlueprintReadOnly, Category="IS Dynamic")
    bool bIsPlaced = false;

    // Fired after the barricade is placed (triggers A* recalculation)
    UPROPERTY(BlueprintAssignable, Category="IS Dynamic")
    FOnBarricadeEvent OnBarricadePlaced;

    // Fired after the barricade is removed
    UPROPERTY(BlueprintAssignable, Category="IS Dynamic")
    FOnBarricadeEvent OnBarricadeRemoved;

protected:
    virtual void BeginPlay() override;

public:
    // -----------------------------------------------------------------------
    // Role 2 (Malindu) — implement these
    // -----------------------------------------------------------------------

    /** Called when the player activates/places this barricade. */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    void PlaceBarricade();

    /** Called when the player removes this barricade. */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    void RemoveBarricade();

    /** Toggle between placed and removed states. */
    UFUNCTION(BlueprintCallable, Category="IS Dynamic")
    void ToggleBarricade();
};
