# CCPM PowerShell Wrapper
# Provides 'pm' command for all CCPM operations

function pm {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Command,
        
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$Arguments
    )

    $scriptDir = Join-Path (Get-Location) "ccpm/scripts/pm"
    $scriptName = "$scriptDir/$Command.sh"
    
    if (-not (Test-Path $scriptName)) {
        Write-Host "❌ Command not found: pm $Command"
        Write-Host "Available commands:"
        Get-ChildItem $scriptDir -Filter "*.sh" | ForEach-Object {
            $cmdName = $_.BaseName
            Write-Host "  pm $cmdName"
        }
        return
    }
    
    # Run the bash script with arguments
    & "C:\Program Files\Git\bin\bash.exe" $scriptName @Arguments
}

Write-Host "✅ CCPM PowerShell wrapper loaded"
Write-Host "Usage: pm <command> [arguments]"
Write-Host "Example: pm status"
Write-Host ""
Write-Host "Type 'pm help' for all available commands"
