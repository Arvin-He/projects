; ���½ű��������� study.exe �ļ�
; ��װʱ������Ӧ�ó����������У���װ�������ʾ�����û��ر�Ӧ�ó���
; ��װ�ɹ�����Զ�����Ӧ�ó���
; �����µ� Modern UI �ĺ�ָ���﷨��ԭ�ȵĲ���ָ�����ֹ�Է�ֹ�ظ�
; �һᾡ��չʾ��λ���ָ����÷�����Ȼ��ָ��Ҳ����һЩ����ָ�����
; ���������������� NSIS �����ܱ���ɹ�.
; ���е�һЩ·�����ļ�����Ը�����Ҫ����

; �����ⲿѹ�����ߣ��������ǲ��ã�ԭ�򿴵� 10 ����
;!define HAVE_UPX
; ���������ⲿѹ�����ߣ�����п�ִ���ļ�ͷ��ѹ��
!ifdef HAVE_UPX
; �� UPX ѹ����ִ���ļ�ͷ������������ع���Ҳ�У�
!packhdr tmp.dat "E:UPX\upx --best tmp.dat"
!endif

; ����ѡ��

; ���ø��Ǳ��
SetOverwrite on
; ����ѹ��ѡ��
SetCompress auto
; ѡ��ѹ����ʽ
SetCompressor bzip2
; �������ݿ��Ż�
SetDatablockOptimize on
; ��������д��ʱ��
SetDateSave on

; �������Ԥ��

; ��������֣������${NAME}�����������
!define NAME "NSIS"
!define NAME_FULL "ȫ��λ���� NSIS ��ʹ��"
!verbose 3
; ����������Ϣ�����ļ�
;!include "${NSISDIR}\Examples\WinMessages.nsh"
; �����½���ĺ�ָ���ļ�
;!include "${NSISDIR}\Examples\Modern UI\ModernUI.nsh"
; ��������λͼ��ָ���ļ�
;!include "${NSISDIR}\Examples\branding.nsh"
!verbose 4
!define CURRENTPAGE $9
!define TEMP1 $R0
!define TEMP2 $R1

; ���밲װ����궨�壨�����ҽ����ˣ�����Ҳû���⡣��������ͨ���������Ҷ�������ˣ�
;!insertmacro MUI_INTERFACE "modern2.exe" "adni18-installer-C-no48xp.ico" "adni18-uninstall-C-no48xp.ico" "modern.bmp" "smooth"

; ��װ��������

; ����ļ�
OutFile "F:\study.exe"
; ��װ��������
Name /LANG=2052 "NSIS"
; �滻�Ի�����ʽ
ChangeUI all "${NSISDIR}\Contrib\UIs\modern.exe"
; ���� WindowsXP ���Ӿ���ʽ
XPstyle on
;��������
SetFont ���� 9
; ��������
Caption "ȫ��λ���� NSIS ��ʹ��"
; ���Ƶ�����
BrandingText /TRIMCENTER "Shao Hao"
; ��װ����ͼ��
Icon "favor.ico"
; ��װ������ʾ����
WindowIcon on
; ��ӱ���λͼ�����ڶ����� TOP ����������Ӹ߶ȣ�
AddBrandingImage LEFT 105
; �趨���䱳��
BGGradient off
; ���ð�����װģʽ
;SilentInstall normal
; ���ð���ж��ģʽ
;SilentUnInstall normal
; ִ�� CRC ��飨����� on �򿪡��ر�����Ϊ��Ҫ�޸İ�װ���򣬿��� 10 ����
CRCCheck off
; ������Ӧ�������ļ�
LoadLanguageFile "${NSISDIR}\Contrib\Language files\SimpChinese.nlf"
; �滻�����Ի�����������
SubCaption 0 "��ȨЭ��"
SubCaption 1 "��װѡ��"
SubCaption 2 "��װĿ¼"
SubCaption 3 "���ڰ�װ"
SubCaption 4 "��ɰ�װ"
; �滻Ĭ�ϰ�ť������
MiscButtonText "< ��һ��" "��һ�� >" "ȡ��" "�ر�"
; �滻����װ����ť������
;InstallButtonText "��װ"
; �滻���ļ��޷���д��ʱ�ľ��洰������
FileErrorText "�޷�д���ļ�$\r$\n$0$\r$\n��ȷ���ļ����Բ���ֻ����δ��ʹ���У�"

; Ĭ�ϵİ�װĿ¼
InstallDir "$PROGRAMFILES\QCD 3"
; ������ܵĻ���ע����м�ⰲװ·��
InstallDirRegKey HKLM \
"Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS" \
"UninstallString"

