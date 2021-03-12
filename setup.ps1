pip --version | Tee-Object -Variable message

$file = ""
if ( $args[0] -eq "dev" )
{
    Write-Host "******************************"
    Write-Host "*            DEV             *"
    Write-Host "******************************"
    $file = "./requirements/dev.txt";
} else
{
    $file = "./requirements/prod.txt"
}

$pat = "^.*python 3\.[1-9].*"
if ($message -match $pat) {
    Write-Host "******************************"
    Write-Host "*         using pip          *"
    Write-Host "******************************"

    pip install -r $file
} else
{
    Write-Host "******************************"
    Write-Host "*        using pip3          *"
    Write-Host "******************************"

    pip3 install -r $file
}

Write-Host "*******************************************"
Write-Host "Assuming no errors you can run the program."
Write-Host "*******************************************"
