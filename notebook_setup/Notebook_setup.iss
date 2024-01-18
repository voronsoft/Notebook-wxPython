; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Notebook"
#define MyAppVersion "1.0"
#define MyAppPublisher "Norov"
#define MyAppURL "https://github.com/voronsoft/Notebook-wxPython"
#define MyAppExeName "Notebook.exe"
#define MyAppExeNameDel "Uninstall"
; C������ ������� ���������� ���� � �������� ����� (� ��� ����� ����� �������� ���������������� ���� (setup)
; !!! ��� ������ ��������� ) �������� ���� �� ��� � ������� ������ ��������� ���� ���� ��������
#define MyFolder "C:\Notebook-wxPython\notebook_setup"

[Setup]
AppId={{39F7701A-E911-42DD-988A-1285F1592112}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
;
UsedUserAreasWarning=no
; �������� ����� ��������� � ����
DefaultGroupName=Notebook
; ���� ���� ����� ������� ���������� � ��� ����������� ����� ������
OutputDir={#MyFolder}
; ���� � ����� Readme.txt
InfoBeforeFile=Readme.txt
; �������� ����� � ���� ����
DisableProgramGroupPage=yes
; �������� �����������
OutputBaseFilename=Notebook-setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
;���� � ������ ��� ����� setup.exe
SetupIconFile="{#MyFolder}\Source\icons\notebook.ico"
; ������������� ������ ��� ����������� � ������ ������������� �������� � ������ ���������� ��� �������� ����������.
UninstallDisplayIcon={app}\icons\uninstall_notebook.ico
; ���� ��� ��������� ����������
DefaultDirName={autopf}\{#MyAppName} {#MyAppVersion}

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
; ��� ��������� ������� ����� ������ �������� ����� �� ������� ���� ��� ���
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Dirs]
; �������������� ����������, ������� ������ ���� ������� �� ����� ��������� ���������
Name: "{app}\db"
Name: "{app}\img"
Name: "{app}\icons"
; �������������� ����������, ������� ������ ���� ������� �� ����� ��������� ���������
; ������� ����� AppData - {localappdata} 
Name: "{localappdata}\Notebook"
Name: "{localappdata}\Notebook\Logs"
; ������� ����� Documents - {userdocs}
Name: "{userdocs}\Notebook-export-json"

[UninstallDelete]
; ������� ��� ����� � ���������� ��� ������������� ���������

Type: filesandordirs; Name: "{app}\db"
Type: filesandordirs; Name: "{app}\img"
Type: filesandordirs; Name: "{app}\icons"
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{localappdata}\Notebook"
Type: filesandordirs; Name: "{userdocs}\Notebook-export-json"
Type: filesandordirs; Name: "{userdocs}\Notebook-pdf"

[Files]
; ��� ��� � ���� ����������� � ����� ����������� ����� ����������� � ����� � ��������������� �����������
Source: "{#MyFolder}\Source\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyFolder}\Source\db\*"; DestDir: "{app}\db"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#MyFolder}\Source\img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#MyFolder}\Source\icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
; ������� ����� ��� �������
Source: "{#MyFolder}\Source\Logs\debug.log"; DestDir: "{localappdata}\Notebook\Logs"; Flags: ignoreversion
Source: "{#MyFolder}\Source\Logs\warning.log"; DestDir: "{localappdata}\Notebook\Logs"; Flags: ignoreversion
Source: "{#MyFolder}\Source\Logs\error.log"; DestDir: "{localappdata}\Notebook\Logs"; Flags: ignoreversion


[Icons]
; ������ �� ��������� URL
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
; ������� ����� ������� ��������� � ����� ����
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icons\notebook.ico"
; ������� ����� �������� ��������� � ���� "����" � ����� "Notebook"
Name: "{group}\{#MyAppExeNameDel}"; Filename: "{app}\unins000.exe"; IconFilename: "{app}\icons\uninstall_notebook.ico"
; ��� ������ �������� �� ������� ���� ���������� ��� ������ ���� (Tasks: desktopicon)
Name: "{commondesktop}\{#MyAppExeName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icons\notebook.ico"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\Notebook"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