; ��ȨЭ��ҳ��
LicenseText "NSIS ������������װǰ�����Ķ�����Э������" "��ͬ��"
; ʹ����ȨЭ���ı�
LicenseData "F:\12\License.txt"
; ������ȨЭ��ҳ��ı���ɫ
;LicenseBkColor 000000

; ѡ��Ҫ����װ�����
ComponentText "���ڽ���װ ${NAME_FULL}�����ļ������" "��ѡ��װ����" "��ѡ����ϣ����װ�����"
InstType "��ȫ��װ(������)"
InstType "���Ͱ�װ"
InstType /CUSTOMSTRING=�Զ���?
;InstType /NOCUSTOM
;InstType /COMPONENTSONLYONCUSTOM
CheckBitmap "${NSISDIR}\Contrib\Icons\modern.bmp"
; �滻��ʾ���̿ռ���Ϣ������
SpaceTexts "����ռ䣺" "���ÿռ䣺"

; ��ʾ�û�����Ŀ¼���ı�
; DirShow hide
; �滻��ʾѡ��װĿ¼������
DirText "��ѡ�� ${NAME} �İ�װ·����" "ѡ��Ŀ¼���԰�װ ${NAME}��" "���..."
; �Ƿ�����װ�ڸ�Ŀ¼��
AllowRootDirInstall false

; ��װ��Ϣ����ɫ
;InstallColors 000000 FFFFFF
; ��װ��������ʾ��ʽ
InstProgressFlags smooth colored
; ��ɺ��Զ��رհ�װ����
AutoCloseWindow true
; ��ʾ����ʾ��ϸϸ�ڡ��Ի���
ShowInstDetails hide
; �滻����ʾϸ�ڡ���ť������
DetailsButtonText "��ʾϸ��"
; �滻����ɡ���ť������
CompletedText "�����"

; ж�س�������

; �滻ж�س��������
UninstallText "���ڽ������ϵͳ��ж�� ${NAME}��" "ж��Ŀ¼��"
; ж�س���ͼ��
UninstallIcon "F:\12\UnQCDIcon.ico"
; �滻ж�س�����������
UninstallCaption /LANG=2052 "ж�� ${NAME}"
; �滻ж�س���ÿҳ��ť������
UninstallSubCaption /LANG=2052 0 "��ȷ��"
UninstallSubCaption /LANG=2052 1 "������ɾ���ļ�"
UninstallSubCaption /LANG=2052 2 "�����"
; ж�س�����ʾ��ʽ
ShowUninstDetails hide
; �滻��ж�ء���ť������
UninstallButtonText /LANG=2052 "ж��"

; ��װ�������ݼ�����صĻص�����

; ��װ��������
Section /e "!��Ҫ����(���밲װ)" SecCore
SectionIn 1 2 RO
; �������·����ÿ��ʹ�ö���ı�
SetOutPath $INSTDIR
; ѭ������Ŀ¼��ȫ������
File /r "F:\12\1\*.*"
; ֻ����һ���ļ�
File "F:\12\gf.gif"
; ����̬���ӿ��ļ�
IfFileExists "$INSTDIR\1.dll" 0 NoFile1
; ȡ�����ע��
UnRegDll "$INSTDIR\1.dll"
Delete "$INSTDIR\1.dll"
NoFile1:
File "F:\12\1.dll"
; ע�����
RegDLL "$INSTDIR\QCDIconMgr.dll"
; д�����ע���ֵ
WriteRegStr HKLM "Software\NSIS\NSIS" "" "$INSTDIR"
; Ϊ Windows ж�س���д���ֵ
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS" "DisplayName" "NSIS��ֻ�����Ƴ���"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS" "UninstallString" '"$INSTDIR\uninst.exe"'
; д������ж�س��򣨿ɶ��ʹ�ã�
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section /e "��չ(��ѡ)" SecUpdate
SectionIn 1
SetOutPath "$INSTDIR\Plugins"
File "F:\12\qcdplus\Plugins\2.dll"
File /r "F:\12\qcdplus\Plugins\3"
SectionEnd

SubSection /e "ѡ��" SecOptions
Section /e "��������ͼ��" SecDesktopShortCut
SectionIn 1 2
SetOutPath "$INSTDIR\Plugins"
CreateShortCut "$DESKTOP\NSIS.lnk" "$INSTDIR\gf.gif"
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section /e "��������������ͼ��" SecQuickbarShortCut
SectionIn 1 2
SetOutPath "$INSTDIR\Plugins"
CreateShortCut "$QUICKLAUNCH\NSIS.lnk" "$INSTDIR\gf.gif"
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section /e "���� NSIS ������" SecShortCutGroup
SectionIn 1 2
SetOutPath "$INSTDIR\Plugins"
CreateDirectory "$SMPROGRAMS\NSIS"
CreateShortCut "$SMPROGRAMS\QCD Player\gf.lnk" "$INSTDIR\gf.gif"
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd
SubSectionEnd

