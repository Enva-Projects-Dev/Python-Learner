; inno-setup-script für python learner - installiert pro user, kein admin nötig
#ifndef MyAppVersion
  #define MyAppVersion "0.0.1"
#endif
#define MyAppName "Python Learner"

[Setup]
AppId={{E4A9C2F1-7B3D-4E5A-9C1F-2D6B8A0E5F33}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Python Learner
DefaultDirName={localappdata}\Programs\Python Learner
DefaultGroupName=Python Learner
PrivilegesRequired=lowest
OutputDir={#SourcePath}\..\dist\installer
OutputBaseFilename=Installer
SetupIconFile={#SourcePath}\..\build\icon.ico
WizardStyle=modern
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\Python Learner.exe

[Files]
Source: "{#SourcePath}\..\dist\Python Learner\*"; \
    DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Python Learner"; Filename: "{app}\Python Learner.exe"
Name: "{autodesktop}\Python Learner"; Filename: "{app}\Python Learner.exe"; \
    Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; \
    GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\Python Learner.exe"; \
    Description: "Launch Python Learner"; Flags: nowait postinstall skipifsilent
