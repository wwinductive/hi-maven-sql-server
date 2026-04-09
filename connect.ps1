# SQL Server Connection Script for PowerShell

# Configuration
$server = "noog-tsql01\bdp_nbs_demo01"

# Create connection with Windows authentication
$connectionString = "Server=$server;Integrated Security=true"

Write-Host "Connection String: $connectionString"

Try {
    $connection = New-Object System.Data.SqlClient.SqlConnection
    $connection.ConnectionString = $connectionString
    
    Write-Host "Attempting to connect..."
    $connection.Open()
    
    Write-Host "✓ Successfully connected to SQL Server" -ForegroundColor Green
    Write-Host "Database: $($connection.Database)"
    
    # Simple query
    $query = "SELECT 'Connected!' as Status"
    $command = New-Object System.Data.SqlClient.SqlCommand($query, $connection)
    $result = $command.ExecuteScalar()
    
    Write-Host "`nQuery Result:"
    Write-Host $result
    
    $connection.Close()
    Write-Host "`n✓ Connection closed" -ForegroundColor Green
}
Catch {
    Write-Host "✗ Connection error: $($_)" -ForegroundColor Red
    Write-Host "Error details: $($_.Exception.Message)"
}