Section "-Run"; ����?
ExecWait '"$INSTDIR\2.exe" -p'
WriteINIStr "$INSTDIR\NSIS.ini" "2" "Language" "Chinese"
Exec "$INSTDIR\2.exe"
ExecShell open "$INSTDIR\����˵��.htm"
SectionEnd

Section ""
;Invisible section to display the Finish header
!insertmacro MUI_FINISHHEADER SetHeader
SectionEnd

; ��װ�����ʼ������
Function .onInit
; �����г�����������ʱ��ʾ�˳����������
loop:
FindWindow $R0 "NSIS"
IntCmp $R0 0 done
MessageBox MB_OKCANCEL \
"NSIS �������С�$\n�����ȷ������ť��ر� NSIS Ȼ�������װ�������ȡ������ť���˳���װ����" \
IDOK NoAbort
Abort
NoAbort:
SendMessage $R0 1029 0 0
; �ԵȺ�������ֱ����ⲻ�����û�ѡ��ȡ��
Sleep 444
Goto loop
done:
; ��ʾ Logo ����
SetOutPath $TEMP
File /oname=qcd_logo.bmp "F:\12\logo.bmp"
File /oname=magiclime.exe "${NSISDIR}\Bin\magiclime.exe"
ExecWait '"$TEMP\magiclime.exe" qcd_logo.bmp'
Delete "$TEMP\magiclime.exe"
Delete "$TEMP\qcd_logo.bmp"
; ��ʼ������λͼ
!insertmacro BI_INIT $R0
FunctionEnd

; ��װ���������������ı�
Function SetHeader
!insertmacro MUI_HEADER_INIT
!insertmacro MUI_HEADER_START 1
!insertmacro MUI_HEADER_TEXT 2052 "��ȨЭ��" "��װ ${NAME} ֮ǰ���������Ķ�һ����Ȩ����."
!insertmacro MUI_HEADER_STOP 1
!insertmacro MUI_HEADER_START 2
!insertmacro MUI_HEADER_TEXT 2052 "ѡ�����" "��ѡ����Ҫ��װ�����."
!insertmacro MUI_HEADER_STOP 2
!insertmacro MUI_HEADER_START 3
!insertmacro MUI_HEADER_TEXT 2052 "ѡ��װλ��" "Ϊ ${NAME} ѡ��һ����װĿ¼."
!insertmacro MUI_HEADER_STOP 3
!insertmacro MUI_HEADER_START 4
!insertmacro MUI_HEADER_TEXT 2052 "��װ" "${NAME} �Ѿ���װ����ȴ�."
!insertmacro MUI_HEADER_STOP 4
!insertmacro MUI_HEADER_START 5
!insertmacro MUI_HEADER_TEXT 2052 "���" "��װ˳�����."
!insertmacro MUI_HEADER_STOP 5
!insertmacro MUI_HEADER_END
FunctionEnd

; ��ʼ����װ����Ի������ʾ�ı�
Function .onInitDialog
!insertmacro MUI_INNERDIALOG_INIT
!insertmacro MUI_INNERDIALOG_START 1
!insertmacro MUI_INNERDIALOG_TEXT 2052 1040 "�����ͬ��Э���е���������,ѡ����ͬ����������װ,�����ѡ���ˡ�ȡ����,��װ������ֹ,ֻ�н���������ܰ�װ ${NAME}."
!insertmacro MUI_INNERDIALOG_STOP 1
!insertmacro MUI_INNERDIALOG_START 2
!insertmacro MUI_INNERDIALOG_TEXT 2052 1042 "����"
!insertmacro MUI_INNERDIALOG_TEXT 2052 1043 "�ƶ������굽�����,����Լ�����ص�����."
!insertmacro MUI_INNERDIALOG_STOP 2
!insertmacro MUI_INNERDIALOG_START 3
!insertmacro MUI_INNERDIALOG_TEXT 2052 1041 "Ŀ���ļ���"
!insertmacro MUI_INNERDIALOG_STOP 3
!insertmacro MUI_INNERDIALOG_END
FunctionEnd

; ת����ҳ��ʱ�Ĵ���
Function .onNextPage
!insertmacro MUI_NEXTPAGE_OUTER
!insertmacro MUI_NEXTPAGE SetHeader
; ����λͼ����
!insertmacro BI_NEXT
FunctionEnd

; ת����һҳ��ʱ�Ĵ���
Function .onPrevPage
!insertmacro MUI_PREVPAGE
; ����λͼ����
!insertmacro BI_PREV
FunctionEnd

