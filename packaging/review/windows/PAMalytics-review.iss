#ifndef MyAppVersion
  #define MyAppVersion "1.0.1"
#endif

#ifndef MySourceDir
  #define MySourceDir "..\..\..\dist-review-windows\PAMalytics Review"
#endif

#ifndef MyOutputDir
  #define MyOutputDir "..\..\..\release-review-windows"
#endif

[Setup]
AppId={{64E6EB5F-9D76-4B20-B49F-865B916F96C7}
AppName=PAMalytics Review
AppVersion={#MyAppVersion}
AppPublisher=PAMalytics
DefaultDirName={autopf}\PAMalytics Review
DefaultGroupName=PAMalytics Review
DisableProgramGroupPage=yes
OutputDir={#MyOutputDir}
OutputBaseFilename=PAMalytics-review-v{#MyAppVersion}-windows-x64-setup
SetupIconFile=PAMalytics.ico
UninstallDisplayIcon={app}\PAMalytics Review.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
CloseApplications=yes
RestartApplications=no
VersionInfoVersion=1.0.1.0
VersionInfoCompany=PAMalytics
VersionInfoDescription=PAMalytics reviewer Windows installer
VersionInfoProductName=PAMalytics Review
VersionInfoProductVersion=1.0.1.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#MySourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PAMalytics Review"; Filename: "{app}\PAMalytics Review.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\PAMalytics Review"; Filename: "{app}\PAMalytics Review.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\PAMalytics Review.exe"; Description: "Launch PAMalytics Review"; Flags: nowait postinstall skipifsilent
