; 以下脚本用以生成 study.exe 文件
; 安装时若发现应用程序正在运行，安装程序会提示并替用户关闭应用程序
; 安装成功后会自动运行应用程序
; 启用新的 Modern UI 的宏指令语法，原先的部分指令将被禁止以防止重复
; 我会尽量展示如何基本指令的用法。当然宏指令也会与一些基本指令发生重
; 复定义的情况，不过 NSIS 照样能编译成功.
; 其中的一些路径、文件你可以根据需要更改

; 启用外部压缩工具（这里我们不用，原因看第 10 步）
;!define HAVE_UPX
; 若启用了外部压缩工具，这进行可执行文件头的压缩
!ifdef HAVE_UPX
; 用 UPX 压缩可执行文件头（用其他的相关工具也行）
!packhdr tmp.dat "E:UPX\upx --best tmp.dat"
!endif

; 编译选项

; 设置覆盖标记
SetOverwrite on
; 设置压缩选项
SetCompress auto
; 选择压缩方式
SetCompressor bzip2
; 设置数据块优化
SetDatablockOptimize on
; 设置数据写入时间
SetDateSave on

; 相关数据预设

; 软件的名字，后面的${NAME}调用这个名字
!define NAME "NSIS"
!define NAME_FULL "全方位掌握 NSIS 的使用"
!verbose 3
; 包含窗口消息定义文件
;!include "${NSISDIR}\Examples\WinMessages.nsh"
; 包含新界面的宏指令文件
;!include "${NSISDIR}\Examples\Modern UI\ModernUI.nsh"
; 包含标牌位图宏指令文件
;!include "${NSISDIR}\Examples\branding.nsh"
!verbose 4
!define CURRENTPAGE $9
!define TEMP1 $R0
!define TEMP2 $R1

; 插入安装界面宏定义（这里我禁用了，启用也没问题。编译照样通过。后面我都定义过了）
;!insertmacro MUI_INTERFACE "modern2.exe" "adni18-installer-C-no48xp.ico" "adni18-uninstall-C-no48xp.ico" "modern.bmp" "smooth"

; 安装程序设置

; 输出文件
OutFile "F:\study.exe"
; 安装程序名称
Name /LANG=2052 "NSIS"
; 替换对话框样式
ChangeUI all "${NSISDIR}\Contrib\UIs\modern.exe"
; 启用 WindowsXP 的视觉样式
XPstyle on
;设置字体
SetFont 宋体 9
; 标题名称
Caption "全方位掌握 NSIS 的使用"
; 标牌的内容
BrandingText /TRIMCENTER "Shao Hao"
; 安装程序图标
Icon "favor.ico"
; 安装程序显示标题
WindowIcon on
; 添加标牌位图（放在顶部用 TOP 参数。后面接高度）
AddBrandingImage LEFT 105
; 设定渐变背景
BGGradient off
; 设置安静安装模式
;SilentInstall normal
; 设置安静卸载模式
;SilentUnInstall normal
; 执行 CRC 检查（最好用 on 打开。关闭是因为还要修改安装程序，看第 10 步）
CRCCheck off
; 加载相应的语言文件
LoadLanguageFile "${NSISDIR}\Contrib\Language files\SimpChinese.nlf"
; 替换各个对话框标题的文字
SubCaption 0 "授权协议"
SubCaption 1 "安装选项"
SubCaption 2 "安装目录"
SubCaption 3 "正在安装"
SubCaption 4 "完成安装"
; 替换默认按钮的文字
MiscButtonText "< 上一步" "下一步 >" "取消" "关闭"
; 替换“安装”按钮的文字
;InstallButtonText "安装"
; 替换当文件无法被写入时的警告窗的文字
FileErrorText "无法写入文件$\r$\n$0$\r$\n请确认文件属性不是只读且未被使用中！"

; 默认的安装目录
InstallDir "$PROGRAMFILES\QCD 3"
; 如果可能的化从注册表中监测安装路径
InstallDirRegKey HKLM \
"Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS" \
"UninstallString"

; 授权协议页面
LicenseText "NSIS 是免费软件。安装前请先阅读以下协议条款" "我同意"
; 使用授权协议文本
LicenseData "F:\12\License.txt"
; 设置授权协议页面的背景色
;LicenseBkColor 000000