; ����Ƶ�ָ�����ʱ����ʾ����
Function .onMouseOverSection
; �ú�ָ�����ð�װ�Լ���ע���ı�
!insertmacro MUI_DESCRIPTION_INIT
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecCore} "��װ��Ӧ�ó���"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecUpdate} "��װ NSIS �ĸ��»��������"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecOptions} "ѡ�� NSIS ��������װѡ����磺������ݷ�ʽ��Ӧ�ó������"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecDesktopShortCut} "���û��������ϴ��� NSIS �Ŀ�ݷ�ʽ"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecQuickbarShortCut} "���û��Ŀ������ﴴ�� NSIS ��ݷ�ʽ"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecShortCutGroup} "���û��Ŀ�ʼ�˵��ĳ����д��� NSIS �Ŀ�ݷ�ʽ��"
!insertmacro MUI_DESCRIPTION_END
FunctionEnd

; ��װ�ɹ���ɺ������
Function .onInstSuccess
; �Լ��Ӱ�:)
FunctionEnd

; ������װʱ���洰�ڵ���ʾ��Ϣ
Function .onUserAbort
!insertmacro MUI_ABORTWARNING 2052 "��ȷ��Ҫ�Ƴ� ${NAME} �İ�װ��?"
!insertmacro MUI_ABORTWARNING_END
FunctionEnd

; ��װ�������λͼ�б�
!insertmacro BI_LIST
!insertmacro BI_LIST_ADD "F:\12\Brand1.bmp" /RESIZETOFIT
!insertmacro BI_LIST_ADD "F:\12\Brand2.bmp" /RESIZETOFIT
!insertmacro BI_LIST_ADD "F:\12\Brand3.bmp" /RESIZETOFIT
!insertmacro BI_LIST_END

; ж�س�������ػص�����

; ж�س�������
Section "Uninstall"
ExecWait '"$INSTDIR\12.exe" /un'
; ѭ��ɾ���ļ�ֱ��ɾ���ļ���
RMDir /r "$SMPROGRAMS\NSIS"
UnRegDLL "$INSTDIR\2.dll"
Delete "$INSTDIR\QCDIconMgr.dll"
Delete "$INSTDIR\*.*"
DeleteRegKey HKLM "Software\NSIS"
DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS"
MessageBox MB_YESNO|MB_ICONQUESTION \
"�Ƿ������Ŀ¼ҲҪɾ����$\n(����Ҫ������Щ�ļ�����������ġ��񡱰�ť)" \
IDNO NoDelete
; ȫɾ�⣡����
RMDir /r "$INSTDIR"
NoDelete:
SectionEnd

; ����ж�س������λͼ
!define BI_UNINSTALL
!include "${NSISDIR}\Examples\branding.nsh"

; ��ʼ��ж�س���Ի��������
Function un.onInit
; ��ʼ������λͼ
!insertmacro BI_INIT $R0
FunctionEnd

; ж�س��������������ı�
Function un.SetHeader
!insertmacro MUI_HEADER_INIT
!insertmacro MUI_HEADER_START 1
!insertmacro MUI_HEADER_TEXT 2052 "ж�� ${NAME}" "${NAME_FULL} �������ϵͳ���Ƴ�."
!insertmacro MUI_HEADER_STOP 1
!insertmacro MUI_HEADER_START 2
!insertmacro MUI_HEADER_TEXT 2052 "ж��" "${NAME} ���ڱ�ж�أ���ȴ�."
!insertmacro MUI_HEADER_STOP 2
!insertmacro MUI_HEADER_START 3
!insertmacro MUI_HEADER_TEXT 2052 "���" "${NAME_FULL} �Ѵ����ϵͳ���Ƴ�."
!insertmacro MUI_HEADER_STOP 3
!insertmacro MUI_HEADER_END
FunctionEnd

; ��ʼ��ж�س���Ի���ʱ�Ĵ���
Function un.onInitDialog
; �Լ���:)
FunctionEnd

; ж�س���ת����һҳʱ�Ĵ���
Function un.onNextPage
!insertmacro MUI_NEXTPAGE_OUTER
!insertmacro MUI_NEXTPAGE un.SetHeader
; ����λͼ����
!insertmacro BI_NEXT
FunctionEnd

; ж�س������ʱ�Ĵ���
Function un.onUninstSuccess
; �ټ�^_^
FunctionEnd

; ����ж�س���ʱ�Ĵ���
Function un.onUserAbort
FunctionEnd

; ж�س������λͼ�б�
!insertmacro BI_LIST
!insertmacro BI_LIST_ADD "F:\12\UnBrand1.bmp" /RESIZETOFIT
!insertmacro BI_LIST_ADD "F:\12\UnBrand2.bmp" /RESIZETOFIT
!insertmacro BI_LIST_END

; ����