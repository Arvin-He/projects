
!define OUT_DIR "."
!define CONFIG_DIR "."

!ifndef MAKE_DIR
	!error "MAKE_DIR 没有定义"
!endif

!ifndef OUT_DIR
	!error "OUT_DIR 没有定义"
!endif

!ifndef DEVELOP_VERSION
	!error "DEVELOP_VERSION 没有定义"
!endif

!ifndef SUPPORT_VERSION
	!error "SUPPORT_VERSION 没有定义"
!endif

!ifndef USER_ID
	!error "USER_ID 没有定义"
!endif

!ifndef PRODUCT_VERSION
	;!error "PRODUCT_VERSION 没有定义"
	!define PRODUCT_VERSION "${DEVELOP_VERSION}.${SUPPORT_VERSION}${USER_ID}"
!endif

!ifndef PRODUCT_NAME
	!error "PRODUCT_NAME 没有定义"
!endif

!ifdef _SIMU
!define SIMU_STR "_SIMU"
!else
!define SIMU_STR ""
!endif

!ifdef _DEBUG
!define DEBUG_STR "_DEBUG"
!else
!define DEBUG_STR ""
!endif

!ifdef _TEST
!define TEST_STR "(测试版)"
!define TEST__STR " (测试版)"
!else
!define TEST_STR ""
!define TEST__STR ""
!endif

!ifndef OUT_FILE_NAME
	;!error "OUT_FILE_NAME 没有定义"
	!define OUT_FILE_NAME "GFD-${PRODUCT_NAME}_${PRODUCT_VERSION}${TEST_STR}.exe"
!endif

RequestExecutionLevel user

!define UNINST_KEY "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"

!define PRODUCT_FULL_NAME   "${PRODUCT_NAME} ${PRODUCT_VERSION}${TEST__STR}"
!define SHORTCUT_NAME   	"GFD-${PRODUCT_NAME} ${PRODUCT_VERSION}${TEST__STR}"
!define PRODUCT_UNINST_KEY  "${UNINST_KEY}\${PRODUCT_NAME} ${PRODUCT_VERSION}.${SUPPORT_VERSION}"

#!system '"StampVer" -o4 -k -nopad -f"${PRODUCT_VERSION}" -p"${PRODUCT_VERSION}" "${MAKE_DIR}\GFD-${PRODUCT_NAME}.exe"'
; MUI 设置
!define MUI_WELCOMEPAGE_TITLE "　${PRODUCT_NAME} ${PRODUCT_VERSION}安装向导"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\orange.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\orange-uninstall.bmp"

!include MUI2.nsh
!include FileFunc.nsh

Name "${PRODUCT_FULL_NAME}"
BrandingText "http://www.gfdauto.net/"

OutFile "${OUT_DIR}\${OUT_FILE_NAME}"

InstallDir "C:\${PRODUCT_NAME}\${PRODUCT_VERSION}"

Page custom nsDialogsPage nsDialogsPageLeave
; 安装页面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
; 卸载页面
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
; 语言支持
!insertmacro MUI_LANGUAGE SimpChinese

