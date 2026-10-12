# Changelog

## 0.0.3

- "What's new"-Popup nach einem Update, einmal pro Version, mit
  Reset-Button inkl. Backup.
- Task-instructions gefixt, wo das Beispiel nicht zum Test gepasst hat
  (Würfel zeigt jetzt den echten seeded Output, die 1x1-Tabelle die
  echten Spaltenbreiten).
- Kapitel-Locks: nächstes Kapitel geht erst auf, wenn 90% vom
  vorherigen fertig sind, in Sidebar, Dashboard und Server-Antworten.
- Show solution: Code wird nicht mehr abgeschnitten, dazu Copy und
  "Load into editor".
- UI aufgeräumt: dünne Scrollbars überall (Sidebar scrollt jetzt auch
  mit der custom), Sidebar mit einzeiligen Items und Progress-Balken,
  klarere Buttons, ruhigere Empty States.
- Leichterer Einstieg in Kapitel 1-5: Starter-Code hat jetzt ein Gerüst
  statt nur `# TODO`, die schwerste Zeile ist schon geschrieben, die
  TODOs sagen was fehlt.
- Neue "Similar solved example"-Card: kurzes fertiges Programm mit
  gleicher Technik und anderen Zahlen, angucken kostet keine XP. Auf
  allen Tasks in Kapitel 1-5 und allen späteren Bossen.
- 7 neue Warm-ups in Kapitel 1-5 (input+int, `:.2f`, while, `break`,
  Comprehensions, `split`, `return`), damit der Sprung zur Schul-Task
  kleiner wird. Jetzt 170 Tasks.
- Lessons in Kapitel 1-5 erweitert: alles was die Tasks brauchen wird
  vorher auch erklärt (`input()`/`int()`/`float()`, f-string
  Format-Specs, `//` vs `%`, `+=`, `random`, Listen-Builtins,
  Datei lesen, `split`/`join`, `ord`/`chr`, erster Blick auf Funktionen).
- macOS: Build-Kit für eine echte .app/.dmg (Apple Silicon).

## 0.0.2

- Fehlermeldungen in einfachem Englisch ("What went wrong"), im
  Output-Panel und pro Test.
- Klarere Test-Labels: Program-Tests zeigen ihr Input
  ("output for input: 3700, 25").
- Leeres Fenster und 404 im installierten Build gefixt.
- macOS: Build-Kit für eine echte .app/.dmg (Apple Silicon).

## 0.0.1 - erster Release

- 20 Kapitel mit dem ganzen Lehrplan: 163 Tasks, 79 Quizzes, 29 Lessons.
- XP, Level, Ränge, Streaks, Achievements und Boss-Missionen (x1,5 XP).
- Dark-first Theme mit Light Mode; Bebas Neue als Display-Font.
- Code läuft lokal abgekapselt mit automatischen Tests; jede Lesson
  hat ausführbare Beispiele.
- Fortschritt wird lokal gespeichert; Windows Installer + portable Build.
