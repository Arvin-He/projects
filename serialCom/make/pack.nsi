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


; MUI 设置
!define MUI_WELCOMEPAGE_TITLE "  ${PRODUCT_NAME} ${PRODUCT_VERSION}安装向导"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Header\orange.bmp"
!define MUI_HEADERIMAGE_UNBITMAP "${NSISDIR}\Contrib\Graphics\Header\orange-uninstall.bmp"

!include MUI2.nsh
!include FileFunc.nsh

Name "${PRODUCT_NAME}"
BrandingText "http://www.microbit.com/"
; 输出文件
OutFile "${OUT_DIR}\${OUT_FILE_NAME}"
; 安装路径
InstallDir "C:\${PRODUCT_NAME}"
;安装显示图标及图片
;!define MUI_ICON "favor.ico"
;卸载图标
;!define MUI_UNICON "uninst.ico"

;Icon "favor.ico"
;UninstallIcon "uninst.ico"

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
	Delete "$DESKTOP\${PRODUCT_NAME}*.lnk"
	Delete "$SMSTARTUP\${PRODUCT_NAME}*.lnk"
	RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"
	
	SetOutPath $INSTDIR
    ; 主要是拷贝需要的文件,包括依赖,图标,配置文件等等,一般程序会事先打包到一个目录下,如build\exe.win-amd64-3.6\下
	File /r "..\serialcom\build\exe.win32-3.6\*"
	;File /r "..\serialcom\build\exe.win32-3.4\*"
	
	File /r "..\serialcom\config"
	;File /r "..\serialcom\userdata"
	;File /r "..\serialcom\log"
	File "favor.ico"
	File "uninst.ico"

	WriteUninstaller "uninstall.exe"
    ; 设置开机启动
    CreateShortCut "$SMSTARTUP\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe" 

	CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
	CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\卸载 ${PRODUCT_NAME}.lnk" "$INSTDIR\Uninstall.exe"
	
	CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe" "" "$INSTDIR\favor.ico"
	CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\${PRODUCT_NAME}.exe" "" "$INSTDIR\favor.ico"
	
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
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "CompanyName"      "MicroBit Auto"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileDescription"  "${PRODUCT_NAME} 安装程序"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "FileVersion"      "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "InternalName"     "${OUT_FILE_NAME}"
VIAddVersionKey /LANG=${LANG_SIMPCHINESE} "LegalCopyright"   "Copyright (C) 2017 Arvin"
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
		MessageBox MB_RetryCancel|MB_ICONEXCLAMATION "${PRODUCT_NAME} 正在运行. 请关闭 ${PRODUCT_NAME} 后重试" IdRetry Retry
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
	
	!insertmacro MUI_HEADER_TEXT "${PRODUCT_NAME} 维护模式" "重新安装或卸载“${PRODUCT_NAME}”"
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