; 选择要按安装的组件
ComponentText "现在将安装 ${NAME_FULL}到您的计算机：" "请选择安装类型" "或选择您希望安装的组件"
InstType "完全安装(都在了)"
InstType "典型安装"
InstType /CUSTOMSTRING=自定义?
;InstType /NOCUSTOM
;InstType /COMPONENTSONLYONCUSTOM
CheckBitmap "${NSISDIR}\Contrib\Icons\modern.bmp"
; 替换显示磁盘空间信息的文字
SpaceTexts "所需空间：" "可用空间："

; 提示用户输入目录的文本
; DirShow hide
; 替换显示选择安装目录的文字
DirText "请选择 ${NAME} 的安装路径：" "选择目录用以安装 ${NAME}：" "浏览..."
; 是否允许安装在根目录下
AllowRootDirInstall false

; 安装信息的颜色
;InstallColors 000000 FFFFFF
; 安装进度条显示方式
InstProgressFlags smooth colored
; 完成后自动关闭安装程序
AutoCloseWindow true
; 显示“显示详细细节”对话框
ShowInstDetails hide
; 替换“显示细节”按钮的文字
DetailsButtonText "显示细节"
; 替换“完成”按钮的文字
CompletedText "已完成"

; 卸载程序设置

; 替换卸载程序的文字
UninstallText "现在将从你的系统中卸载 ${NAME}：" "卸载目录："
; 卸载程序图标
UninstallIcon "F:\12\UnQCDIcon.ico"
; 替换卸载程序标题的文字
UninstallCaption /LANG=2052 "卸载 ${NAME}"
; 替换卸载程序每页按钮的文字
UninstallSubCaption /LANG=2052 0 "：确认"
UninstallSubCaption /LANG=2052 1 "：正在删除文件"
UninstallSubCaption /LANG=2052 2 "：完成"
; 卸载程序显示方式
ShowUninstDetails hide
; 替换“卸载”按钮的文字
UninstallButtonText /LANG=2052 "卸载"

; 安装程序内容及其相关的回调函数

; 安装程序内容
Section /e "!主要程序(必须安装)" SecCore
SectionIn 1 2 RO
; 设置输出路径，每次使用都会改变
SetOutPath $INSTDIR
; 循环包含目录下全部内容
File /r "F:\12\1\*.*"
; 只包含一个文件
File "F:\12\gf.gif"
; 处理动态连接库文件
IfFileExists "$INSTDIR\1.dll" 0 NoFile1
; 取消组件注册
UnRegDll "$INSTDIR\1.dll"
Delete "$INSTDIR\1.dll"
NoFile1:
File "F:\12\1.dll"
; 注册组件
RegDLL "$INSTDIR\QCDIconMgr.dll"
; 写入软件注册键值
WriteRegStr HKLM "Software\NSIS\NSIS" "" "$INSTDIR"
; 为 Windows 卸载程序写入键值
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS" "DisplayName" "NSIS（只用于移除）"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS" "UninstallString" '"$INSTDIR\uninst.exe"'
; 写入生成卸载程序（可多次使用）
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section /e "扩展(可选)" SecUpdate
SectionIn 1
SetOutPath "$INSTDIR\Plugins"
File "F:\12\qcdplus\Plugins\2.dll"
File /r "F:\12\qcdplus\Plugins\3"
SectionEnd

SubSection /e "选项" SecOptions
Section /e "创建桌面图标" SecDesktopShortCut
SectionIn 1 2
SetOutPath "$INSTDIR\Plugins"
CreateShortCut "$DESKTOP\NSIS.lnk" "$INSTDIR\gf.gif"
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section /e "创建快速启动栏图标" SecQuickbarShortCut
SectionIn 1 2
SetOutPath "$INSTDIR\Plugins"
CreateShortCut "$QUICKLAUNCH\NSIS.lnk" "$INSTDIR\gf.gif"
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd

Section /e "创建 NSIS 程序组" SecShortCutGroup
SectionIn 1 2
SetOutPath "$INSTDIR\Plugins"
CreateDirectory "$SMPROGRAMS\NSIS"
CreateShortCut "$SMPROGRAMS\QCD Player\gf.lnk" "$INSTDIR\gf.gif"
WriteUninstaller "$INSTDIR\uninst.exe"
SectionEnd
SubSectionEnd

