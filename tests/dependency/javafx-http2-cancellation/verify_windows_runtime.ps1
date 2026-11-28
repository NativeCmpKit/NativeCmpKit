param(
    [Parameter(Mandatory = $true)][string] $Sdk,
    [Parameter(Mandatory = $true)][string] $VisualStudio,
    [Parameter(Mandatory = $true)][string] $Report
)

$ErrorActionPreference = 'Stop'
$vcRedist = Join-Path $VisualStudio 'VC/Redist/MSVC'
$kitRedist = Join-Path ${env:ProgramFiles(x86)} 'Windows Kits/10/Redist'
$vcDirs = @(Get-ChildItem -Directory -LiteralPath $vcRedist | ForEach-Object {
    Join-Path $_.FullName 'x64/Microsoft.VC143.CRT'
} | Where-Object { Test-Path -LiteralPath $_ -PathType Container })
$kitDirs = @(@($kitRedist) + @(Get-ChildItem -Directory -LiteralPath $kitRedist).FullName |
    ForEach-Object { Join-Path $_ 'ucrt/DLLs/x64' } |
    Where-Object { Test-Path -LiteralPath $_ -PathType Container })
if (!$vcDirs -or !$kitDirs) { throw 'Expected the official x64 VC143 and Kit UCRT redistributable directories' }

$runtime = @(Get-ChildItem -File -LiteralPath (Join-Path $Sdk 'bin') | Where-Object {
    $_.Name -match '^(?:api-ms-win-.*|msvcp140(?:_[12])?|vcruntime140(?:_1)?|ucrtbase)\.dll$'
})
[string[]] $names = @($runtime | ForEach-Object { $_.Name.ToLowerInvariant() })
[Array]::Sort($names, [StringComparer]::Ordinal)
$nameBytes = [Text.Encoding]::UTF8.GetBytes(($names -join "`n") + "`n")
$namesHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($nameBytes)).ToLowerInvariant()
if ($names.Count -ne 46 -or $namesHash -ne '1648d06f5dab00601e46ec258163963b511cdaec7661427b9cd48ca737040c49') {
    throw 'The x64 CRT file names differ from the official OpenJFX 21.0.13 Windows classifier'
}

$entries = foreach ($dll in $runtime) {
    $apiSet = $dll.Name.StartsWith('api-ms-win-', [StringComparison]::OrdinalIgnoreCase)
    $candidates = if ($apiSet -or $dll.Name -eq 'ucrtbase.dll') { $kitDirs } else { $vcDirs }
    $digest = (Get-FileHash -Algorithm SHA256 -LiteralPath $dll.FullName).Hash
    $origin = $candidates | ForEach-Object { Join-Path $_ $dll.Name } | Where-Object {
        (Test-Path -LiteralPath $_ -PathType Leaf) -and ((Get-FileHash -Algorithm SHA256 -LiteralPath $_).Hash -eq $digest)
    } | Select-Object -First 1
    if (!$origin) { throw "The SDK DLL $($dll.Name) differs from all installed official x64 redistributable copies" }
    $signature = Get-AuthenticodeSignature -LiteralPath $origin
    if ($signature.Status -eq 'Valid') {
        if ($signature.SignerCertificate.Subject -notmatch '(?:^|,\s*)O=Microsoft Corporation(?:,|$)') {
            throw "The SDK DLL $($dll.Name) does not have the expected Microsoft signer"
        }
    } elseif (!$apiSet -or $signature.Status -ne 'NotSigned') {
        throw "The SDK DLL $($dll.Name) signature status is $($signature.Status)"
    }
    [ordered] @{
        name = $dll.Name
        size = $dll.Length
        sha256 = $digest.ToLowerInvariant()
        source = $origin
        file_version = $dll.VersionInfo.FileVersion
        signature_status = $signature.Status.ToString()
        signature_type = $signature.SignatureType.ToString()
        signer_thumbprint = $signature.SignerCertificate.Thumbprint
    }
}
[ordered] @{ compared_file_count = $entries.Count; stock_name_sha256 = $namesHash; files = $entries } |
    ConvertTo-Json -Depth 4 | Set-Content -Encoding utf8 $Report
