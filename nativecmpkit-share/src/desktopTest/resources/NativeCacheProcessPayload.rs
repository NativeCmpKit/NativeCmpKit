// NativeCmpKit test-only JNI versions; never packaged in library artifacts.
use core::ffi::c_void;
#[cfg(fixture_v1)]
const VERSION: i32 = 1;
#[cfg(fixture_v2)]
const VERSION: i32 = 2;
#[no_mangle]
pub extern "system" fn Java_io_github_apdelrahman1911_nativecmpkit_share_platform_NativeCacheProcessPayload_version(
    _environment: *mut c_void, _class: *mut c_void,
) -> i32 { VERSION }