Section "-Run"; 运行?
ExecWait '"$INSTDIR\2.exe" -p'
WriteINIStr "$INSTDIR\NSIS.ini" "2" "Language" "Chinese"
Exec "$INSTDIR\2.exe"
ExecShell open "$INSTDIR\汉化说明.htm"
SectionEnd

Section ""
;Invisible section to display the Finish header
!insertmacro MUI_FINISHHEADER SetHeader
SectionEnd

; 安装程序初始化设置
Function .onInit
; 发现有程序正在运行时提示退出后继续运行
loop:
FindWindow $R0 "NSIS"
IntCmp $R0 0 done
MessageBox MB_OKCANCEL \
"NSIS 正在运行。$\n点击“确定”按钮会关闭 NSIS 然后继续安装，点击“取消”按钮将退出安装程序" \
IDOK NoAbort
Abort
NoAbort:
SendMessage $R0 1029 0 0
; 稍等后继续检测直至检测不到或用户选择取消
Sleep 444
Goto loop
done:
; 显示 Logo 画面
SetOutPath $TEMP
File /oname=qcd_logo.bmp "F:\12\logo.bmp"
File /oname=magiclime.exe "${NSISDIR}\Bin\magiclime.exe"
ExecWait '"$TEMP\magiclime.exe" qcd_logo.bmp'
Delete "$TEMP\magiclime.exe"
Delete "$TEMP\qcd_logo.bmp"
; 初始化标牌位图
!insertmacro BI_INIT $R0
FunctionEnd

; 安装程序主界面的相关文本
Function SetHeader
!insertmacro MUI_HEADER_INIT
!insertmacro MUI_HEADER_START 1
!insertmacro MUI_HEADER_TEXT 2052 "授权协议" "安装 ${NAME} 之前，请认真阅读一下授权条款."
!insertmacro MUI_HEADER_STOP 1
!insertmacro MUI_HEADER_START 2
!insertmacro MUI_HEADER_TEXT 2052 "选择组件" "请选择你要安装的组件."
!insertmacro MUI_HEADER_STOP 2
!insertmacro MUI_HEADER_START 3
!insertmacro MUI_HEADER_TEXT 2052 "选择安装位置" "为 ${NAME} 选择一个安装目录."
!insertmacro MUI_HEADER_STOP 3
!insertmacro MUI_HEADER_START 4
!insertmacro MUI_HEADER_TEXT 2052 "安装" "${NAME} 已经安装，请等待."
!insertmacro MUI_HEADER_STOP 4
!insertmacro MUI_HEADER_START 5
!insertmacro MUI_HEADER_TEXT 2052 "完成" "安装顺利完成."
!insertmacro MUI_HEADER_STOP 5
!insertmacro MUI_HEADER_END
FunctionEnd

; 初始化安装程序对话框的显示文本
Function .onInitDialog
!insertmacro MUI_INNERDIALOG_INIT
!insertmacro MUI_INNERDIALOG_START 1
!insertmacro MUI_INNERDIALOG_TEXT 2052 1040 "如果你同意协议中的所有条款,选择“我同样”继续安装,如果你选择了“取消”,安装程序将终止,只有接受条款才能安装 ${NAME}."
!insertmacro MUI_INNERDIALOG_STOP 1
!insertmacro MUI_INNERDIALOG_START 2
!insertmacro MUI_INNERDIALOG_TEXT 2052 1042 "描述"
!insertmacro MUI_INNERDIALOG_TEXT 2052 1043 "移动你的鼠标到组件上,便可以见到相关的描述."
!insertmacro MUI_INNERDIALOG_STOP 2
!insertmacro MUI_INNERDIALOG_START 3
!insertmacro MUI_INNERDIALOG_TEXT 2052 1041 "目标文件夹"
!insertmacro MUI_INNERDIALOG_STOP 3
!insertmacro MUI_INNERDIALOG_END
FunctionEnd

; 转到下页面时的处理
Function .onNextPage
!insertmacro MUI_NEXTPAGE_OUTER
!insertmacro MUI_NEXTPAGE SetHeader
; 标牌位图设置
!insertmacro BI_NEXT
FunctionEnd

; 转到上一页面时的处理
Function .onPrevPage
!insertmacro MUI_PREVPAGE
; 标牌位图设置
!insertmacro BI_PREV
FunctionEnd

