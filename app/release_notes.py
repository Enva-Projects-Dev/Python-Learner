"""Release-Notizen fürs "What's new"-Popup nach einem Update.

Key = VERSION-String. Pro Release einen Eintrag dazu, alte bleiben drin.
"""

NOTES = {
    "0.0.3": {
        "title": "Moin Leute, paar Änderungen an der App.",
        "intro": "Version 0.0.3, kurz was sich getan hat:",
        "changes": [
            "Aufgaben gefixt, bei denen das Beispiel nicht zum Test gepasst hat (Mini-Poster-Boss, Würfel, 1x1 u.a.).",
            "\"Show solution\": Code wird nicht mehr abgeschnitten, dazu gibts jetzt Copy und \"Load into editor\".",
            "Kapitel 1-5 sind leichter zum Einstieg: die Lessons erklären jetzt alles, was die Aufgaben wirklich brauchen, und der Starter-Code hat ein Gerüst statt nur # TODO.",
            "UI aufgeräumt: Scrollbars, Sidebar, Buttons, Ergebnis-Anzeige.",
        ],
        "new": [
            "Kapitel-Locks: das nächste Kapitel geht erst auf, wenn 90% vom vorherigen fertig sind.",
            "\"Similar solved example\" bei jeder Aufgabe, gleiches Prinzip, andere Zahlen, kostet keine XP.",
            "7 neue Warm-up-Aufgaben (jetzt 170 Tasks).",
            "Mac: Build-Kit für eine echte .app / .dmg.",
        ],
        "outro": "Euer Progress bleibt, könnt aber auch restarten um die ✨ Experience ✨ nochmal von vorn zu erleben.",
    },
}
