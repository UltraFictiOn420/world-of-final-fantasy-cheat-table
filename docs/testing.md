# Validation record — 2026-10-10

23 structural/model tests pass on v19. They check XML/IDs, hook restoration and scope, information-row protections, replacement queue/native grant boundaries, save-toggle address resolution, party-status scope/member propagation, accuracy bytecode boundaries, and enemy topple one-shot dispatch. Four installed-catalogue checks also pass. This is not equivalent to testing every game situation.

User gameplay confirmations: Gil/SP/XP, God Mode/AP, damage and max vitals, zero ability AP cost, both item modes, easy Mu/Chocochick/Behemoth capture, Mu-to-Chocochick and Mu-to-Goblin owned replacement, field saving and reloading, Always Critical, and F8 topple of Mini Golem/Copper Gnome.

v18 status evidence: after Defend, both party stacks and all observed members acquired Haste/Regen/Protect/Shell flags; enemy flags remained unchanged. Native Protect/Shell counters and propagation guards were repaired. Across-battle effects and negative-status protection still need player testing. Native capture hooks and status hooks passed compilation, enable/disable and exact-byte restoration checks.

v19 topple evidence: compile/enable/disable/native-byte-restoration/re-enable passed; F8 queues a one-shot request and unused requests expire. User confirmed separation after F8 then Defend just before the enemy turn. This does not independently confirm HP preservation or every enemy stack.

Save toggle was additionally compiled and exercised off/on/off successfully after the v12 disable-resolution repair. The inactive developer owned-Mirage trace was removed from the live session and is absent from the current artifact.

Remaining tests: champions/cost-zero implementation, broader enemy-stack/topple and party balance protection, buff behavior across battles, Never Miss, broader loot rolls and future quantity work, broader replacement catalogue and multi-capture, replacement board/ability/save persistence, other save-menu map/story states and non-use inventory removal. These are not marked completed.

v13 changed presentation/provenance and packaging only. v14-v19 add battle features and repairs. Archives include known failed versions for recovery/history, not use; use v19 rather than earlier buff/capture implementations.
