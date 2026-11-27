plugins {
    id("compose.multiplatform")
    id("module.publication")
}

kotlin {
    sourceSets.commonMain.dependencies {
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsCore)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsCamera)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsGallery)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsLocation)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsBackgroundLocation)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsBluetooth)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsContacts)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsCalendar)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsNotifications)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsWifi)
        api(projects.nativecmpkitPermissions.nativecmpkitPermissionsMicrophone)
    }
}
