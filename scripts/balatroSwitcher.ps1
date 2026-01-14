Write-Host "╭────────────────────────────────╮" -ForegroundColor Yellow
Write-Host "│  🃏 Balatro Config Switcher 🎰 │" -ForegroundColor Yellow
Write-Host "╰────────────────────────────────╯" -ForegroundColor Yellow
Write-Host ""
Write-Host "Choose the config :"
Write-Host "  0  ➡️ Solo" -ForegroundColor Blue
Write-Host "  1  ➡️ PvP" -ForegroundColor Blue
Write-Host "  2  ➡️ Potluck" -ForegroundColor Blue
Write-Host "  > Heavily modded"
Write-Host "  3  ➡️ Cryptid (+ Multiplayer)" -ForegroundColor Blue
Write-Host "  4  ➡️ Yahimod" -ForegroundColor Blue
Write-Host ""

$mode = Read-Host "Enter the config number "


# ---- CONFIG ---------------------------------------------------------------
$RootPath = Join-Path $env:APPDATA "Balatro"


# --- SOLO ------------------------------------------------------------------
$Solo_FoldersToDelete = @(
    @{ Path = Join-Path $RootPath "Mods\smods" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.4.2" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.9" }
    @{ Path = Join-Path $RootPath "Mods\Cryptid-0.5.14" }
    @{ Path = Join-Path $RootPath "Mods\yahimod-balatro-v2.33" }
)

$Solo_FoldersToCopy = @(
    @{
        Source      = Join-Path $RootPath "Switcher\smods-1.0.0-beta-1016c"
        Destination = Join-Path $RootPath "Mods\smods"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\JokerDisplay-1.8.9"
        Destination = Join-Path $RootPath "Mods\JokerDisplay-1.8.9"
    }
)

# IsCompressed = $true when the file is raw-deflate compressed like in pako.inflateRaw
$Solo_FileEdits = @(
    @{
        Path        = Join-Path $RootPath "config\Steamodded.jkr"
        Pattern     = '\["achievements"\]\s*=\s*\d+'
        Replacement = '["achievements"] = 3'
        IsCompressed = $false
    },
    @{
        Path        = Join-Path $RootPath "settings.jkr"
        Pattern     = '\["profile"\]\s*=\s*\d+'
        Replacement = '["profile"]=1'
        IsCompressed = $true
    }
)


# --- PVP -------------------------------------------------------------------
$PvP_FoldersToDelete = @(
    @{ Path = Join-Path $RootPath "Mods\smods" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.4.2" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.9" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-1.0.7-beta" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-0.2.20" }
    @{ Path = Join-Path $RootPath "Mods\Cryptid-0.5.14" }
    @{ Path = Join-Path $RootPath "Mods\yahimod-balatro-v2.33" }
)

$PvP_FoldersToCopy = @(
    @{
        Source      = Join-Path $RootPath "Switcher\smods-1.0.0-beta-1016c"
        Destination = Join-Path $RootPath "Mods\smods"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\JokerDisplay-1.8.9"
        Destination = Join-Path $RootPath "Mods\JokerDisplay-1.8.9"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\multiplayer-0.2.20"
        Destination = Join-Path $RootPath "Mods\multiplayer-0.2.20"
    }
)

$PvP_FileEdits = @(
    @{
        Path        = Join-Path $RootPath "config\Steamodded.jkr"
        Pattern     = '\["achievements"\]\s*=\s*\d+'
        Replacement = '["achievements"] = 1'
        IsCompressed = $false
    },
    @{
        Path        = Join-Path $RootPath "settings.jkr"
        Pattern     = '\["profile"\]\s*=\s*\d+'
        Replacement = '["profile"]=2'
        IsCompressed = $true
    }
)