Section "Installer Section"
        
	Delete "$DESKTOP\Pung*.lnk"
	Delete "$DESKTOP\GFD-Pung*.lnk"
	Delete "$SMSTARTUP\Pung*.lnk"
	Delete "$SMSTARTUP\GFD-Pung*.lnk"
	RMDir /r "$SMPROGRAMS\Pungo"
	RMDir /r "$SMPROGRAMS\Punggol"

	Delete "$DESKTOP\${PRODUCT_NAME}*.lnk"
	Delete "$DESKTOP\GFD-${PRODUCT_NAME}*.lnk"
	Delete "$SMSTARTUP\${PRODUCT_NAME}*.lnk"
	Delete "$SMSTARTUP\GFD-${PRODUCT_NAME}*.lnk"
	RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"

	SetOutPath $INSTDIR\config
	File /r /x "*.nsi" /x "*.exe" /x "*.bat" /x "*.py" /x "*.pyc" /x "*.mmp" "${CONFIG_DIR}\*"
	File "${README}"

	SetOutPath $INSTDIR
	#File /r /x "SimuDriver.dll" /x "KernelSimulator.dll" /x "config" "${MAKE_DIR}\*"
	!include "binary.nsi"
	;File /x "uninstall.exe" "${MAKE_DIR}\*"
	
	Rename "$INSTDIR\GFD-Pungo.exe" "$INSTDIR\GFD-${PRODUCT_NAME}.exe"
	
	WriteUninstaller "uninstall.exe"

	CreateShortCut "$SMSTARTUP\GFD-${PRODUCT_FULL_NAME}.lnk" "$INSTDIR\GFD-${PRODUCT_NAME}.exe"
	
	CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
	CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_VERSION}"
	CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_VERSION}\GFD-${PRODUCT_NAME}${TEST__STR}.lnk" "$INSTDIR\GFD-${PRODUCT_NAME}.exe"
	CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_VERSION}\卸载 ${PRODUCT_NAME}${TEST__STR}.lnk" "$INSTDIR\Uninstall.exe"
	
	CreateShortCut "$DESKTOP\GFD-${PRODUCT_FULL_NAME}.lnk" "$INSTDIR\GFD-${PRODUCT_NAME}.exe"
	
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_FULL_NAME}"
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\GFD-${PRODUCT_NAME}.exe"
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
	WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "谷夫道自动化"

SectionEnd

Section "un.Uninstaller Section"
        
	Delete "$DESKTOP\Pungo*.lnk"
	Delete "$DESKTOP\GFD-Pungo*.lnk"
	Delete "$SMSTARTUP\Pungo*.lnk"
	Delete "$SMSTARTUP\GFD-Pungo*.lnk"
	RMDir /r "$SMPROGRAMS\Pungo"

	Delete "$DESKTOP\${PRODUCT_NAME}*.lnk"
	Delete "$DESKTOP\GFD-${PRODUCT_NAME}*.lnk"
	Delete "$DESKTOP\${SHORTCUT_NAME}*.lnk"
	Delete "$SMSTARTUP\${PRODUCT_NAME}*.lnk"
	Delete "$SMSTARTUP\GFD-${PRODUCT_NAME}*.lnk"
	RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
	
	RMDir /r "$INSTDIR"

	DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
SectionEnd


VIProductVersion "${PRODUCT_VERSION}"

VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "CompanyName"      "谷夫道自动化"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileDescription"  "${PRODUCT_NAME} 安装程序"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileVersion"      "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "InternalName"     "${OUT_FILE_NAME}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "LegalCopyright"   "Copyright (C) 2015 谷夫道自动化"
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
	System::Call "kernel32::CreateMutexW(i 0, i 0, w 'gfdauto.com/pungo/1.0' ) i .R1 ?e"
	Pop $R0
	System::Call "kernel32::CloseHandle(i R1) i.s"
	${If} $R0 != 0
		MessageBox MB_RetryCancel|MB_ICONEXCLAMATION "${PRODUCT_NAME} 正在运行。请关闭 ${PRODUCT_NAME} 后重试。" IdRetry Retry
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
	
	!insertmacro MUI_HEADER_TEXT "${PRODUCT_FULL_NAME} 维护模式" "重新安装或卸载“${PRODUCT_FULL_NAME}”"
	nsDialogs::Create /NOUNLOAD 1018
	${NSD_CreateLabel} 0u 0u 300u 30u "请选择您要执行的操作，然后单击 [下一步(N)] 继续"

	${NSD_CreateRadioButton} 30u 30u 120u 30u "重新安装"
	Pop $RADIO_REPAIR
		${If} $Checkbox_State_REPAIR == ${BST_CHECKED}
			${NSD_Check} $RADIO_REPAIR
			${NSD_GetState} $RADIO_REPAIR $Checkbox_State
		${EndIf}

	${NSD_CreateRadioButton} 30u 60u 120u 30u "卸载"
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