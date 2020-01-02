#=====================================================# Start Importing Modules and Functions   #=====================================================# 
# OktaAPI Module
# https://github.com/gabrielsroka/OktaAPI.psm1
# Credit: @gabrielsroka
Import-Module OktaAPI
#=====================================================# End Importing Modules and Functions   #=====================================================# 


#=====================================================# Start Script Settings  #=====================================================# 
# Define Okta Connection String
# API token comes from Okta Admin > Security > API > Tokens > Create Token
# see https://developer.okta.com/docs/api/getting_started/getting_a_token
# Tokens are valid for 30 days and automatically refresh with each API call. 
# Tokens that are not used for 30 days will expire.
# Connection String to the Okta API. Replace YOUR_API_TOKEN and YOUR_ORG with your values.
Connect-Okta "00r9UqymNoRZfrPVYJERELuXLHSimXwBamHxxIw57e" "https://okta-demo-domain-uk.oktapreview.com"
$currentDate = (Get-Date).tostring(“yyyy-MM-dd_HH-mm-ss”)
#=====================================================# End Script Settings  #=====================================================# 

#=====================================================# Start Export Script #=====================================================# 
Write-Host "*** Exporting of Okta Config Initialised ***"

#Make Export Directory in exports subdirectory
cd "exports"
$exportDirectory = "okta_export_$currentDate"
mkdir $exportDirectory

