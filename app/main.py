"""Desktop-einstieg: pywebview-fenster, das die ui hostet."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import webview

from app.api import Api

if getattr(sys, "frozen", False):
    # pyinstaller: datas landen in <sys._MEIPASS>/app/ui
    UI = os.path.join(sys._MEIPASS, "app", "ui", "index.html")
else:
    UI = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "ui", "index.html")


def main():
    api = Api()
    window = webview.create_window(
        "Python Learner",
        url=UI,
        js_api=api,
        width=1380, height=860,
        min_size=(1024, 680),
    )
    webview.start()


if __name__ == "__main__":
    main()
