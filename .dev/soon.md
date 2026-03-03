═══════════════════════════════════════════════════
  CODEY STATS LOGIC v2 — NO MERCY EDITION
═══════════════════════════════════════════════════

HUNGER (= Appetite for Success / Gier nach mehr)
───────────────────────────────────────────────────
  STEIGT wenn:
    + inaktivität (täglich decay)     → "will was erreichen"
    + neue stars von anderen          → "ich will MEHR!"
    + jemand forkt deine repo         → "die wollen mehr!"
    + neuer follower                  → "ich bin relevant!"

  SINKT wenn:
    - commits gemacht                 → drive gestillt
    - release veröffentlicht          → "hab geliefert"
    - energy = 0                      → kein Drive mehr möglich
    - zu viele commits (spam)         → übersättigt

  RANGE: 0-100
  DECAY: +15 pro Tag inaktiv (wird hungrig)
  CAP:   bei energy < 10 → hunger max 30


═══════════════════════════════════════════════════
HAPPINESS (= Wertschätzung / Anerkennung)
───────────────────────────────────────────────────
  STEIGT wenn:
    + andere forken DEINE repos       → "mein Werk lebt!"
    + stars von anderen auf deine repos
    + neue follower
    + issue von dir wurde gefixed/closed
    + streak milestone (7d, 30d, 100d)

  SINKT wenn:
    - DU forkst andere               → "ich konsumiere nur"
    - inaktivität (täglich -8)
    - viele open issues ohne fix     → "ich versage"
    - commit quality penalties       → "ich schreibe Müll"

  RANGE: 0-100
  DECAY: -8 pro Tag


═══════════════════════════════════════════════════
ENERGY (= Schaffenskraft / Tatkraft)
───────────────────────────────────────────────────
  STEIGT wenn:
    + issues gefixed (PR merged)     → "ich löse Probleme!"
    + neue follower                  → "ich werde gesehen!"
    + stars auf eigene repos         → "mein Werk wird genutzt!"
    + streak bonus (aktiver Tag)     → "ich bin im Flow!"
    + weekend warrior bonus

  SINKT wenn:
    - commits                        → -2.5 pro commit
    - release                        → -10 pro release
    - issues öffnen                  → -3 pro issue
    - inaktivität                    → +20 regen (ruht sich aus)

  RANGE: 0-100
  REGEN: +20 wenn keine aktivität (schläft/erholt sich)
  REGEN: +5  wenn aktiv (kleiner boost)


═══════════════════════════════════════════════════
HEALTH (= Gesamtzustand — nicht direkt beeinflussbar)
───────────────────────────────────────────────────
  = gewichteter Durchschnitt:

  health = (
      energy    * 0.35 +   ← wichtigste: ohne kraft nichts
      happiness * 0.35 +   ← anerkennung hält am leben
      hunger    * 0.30     ← motivation hält es am laufen
  )

  BONUS:  streak > 7d   → +5
  BONUS:  streak > 30d  → +10
  PENALTY: quality_score < 0.5 → -10
  PENALTY: social spam penalty → -15

  RANGE: 0-100


═══════════════════════════════════════════════════
MOOD (= Kombination aus allen Stats)
───────────────────────────────────────────────────
  'burnout'    → energy < 10 AND happiness < 10
  'struggling' → health < 25
  'exhausted'  → energy < 20 AND hunger > 70
                 "will aber kann nicht"
  'lazy'       → energy > 60 AND hunger < 20
                 "kann aber will nicht"
  'grinding'   → energy > 50 AND hunger > 60
                 "will und kann — im Tunnel"
  'inspired'   → happiness > 75 AND energy > 50
                 "frisch geforktes repo, neue follower"
  'elite'      → social_score > 1.2 AND health > 70
  'wise'       → tier = elder AND health > 70
  'happy'      → health > 80
  'neutral'    → alles andere


═══════════════════════════════════════════════════
SOCIAL SCORE (bleibt weitgehend gleich)
───────────────────────────────────────────────────
  following/follower ratio (FFR):
    FFR > 5.0  → spam_follower        × 0.25
    FFR > 2.0  → desperate_networker  × 0.75
    FFR < 0.5  → selective_networker  × 1.25  ← BONUS!

  fork ratio:
    own_forks > 2.0 → fork_leech      × 0.5

  star quality:
    stars/repo < 1.0 AND repos > 5 → code_spammer × 0.7


═══════════════════════════════════════════════════
QUALITY SCORE (bleibt weitgehend gleich)
───────────────────────────────────────────────────
  + has_license      → +0.3
  + has_description  → +0.2
  + issue close ratio > 0.7 → +0.2
  - is_fork          × 0.1
  - open_issues > 10 → -0.2
  commit messages:
    - 'fix','wip','typo' → -0.05 each
    - len < 10           → -0.1
  DEIN score 0.83 = sehr gut 


═══════════════════════════════════════════════════
PENALTY RENAME
───────────────────────────────────────────────────
  ALT: 'quality_curator'  (klingt wie Strafe)
  NEU: 'selective_networker' + BONUS statt Penalty
  
  Wer weniger folgt als ihm folgt = Qualitätsmerkmal!
  Nicht bestrafen — belohnen!
═══════════════════════════════════════════════════