# Export All Users and their Group Memberships and App Assignments
$totalUsers = 0
$exportedUsers = @()
# for more filters, see https://developer.okta.com/docs/api/resources/users#list-users-with-a-filter
$userParams = @{} # @{filter = 'status eq "ACTIVE"'}
do {
    $page = Get-OktaUsers @userParams
    $users = $page.objects
    $users | ConvertTo-JSON | Out-File $exportDirectory'/oktaUserExport.json'
    foreach ($user in $users) {
        $userGroups = Get-OktaUserGroups $user.id
        $groups = @()
        foreach ($userGroup in $userGroups) {
            if ($userGroup.type -eq "OKTA_GROUP" -or  $userGroup.type -eq "APP_GROUP" -or $userGroup.type -eq "BUILT_IN" ) {
                $groups += $userGroup.id
            }
        }
        $totalApps = 0
        $userAppParams = @{filter = "user.id eq `"$($user.id)`""}
        do {
            $apps = @()
            $page = Get-OktaApps @userAppParams
            $apps = $page.objects
            foreach ($app in $apps) {
                $apps += $apps.id
            }
            $totalApps += $apps.count
            $userAppParams = @{url = $page.nextUrl}
        } while ($page.nextUrl)
        
    # For User Profile Attributes, the below can be modified to add more attributes to the CSV Export
    $exportedUsers += [PSCustomObject]@{oktaUserId = $user.id;login = $user.profile.login;email = $user.profile.email;firstName = $user.profile.firstName;lastName = $user.profile.lastName;assignedGroups = $groups -join ";";assignedApps = $apps -join ";";}
    }
    $totalUsers += $users.count
    $params = @{url = $page.nextUrl}
} while ($page.nextUrl)
$exportedUsers | Export-Csv $exportDirectory'/oktaUserExport.csv' -notype
Write-Host "-- Completed User Export - $totalUsers users exported --"

#Export All Groups
$totalGroups = 0
$exportedGroups = @()
# type eq "OKTA_GROUP", "APP_GROUP" (including AD/LDAP), or "BUILT_IN" 
# see https://developer.okta.com/docs/api/resources/groups#group-type
$filter = 'type eq "APP_GROUP" or type eq "BUILT_IN" or type eq "OKTA_GROUP"' 
$groupParams = @{filter = $filter; paged = $true}
do {
    $page = Get-OktaGroups @groupParams
    $groups = $page.objects
    $groups | ConvertTo-JSON | Out-File $exportDirectory'/oktaGroupExport.json'
    foreach ($group in $groups) {
        # For Group Profile Attributs, the below can be modified to add more attributes to the CSV Export
        $exportedGroups += [PSCustomObject]@{oktaGroupId = $group.id; grouptype=$group.type; name = $group.profile.name;description = $group.profile.description}
    }
    $totalGroups += $groups.count
    $groupParams = @{url = $page.nextUrl; paged = $true}
} while ($page.nextUrl)
$exportedGroups | Export-Csv $exportDirectory'/oktaGroupExport.csv' -notype
Write-Host "-- Completed Group Export - $($groups.count) groups exported --"

#Export All Apps
$totalApps = 0
$exportedApps = @()
$appParams = @{filter = ""}
do {
    $page = Get-OktaApps @appParams
    $apps = $page.objects
    $apps | ConvertTo-JSON | Out-File $exportDirectory'/oktaAppExport.json'
    foreach ($app in $apps) {
        $total = 0
        $appGroupParams = @{appid = $app.id}
        do {
            $page = Get-OktaAppGroups @appGroupParams
            $appgroups = $page.objects
            $appsGroups = @()
            foreach ($appgroup in $appgroups) {
                $appsGroups += $appgroup.id
            }
            $appGroupParams = @{url = $page.nextUrl}
        } while ($page.nextUrl)
        $exportedApps += [PSCustomObject]@{oktaAppId = $app.id; name=$app.name;label=$app.label;signOnMode=$app.signOnMode;groupAssignments = $appsGroups -join ";";}
    } 
    $totalApps += $apps.count
    $appParams = @{url = $page.nextUrl;paged=$true}
} while ($page.nextUrl)
$exportedApps | Export-Csv $exportDirectory'/oktaAppExport.csv' -notype
Write-Host "-- Completed App Export - $totalApps Apps exported --"

#Export Network Zones
$totalZones = 0
$exportedZones = @()
$params = @{} # @{filter = ''}
do {
    $page = Get-OktaZones @params
    $zones = $page.objects
    $zones | ConvertTo-JSON | Out-File $exportDirectory'/oktaZoneExport.json'
    foreach ($zone in $zones) {
        $exportedZones += [PSCustomObject]@{id = $zone.id; name = $zone.name}
    }
    $totalZones += $zones.count
    $params = @{url = $page.nextUrl}
} while ($page.nextUrl)
$exportedZones | Export-Csv $exportDirectory'/oktaZoneExport.csv' -notype
Write-Host "-- Completed Zone Export - $totalZones Zones exported --"


#Export Okta Group Rules
$totalGroupRules = 0
$exportedGroupRules= @()
$params = @{} # @{filter = ''}
do {
    $page = Get-OktaGroupRules @params
    $groupRules = $page.objects
    $groupRules | ConvertTo-JSON | Out-File $exportDirectory'/oktaGroupRuleExport.json'
    foreach ($groupRule in $groupRules) {
        $exportedGroupRules += [PSCustomObject]@{oktaGroupRuleId = $groupRule.id;name=$groupRule.name}
    }
    $totalGroupRules += $groupRules.count
    $params = @{url = $page.nextUrl}
} while ($page.nextUrl)
$exportedGroupRules | Export-Csv $exportDirectory'/oktaGroupRuleExport.csv' -notype
Write-Host "-- Completed Group Rule Export - $totalGroupRules Group Rules exported --"

#Export Okta Inbound IDP's
$totalIDPs = 0
$exportedIDPs= @()
$params = @{} # @{filter = ''}

$page = Get-OktaIdps @params
$idps = $page.objects
$idps | ConvertTo-JSON | Out-File $exportDirectory'/oktaIDPExport.json'
foreach ($idp in $idps) {
    $exportedIDPs += [PSCustomObject]@{oktaIDPId = $idp.id;name = $idp.name;type=$idp.type}
}
$totalIDPs += $idps.count
$params = @{url = $page.nextUrl}

$exportedIDPs | Export-Csv $exportDirectory'/oktaGroupIDPExport.csv' -notype
Write-Host "-- Completed IDP Export - $totalIDPs IDPs exported --"


#Export User Schema
$userSchema = Get-OktaSchemas
$userSchema | ConvertTo-JSON | Out-File $exportDirectory'/oktaSchemaExport.json'
Write-Host "-- Completed Schema export --"


Write-Host "*** Exporting of Okta Config Complete ***"
#=====================================================# End Export Script #=====================================================# 


