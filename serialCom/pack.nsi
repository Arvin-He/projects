!define PRODUCT_NAME "valueReader"
!define PRODUCT_VERSION "1.0.0.0"
!define PRODUCT_PUBLISHER "Arvin"
!define PRODUCT_FULL_NAME "${PRODUCT_NAME} ${PRODUCT_VERSION}"
!define OUT_DIR "."
!define OUT_FILE_NAME "${PRODUCT_NAME}.exe"

RequestExecutionLevel user

!define UNINST_KEY "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

!define SHORTCUT_NAME "${PRODUCT_NAME}"

!define PRODUCT_UNINST_KEY  "${UNINST_KEY}\${PRODUCT_NAME}"

#!system '"StampVer" -o4 -k -nopad -f"${PRODUCT_VERSION}" -p"${PRODUCT_VERSION}" "${MAKE_DIR}\MicroBit-${PRODUCT_NAME}.exe"'

; MUI ????
!define MUI_WELCOMEPAGE_TITLE "??${PRODUCT_NAME} ${PRODUCT_VERSION}?????"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\orange.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\orange-uninstall.bmp"

!include MUI2.nsh
!include FileFunc.nsh

Name "${PRODUCT_NAME}"
BrandingText "http://www.microbit.com/"
; ??????
OutFile "${OUT_DIR}\${OUT_FILE_NAME}"
; ?????
InstallDir "C:\${PRODUCT_NAME}"

Page custom nsDialogsPage nsDialogsPageLeave
; ??????
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
; §Ø?????
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
; ???????
!insertmacro MUI_LANGUAGE SimpChinese

Section "Installer Section"    
	Delete "$DESKTOP\${PRODUCT_NAME}*.lnk"
	Delete "$SMSTARTUP\${PRODUCT_NAME}*.lnk"
	RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
	
	SetOutPath $INSTDIR

	File /r /x "*.nsi" /x "*.bat" /x "*.pyc" ".\dist\*"
	File /r "log"
	File /r "platforms"
	File "config.ini"

	WriteUninstaller "uninstall.exe"

	CreateShortCut "$SMSTARTUP\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe"
	
	CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
	CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_VERSION}"
	CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_VERSION}\§Ø?? ${PRODUCT_NAME}.lnk" "$INSTDIR\Uninstall.exe" "$INSTDIR\favor.ico"
	
	CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe" "$INSTDIR\favor.ico"
	
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${PRODUCT_NAME}.exe"
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "Arvin"

SectionEnd

Section "un.Uninstaller Section"
	Delete "$DESKTOP\${PRODUCT_NAME}*.lnk"
	Delete "$DESKTOP\${SHORTCUT_NAME}*.lnk"
	Delete "$SMSTARTUP\${PRODUCT_NAME}*.lnk"
	RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
	
	RMDir /r "$INSTDIR"

	DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
SectionEnd


VIProductVersion "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "CompanyName"      "??????????"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileDescription"  "${PRODUCT_NAME} ???????"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileVersion"      "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "InternalName"     "${OUT_FILE_NAME}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "LegalCopyright"   "Copyright (C) 2017 ??????????"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "OriginalFilename" "${OUT_FILE_NAME}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "ProductName"      "${PRODUCT_NAME}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "ProductVersion"   "${PRODUCT_VERSION}"

Var UninstallFileName

Function .onInit
	Call CreateMutex
	ReadRegStr $UninstallFileName HKLM "${PRODUCT_UNINST_KEY}" "UninstallString"
FunctionEnd

Function CreateMutex
	Retry:
	System::Call "kernel32::CreateMutexW(i 0, i 0, w 'MicroBitauto.com/valReader/1.0' ) i .R1 ?e"
	Pop $R0
	System::Call "kernel32::CloseHandle(i R1) i.s"
	${If} $R0 != 0
		MessageBox MB_RetryCancel|MB_ICONEXCLAMATION "${PRODUCT_NAME} ????????" IdRetry Retry
		Quit
	${EndIf}
FunctionEnd

Var RADIO_REPAIR
Var RADIO_REMOVE
Var Checkbox_State_REPAIR
Var Checkbox_State_REMOVE
Var Checkbox_State

Function nsDialogsPage
	${if} $UninstallFileName == ""
		Abort
	${EndIf}
	
	!insertmacro MUI_HEADER_TEXT "${PRODUCT_NAME} ?????" "???¡ã????§Ø??${PRODUCT_NAME}"
	nsDialogs::Create /NOUNLOAD 1018
	${NSD_CreateLabel} 0u 0u 300u 30u "??????????§Ö?????????? [?????(N)] ????"

	${NSD_CreateRadioButton} 30u 30u 120u 30u "???¡ã??"
	Pop $RADIO_REPAIR
		${If} $Checkbox_State_REPAIR == ${BST_CHECKED}
			${NSD_Check} $RADIO_REPAIR
			${NSD_GetState} $RADIO_REPAIR $Checkbox_State
		${EndIf}

	${NSD_CreateRadioButton} 30u 60u 120u 30u "§Ø??"
	Pop $RADIO_REMOVE
		${If} $Checkbox_State_REMOVE == ${BST_CHECKED}
			${NSD_Check} $RADIO_REMOVE
			${NSD_GetState} $RADIO_REMOVE $Checkbox_State
		${EndIf}
		${If} $Checkbox_State <> ${BST_CHECKED}
			${NSD_Check} $RADIO_REPAIR
		${EndIf}

	nsDialogs::Show
FunctionEnd

Function nsDialogsPageLeave
	${NSD_GetState} $RADIO_REPAIR $Checkbox_State_REPAIR
	${NSD_GetState} $RADIO_REMOVE $Checkbox_State_REMOVE
	${If} $Checkbox_State_REMOVE == ${BST_CHECKED}
		Exec $UninstallFileName
		Quit
	${EndIf}
FunctionEnd