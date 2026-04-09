# Reusable SQL Server Query Function for PowerShell

function Query-SqlServer {
    param(
        [string]$Server = "noog-tsql01\bdp_nbs_demo01",
        [string]$Query,
        [string]$Database = "master"
    )
    
    $connectionString = "Server=$Server;Database=$Database;Integrated Security=true"
    
    try {
        $connection = New-Object System.Data.SqlClient.SqlConnection
        $connection.ConnectionString = $connectionString
        $connection.Open()
        
        $command = New-Object System.Data.SqlClient.SqlCommand($Query, $connection)
        $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($command)
        $dataset = New-Object System.Data.DataSet
        $adapter.Fill($dataset) | Out-Null
        
        $connection.Close()
        
        return $dataset.Tables[0]
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Example usage:
Write-Host "Connected to: noog-tsql01\bdp_nbs_demo01" -ForegroundColor Green
Write-Host ""

# List all tables in current database
Write-Host "Tables in database:" -ForegroundColor Cyan
$tables = Query-SqlServer -Query "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME"
if ($tables) {
    $tables | ForEach-Object { Write-Host "  - $($_.TABLE_NAME)" }
} else {
    Write-Host "  (no tables found)"
}

Write-Host ""
Write-Host "Use Query-SqlServer function for custom queries:" -ForegroundColor Yellow
Write-Host "`$result = Query-SqlServer -Query 'SELECT TOP 10 * FROM YourTable' -Database 'YourDatabase'"