# --- POTLUCK ---------------------------------------------------------------
$Potluck_FoldersToDelete = @(
    @{ Path = Join-Path $RootPath "Mods\smods" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.4.2" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.9" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-1.0.7-beta" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-0.2.20" }
    @{ Path = Join-Path $RootPath "Mods\Cryptid-0.5.14" }
    @{ Path = Join-Path $RootPath "Mods\yahimod-balatro-v2.33" }
)

$Potluck_FoldersToCopy = @(
    @{
        Source      = Join-Path $RootPath "Switcher\smods-1.0.0-beta-0506a"
        Destination = Join-Path $RootPath "Mods\smods"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\JokerDisplay-1.8.4.2"
        Destination = Join-Path $RootPath "Mods\JokerDisplay-1.8.4.2"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\multiplayer-1.0.7-beta"
        Destination = Join-Path $RootPath "Mods\multiplayer-1.0.7-beta"
    }
)

$Potluck_FileEdits = @(
    @{
        Path        = Join-Path $RootPath "config\Steamodded.jkr"
        Pattern     = '\["achievements"\]\s*=\s*\d+'
        Replacement = '["achievements"] = 1'
        IsCompressed = $false
    },
    @{
        Path        = Join-Path $RootPath "settings.jkr"
        Pattern     = '\["profile"\]\s*=\s*\d+'
        Replacement = '["profile"]=2'
        IsCompressed = $true
    }
)

# --- CRYPTID (& Multiplayer) -----------------------------------------------
$Cryptid_FoldersToDelete = @(
    @{ Path = Join-Path $RootPath "Mods\smods" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.4.2" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.9" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-1.0.7-beta" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-0.2.20" }
    @{ Path = Join-Path $RootPath "Mods\yahimod-balatro-v2.33" }
)

$Cryptid_FoldersToCopy = @(
    @{
        Source      = Join-Path $RootPath "Switcher\smods-1.0.0-beta-1224a"
        Destination = Join-Path $RootPath "Mods\smods"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\JokerDisplay-1.8.9"
        Destination = Join-Path $RootPath "Mods\JokerDisplay-1.8.9"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\multiplayer-0.2.20"
        Destination = Join-Path $RootPath "Mods\multiplayer-0.2.20"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\Cryptid-0.5.14"
        Destination = Join-Path $RootPath "Mods\Cryptid-0.5.14"
    }
)

$Cryptid_FileEdits = @(
    @{
        Path        = Join-Path $RootPath "config\Steamodded.jkr"
        Pattern     = '\["achievements"\]\s*=\s*\d+'
        Replacement = '["achievements"] = 1'
        IsCompressed = $false
    },
    @{
        Path        = Join-Path $RootPath "settings.jkr"
        Pattern     = '\["profile"\]\s*=\s*\d+'
        Replacement = '["profile"]=3'
        IsCompressed = $true
    }
)

