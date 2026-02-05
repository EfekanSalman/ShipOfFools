# ==================================================
# FILE 22: main.py
# ==================================================
from config import CONFIG
from core.ship import Ship


def main():
    """Main entry point"""
    print("=" * 70)
    print("🚢 SHIP OF FOOLS - ADVANCED SOCIAL SIMULATION")
    print("=" * 70)
    print("\nBased on Theodore Kaczynski's allegory")
    print("\nThe ship heads north into dangerous waters...")
    print("Will anyone listen to reason before it's too late?\n")

    # Initialize ship
    ship = Ship()
    ship.initialize()

    print("✓ Ship initialized")
    print(f"✓ {len(ship.characters)} characters created")
    print(f"✓ All systems operational\n")

    # Simulation loop
    try:
        while ship.simulation_active:
            if not ship.simulate_day():
                break

            # Detailed status every 5 days
            if ship.day % 5 == 0:
                ship.print_detailed_status()

            # Check if we've exceeded max days
            if ship.day > CONFIG.MAX_DAYS:
                print(f"\n⏰ Maximum simulation days reached")
                break

            # Pause for user input
            response = input("\n[Press ENTER to continue, 's' for status, 'q' to quit]: ").strip().lower()

            if response == 'q':
                print("\nSimulation ended by user.")
                break
            elif response == 's':
                ship.print_detailed_status()

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")

    # Final summary
    print("\n" + "=" * 70)
    print("📖 SIMULATION COMPLETE")
    print("=" * 70)

    print("\n🎯 KEY LESSONS FROM THIS SIMULATION:")
    print("  • Groups focused on immediate grievances while ignoring existential threats")
    print("  • Authority manipulated through small, meaningless concessions")
    print("  • Those warning about real danger were dismissed as extremists")
    print("  • Conflicting memories and narratives prevented unified action")
    print("  • Cultural norms shifted to accept previously unthinkable behaviors")
    print("  • The ship sank while everyone argued about distribution of resources")

    print("\n💭 REFLECTION:")
    print("  This simulation demonstrates how social psychology, power structures,")
    print("  and cognitive biases can lead groups toward collective disaster even")
    print("  when the solution is obvious to any rational observer.")

    print("\n📚 SYSTEMS DEMONSTRATED:")
    print("  ✓ Psychological (personality, trauma, PTSD, emotion, cognition)")
    print("  ✓ Social (alliances, networks, propaganda, culture)")
    print("  ✓ Power (hierarchy, manipulation, politics)")
    print("  ✓ Morality (Overton window, ethics, dilemmas)")
    print("  ✓ Narrative (story arcs, memory, foreshadowing)")
    print("  ✓ Environmental (resources, health, danger)")

    print("\n" + "=" * 70)
    print("Thank you for experiencing the Ship of Fools.")
    print("=" * 70)


if __name__ == "__main__":
    main()