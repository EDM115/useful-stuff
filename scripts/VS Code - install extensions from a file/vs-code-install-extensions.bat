@echo off
for /F "tokens=*" %%A in (extensions.txt) do (
  code --install-extension %%A --force
)