# --- YAHIMOD ---------------------------------------------------------------
$Yahimod_FoldersToDelete = @(
    @{ Path = Join-Path $RootPath "Mods\smods" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.4.2" }
    @{ Path = Join-Path $RootPath "Mods\JokerDisplay-1.8.9" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-1.0.7-beta" }
    @{ Path = Join-Path $RootPath "Mods\multiplayer-0.2.20" }
    @{ Path = Join-Path $RootPath "Mods\Cryptid-0.5.14" }
)

$Yahimod_FoldersToCopy = @(
    @{
        Source      = Join-Path $RootPath "Switcher\smods-1.0.0-beta-1016c"
        Destination = Join-Path $RootPath "Mods\smods"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\JokerDisplay-1.8.9"
        Destination = Join-Path $RootPath "Mods\JokerDisplay-1.8.9"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\multiplayer-0.2.20"
        Destination = Join-Path $RootPath "Mods\multiplayer-0.2.20"
    },
    @{
        Source      = Join-Path $RootPath "Switcher\yahimod-balatro-v2.33"
        Destination = Join-Path $RootPath "Mods\yahimod-balatro-v2.33"
    }
)

$Yahimod_FileEdits = @(
    @{
        Path        = Join-Path $RootPath "config\Steamodded.jkr"
        Pattern     = '\["achievements"\]\s*=\s*\d+'
        Replacement = '["achievements"] = 1'
        IsCompressed = $false
    },
    @{
        Path        = Join-Path $RootPath "settings.jkr"
        Pattern     = '\["profile"\]\s*=\s*\d+'
        Replacement = '["profile"]=3'
        IsCompressed = $true
    }
)
# ---------------------------------------------------------------------------


# Helper : raw-deflate decompress (pako.inflateRaw equivalent)
function Invoke-DeflateRawDecompress {
    param(
        [Parameter(Mandatory)]
        [byte[]] $Data
    )

    $inputStream  = New-Object System.IO.MemoryStream(,$Data)
    $defStream    = New-Object System.IO.Compression.DeflateStream(
        $inputStream,
        [System.IO.Compression.CompressionMode]::Decompress
    )
    $outputStream = New-Object System.IO.MemoryStream

    $defStream.CopyTo($outputStream)
    $defStream.Dispose()
    $inputStream.Dispose()

    return $outputStream.ToArray()
}

# Helper : raw-deflate compress (pako.deflateRaw equivalent)
function Invoke-DeflateRawCompress {
    param(
        [Parameter(Mandatory)]
        [byte[]] $Data
    )

    $outputStream = New-Object System.IO.MemoryStream
    $defStream    = New-Object System.IO.Compression.DeflateStream(
        $outputStream,
        [System.IO.Compression.CompressionMode]::Compress
    )

    $defStream.Write($Data, 0, $Data.Length)
    $defStream.Flush()
    $defStream.Dispose()

    return $outputStream.ToArray()
}

# Helper : apply regex replacements to a string
function Invoke-RegexReplace {
    param(
        [Parameter(Mandatory)]
        [string] $Text,
        [Parameter(Mandatory)]
        [string] $Pattern,
        [Parameter(Mandatory)]
        [string] $Replacement
    )

    return [regex]::Replace($Text, $Pattern, $Replacement)
}

# Helper : process editable files (plain or compressed)
function Invoke-FileEdits {
    param(
        [Parameter(Mandatory)]
        [array] $FileEdits
    )

    foreach ($edit in $FileEdits) {
        $path        = $edit.Path
        $pattern     = $edit.Pattern
        $replacement = $edit.Replacement
        $isCompressed = [bool]($edit.IsCompressed)

        if ([string]::IsNullOrWhiteSpace($path)) { continue }

        if (-not (Test-Path -LiteralPath $path)) {
            Write-Host "⏭️ $path" -ForegroundColor DarkGray -NoNewline
            Write-Host " not found (skip)"
            continue
        }

        Write-Host "📝 Editing" -NoNewline
        Write-Host " $path" -ForegroundColor DarkGray

        if ($isCompressed) {
            # --- compressed path (raw deflate) ---
            [byte[]]$bytes = [System.IO.File]::ReadAllBytes($path)

            # decompress
            $decompressedBytes = Invoke-DeflateRawDecompress -Data $bytes
            $text = [System.Text.Encoding]::UTF8.GetString($decompressedBytes)

            # regex replace
            $newText = Invoke-RegexReplace -Text $text -Pattern $pattern -Replacement $replacement

            # recompress
            $newBytes = Invoke-DeflateRawCompress -Data (
                [System.Text.Encoding]::UTF8.GetBytes($newText)
            )

            [System.IO.File]::WriteAllBytes($path, $newBytes)
        } else {
            # --- plain text path ---
            $text = Get-Content -LiteralPath $path -Raw
            $newText = Invoke-RegexReplace -Text $text -Pattern $pattern -Replacement $replacement
            Set-Content -LiteralPath $path -Value $newText -Encoding UTF8
        }
    }
}
# ---------------------------------------------------------------------------


function Invoke-Mode {
    param(
        [Parameter(Mandatory)]
        [string] $ModeName,

        [Parameter(Mandatory)]
        [array] $FoldersToDelete,

        [Parameter(Mandatory)]
        [array] $FoldersToCopy,
        
        [Parameter(Mandatory)]
        [array] $FileEdits
    )

    Write-Host ""
    Write-Host "🪄 Changing to " -ForegroundColor Cyan -NoNewline
    Write-Host $ModeName -ForegroundColor Green -NoNewline
    Write-Host " config..." -ForegroundColor Cyan
    Write-Host ""

    # 1) Delete folders
    foreach ($item in $FoldersToDelete) {
        $path = $item.Path
        if ([string]::IsNullOrWhiteSpace($path)) { continue }

        if (Test-Path -LiteralPath $path) {
            Write-Host "🗑️ Deleting" -NoNewline
            Write-Host " $path" -ForegroundColor DarkGray
            Remove-Item -LiteralPath $path -Recurse -Force
        } else {
            Write-Host "⏭️ $path" -ForegroundColor DarkGray -NoNewline
            Write-Host " not found (skip)"
        }
    }

    # 2) Copy folders
    foreach ($map in $FoldersToCopy) {
        $src = $map.Source
        $dst = $map.Destination

        if ([string]::IsNullOrWhiteSpace($src) -or [string]::IsNullOrWhiteSpace($dst)) {
            continue
        }

        if (-not (Test-Path -LiteralPath $src)) {
            Write-Host "⏭️ $src" -ForegroundColor DarkGray -NoNewline
            Write-Host " not found (skip copy)"
            continue
        }

        # If destination exists, remove it first to ensure a clean copy
        if (Test-Path -LiteralPath $dst) {
            Write-Host "⏭️ $dst" -ForegroundColor DarkGray -NoNewline
            Write-Host " exists, deleting first"
            Remove-Item -LiteralPath $dst -Recurse -Force
        }

        Write-Host "📚 Copying" -NoNewline
        Write-Host " $src  ➡️ $dst" -ForegroundColor DarkGray
        Copy-Item -LiteralPath $src -Destination $dst -Recurse
    }

    # 3) File edits (plain + pako-style compressed)
    if ($FileEdits.Count -gt 0) {
        Invoke-FileEdits -FileEdits $FileEdits
    } else {
        Write-Host "⏭️ No file edits configured for" -NoNewline
        Write-Host " $ModeName" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "✅ Switched to $ModeName config !" -ForegroundColor Green
    Write-Host ""
}


switch ($mode) {
    '0' {
        Invoke-Mode -ModeName "Solo" `
            -FoldersToDelete $Solo_FoldersToDelete `
            -FoldersToCopy   $Solo_FoldersToCopy `
            -FileEdits       $Solo_FileEdits
    }
    '1' {
        Invoke-Mode -ModeName "PvP" `
            -FoldersToDelete $PvP_FoldersToDelete `
            -FoldersToCopy   $PvP_FoldersToCopy `
            -FileEdits       $PvP_FileEdits
    }
    '2' {
        Invoke-Mode -ModeName "Potluck" `
            -FoldersToDelete $Potluck_FoldersToDelete `
            -FoldersToCopy   $Potluck_FoldersToCopy `
            -FileEdits       $Potluck_FileEdits
    }
    '3' {
        Invoke-Mode -ModeName "Cryptid (+ Multiplayer)" `
            -FoldersToDelete $Cryptid_FoldersToDelete `
            -FoldersToCopy   $Cryptid_FoldersToCopy `
            -FileEdits       $Cryptid_FileEdits
    }
    '4' {
        Invoke-Mode -ModeName "Yahimod" `
            -FoldersToDelete $Yahimod_FoldersToDelete `
            -FoldersToCopy   $Yahimod_FoldersToCopy `
            -FileEdits       $Yahimod_FileEdits
    }
    default {
        Write-Host ""
        Write-Host "❌ No valid config selected, exiting..." -ForegroundColor Red
    }
}
