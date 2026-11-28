#!/usr/bin/env bash
# Build the exact upstream SDK against the ordinary x64 glibc baseline.
set -euo pipefail

source_dir=$(realpath "$1")
evidence_dir=$(realpath "$2")
mkdir -p "$GRADLE_USER_HOME"
gradle_home=$(realpath "$GRADLE_USER_HOME")
source_epoch=$(git -C "$source_dir" log -1 --format=%ct)
base=quay.io/pypa/manylinux2014_x86_64@sha256:e41a4e96b1e908740d0664bcaba34455a81c7219f0c0b3e093abdc058a52f551
image="nativecmpkit-openjfx-build:${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}"

docker pull --platform linux/amd64 "$base"
docker build --platform linux/amd64 --pull=false --progress=plain --tag "$image" - <<EOF
FROM $base
RUN yum --setopt=gpgcheck=1 --setopt=keepcache=1 install -y mesa-libGL-devel libX11-devel \\
    libXxf86vm-devel pkgconfig gtk3-devel libXtst-devel alsa-lib-devel bison flex gperf \\
    rh-ruby30-ruby rh-perl530 rh-perl530-perl rh-perl530-perl-Digest-MD5 \\
    rh-perl530-perl-JSON-PP rh-perl530-perl-Time-HiRes rh-perl530-perl-Term-ANSIColor \\
    rh-perl530-perl-Getopt-Long rh-perl530-perl-File-Temp rh-perl530-perl-Scalar-List-Utils \\
    rh-perl530-perl-Text-ParseWords
EOF
docker image inspect --format '{{.Id}}' "$image" > "$evidence_dir/compat-image.txt"
printf '%s\n' "$base" >> "$evidence_dir/compat-image.txt"

# Let the upstream wrapper obtain and verify its pinned distribution before the offline build.
(cd "$source_dir" && bash gradlew --version)

docker run --rm -i --network=none --user "$(id -u):$(id -g)" --workdir /openjfx/source \
  -v "$source_dir:/openjfx/source" -v "$evidence_dir:/openjfx/evidence" \
  -v "$gradle_home:/openjfx/gradle" -v "$JAVA_HOME:/opt/openjfx-jdk:ro" \
  -e HOME=/openjfx/gradle -e GRADLE_USER_HOME=/openjfx/gradle -e JAVA_HOME=/opt/openjfx-jdk \
  -e TZ=UTC -e SOURCE_DATE_EPOCH="$source_epoch" "$image" /bin/bash -s <<'BUILD'
set -eo pipefail
source /opt/rh/rh-ruby30/enable
source /opt/rh/rh-perl530/enable
set -u

test "$(uname -m)" = x86_64
test "$(getconf GNU_LIBC_VERSION)" = 'glibc 2.17'
{
  cat /etc/os-release
  getconf GNU_LIBC_VERSION
  gcc --version
  perl -MList::Util=uniq -e 'print "$List::Util::VERSION\n"'
  ruby --version
  pkg-config --modversion gtk+-3.0
  rpm -qa --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n' | sort
} > /openjfx/evidence/compat-toolchain.txt 2>&1
find /var/cache/yum -type f -name '*.rpm' -print0 | sort -z | xargs -0 -r sha256sum > /openjfx/evidence/compat-rpm-sha256.txt

materials=/openjfx/evidence/sources
mkdir -p /tmp/openjfx-tools/gcc-source /tmp/openjfx-tools/gcc-build /tmp/openjfx-tools/cmake
tar -xf "$materials/gcc-13.5.0.tar.xz" -C /tmp/openjfx-tools/gcc-source --strip-components=1
gcc_source=/tmp/openjfx-tools/gcc-source
for archive in gmp-6.2.1.tar.bz2 mpfr-4.1.0.tar.bz2 mpc-1.2.1.tar.gz isl-0.24.tar.bz2; do
  dependency=${archive%%-*}
  mkdir "$gcc_source/$dependency"
  tar -xf "$materials/$archive" -C "$gcc_source/$dependency" --strip-components=1
done
tar -xf "$materials/cmake-3.31.12-linux-x86_64.tar.gz" -C /tmp/openjfx-tools/cmake --strip-components=1
(
  cd /tmp/openjfx-tools/gcc-build
  "$gcc_source/configure" --prefix=/tmp/openjfx-tools/gcc --enable-languages=c,c++ --disable-multilib \
    --disable-bootstrap --disable-libsanitizer --disable-nls CFLAGS_FOR_TARGET='-O2 -fPIC' CXXFLAGS_FOR_TARGET='-O2 -fPIC'
  make -j4
  make install-strip
) 2>&1 | tee /openjfx/evidence/compat-compiler-build.log
rm -rf /tmp/openjfx-tools/gcc-build
export PATH="/tmp/openjfx-tools/gcc/bin:/tmp/openjfx-tools/cmake/bin:/opt/openjfx-jdk/bin:$PATH"
export CC=gcc CXX=g++ LC_ALL=C LDFLAGS='-static-libgcc -static-libstdc++'
test "$(g++ -dumpfullversion)" = 13.5.0
{
  java -version
  gcc --version
  cmake --version
  sha256sum "$gcc_source/COPYING3" "$gcc_source/COPYING.RUNTIME"
  sha256sum "$(command -v gcc)" "$(command -v g++)" "$(g++ -print-file-name=libstdc++.a)" \
    "$(gcc -print-libgcc-file-name)" "$(command -v cmake)"
} >> /openjfx/evidence/compat-toolchain.txt 2>&1

set -x
bash gradlew --no-daemon --offline --max-workers=2 --console=plain sdk \
  -PCOMPILE_WEBKIT=true -PCOMPILE_MEDIA=true -PNUM_COMPILE_THREADS=2 -PBUILD_LIBAV_STUBS=true \
  -PBUILD_WORKING_LIBAV=false -PicuVersion=77.1 -PJFX_DEPS_URL=file:///openjfx/evidence/ivy
BUILD
