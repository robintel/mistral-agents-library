@echo off
rem CMD entry point for the installer. A thin wrapper: everything
rem below is install.ps1 running under PowerShell with the
rem execution policy bypassed for this one invocation, arguments
rem forwarded - so cmd, PowerShell, and Python all install the
rem same byte-identical batch (see DEPLOYING.md).
rem   install.bat -Dest DIR -Target REPO -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
exit /b %ERRORLEVEL%