; 鼠标移到指定组件时的显示处理
Function .onMouseOverSection
; 用宏指令设置安装自己的注释文本
!insertmacro MUI_DESCRIPTION_INIT
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecCore} "安装主应用程序"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecUpdate} "安装 NSIS 的更新或新增插件"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecOptions} "选择 NSIS 的其他安装选项，例如：创建快捷方式和应用程序组的"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecDesktopShortCut} "在用户的桌面上创建 NSIS 的快捷方式"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecQuickbarShortCut} "在用户的快速栏里创建 NSIS 快捷方式"
!insertmacro MUI_DESCRIPTION_TEXT 2052 ${SecShortCutGroup} "在用户的开始菜单的程序中创建 NSIS 的快捷方式组"
!insertmacro MUI_DESCRIPTION_END
FunctionEnd

; 安装成功完成后的设置
Function .onInstSuccess
; 自己加吧:)
FunctionEnd

; 放弃安装时警告窗口的显示信息
Function .onUserAbort
!insertmacro MUI_ABORTWARNING 2052 "你确定要推出 ${NAME} 的安装吗?"
!insertmacro MUI_ABORTWARNING_END
FunctionEnd

; 安装程序标牌位图列表
!insertmacro BI_LIST
!insertmacro BI_LIST_ADD "F:\12\Brand1.bmp" /RESIZETOFIT
!insertmacro BI_LIST_ADD "F:\12\Brand2.bmp" /RESIZETOFIT
!insertmacro BI_LIST_ADD "F:\12\Brand3.bmp" /RESIZETOFIT
!insertmacro BI_LIST_END

; 卸载程序及其相关回调函数

; 卸载程序内容
Section "Uninstall"
ExecWait '"$INSTDIR\12.exe" /un'
; 循环删除文件直至删除文件夹
RMDir /r "$SMPROGRAMS\NSIS"
UnRegDLL "$INSTDIR\2.dll"
Delete "$INSTDIR\QCDIconMgr.dll"
Delete "$INSTDIR\*.*"
DeleteRegKey HKLM "Software\NSIS"
DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\NSIS"
MessageBox MB_YESNO|MB_ICONQUESTION \
"是否连插件目录也要删除？$\n(若您要保留这些文件，请点击下面的“否”按钮)" \
IDNO NoDelete
; 全删光！！！
RMDir /r "$INSTDIR"
NoDelete:
SectionEnd

; 定义卸载程序标牌位图
!define BI_UNINSTALL
!include "${NSISDIR}\Examples\branding.nsh"

; 初始化卸载程序对话框的设置
Function un.onInit
; 初始化标牌位图
!insertmacro BI_INIT $R0
FunctionEnd

; 卸载程序主界面的相关文本
Function un.SetHeader
!insertmacro MUI_HEADER_INIT
!insertmacro MUI_HEADER_START 1
!insertmacro MUI_HEADER_TEXT 2052 "卸载 ${NAME}" "${NAME_FULL} 将从你的系统里移除."
!insertmacro MUI_HEADER_STOP 1
!insertmacro MUI_HEADER_START 2
!insertmacro MUI_HEADER_TEXT 2052 "卸载" "${NAME} 正在被卸载，请等待."
!insertmacro MUI_HEADER_STOP 2
!insertmacro MUI_HEADER_START 3
!insertmacro MUI_HEADER_TEXT 2052 "完成" "${NAME_FULL} 已从你的系统中移除."
!insertmacro MUI_HEADER_STOP 3
!insertmacro MUI_HEADER_END
FunctionEnd

; 初始化卸载程序对话框时的处理
Function un.onInitDialog
; 自己加:)
FunctionEnd

; 卸载程序转到下一页时的处理
Function un.onNextPage
!insertmacro MUI_NEXTPAGE_OUTER
!insertmacro MUI_NEXTPAGE un.SetHeader
; 标牌位图设置
!insertmacro BI_NEXT
FunctionEnd

; 卸载程序完成时的处理
Function un.onUninstSuccess
; 再加^_^
FunctionEnd

; 放弃卸载程序时的处理
Function un.onUserAbort
FunctionEnd

; 卸载程序标牌位图列表
!insertmacro BI_LIST
!insertmacro BI_LIST_ADD "F:\12\UnBrand1.bmp" /RESIZETOFIT
!insertmacro BI_LIST_ADD "F:\12\UnBrand2.bmp" /RESIZETOFIT
!insertmacro BI_LIST_END

; 结束