[Setup]
AppName=Royal Screenshot
AppVersion=1.0
DefaultDirName={pf}\Royal Screenshot
DefaultGroupName=Royal Screenshot
OutputDir=.
OutputBaseFilename=Royal_Screenshot_Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile=license.txt

[Files]
Source: "C:\Users\EmonIbnMustafa\Documents\Win ss project\dist\royal_screenshot.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\Royal Screenshot"; Filename: "{app}\royal_screenshot.exe"; WorkingDir: "{app}"
Name: "{group}\Royal Screenshot"; Filename: "{app}\royal_screenshot.exe"

[Run]
Filename: "{app}\royal_screenshot.exe"; Description: "Launch Royal Screenshot"; Flags: nowait postinstall skipifsilent
