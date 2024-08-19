pkgname = "perf"
pkgver = "6.10.6"
pkgrel = 0
build_wrksrc = "tools/perf"
build_style = "makefile"
make_cmd = "gmake"
make_build_args = [
    "-f",
    "Makefile.perf",
    "LLVM=1",
    "NO_LIBAUDIT=1",
    "NO_LIBBABELTRACE=1",
    "NO_LIBPFM4=1",
    "NO_LIBUNWIND=1",
    "NO_SDT=1",
    "STRIP=/bin/true",
    "V=1",
    "WERROR=0",
    "libdir=/usr/lib",
    "mandir=/usr/share/man",
    "prefix=/usr",
    "sbindir=/usr/bin",
]
make_install_args = [
    "install-python_ext",
    *make_build_args,
]
make_use_env = True
hostmakedepends = [
    "asciidoc",
    "bash",
    "bison",
    "flex",
    "gmake",
    "pkgconf",
    "python-setuptools",
    "xmlto",
]
makedepends = [
    "capstone-devel",
    "elfutils-devel",
    "libcap-devel",
    "libnuma-devel",
    "libtraceevent-devel",
    "linux-headers",
    "openssl-devel",
    "perl",
    "python-devel",
    "slang-devel",
    "xz-devel",
    "zlib-ng-compat-devel",
    "zstd-devel",
]
pkgdesc = "Linux performance analyzer"
maintainer = "psykose <alice@ayaya.dev>"
license = "GPL-2.0-only"
url = "https://perf.wiki.kernel.org/index.php/Main_Page"
source = f"https://cdn.kernel.org/pub/linux/kernel/v{pkgver[:pkgver.find('.')]}.x/linux-{pkgver}.tar.xz"
sha256 = "e0d50d5b74f8599375660e79f187af7493864dba5ff6671b14983376a070b3d1"
# nope
# docs are a single tips file that gets displayed in the TUI
options = ["!check", "!splitdoc"]
# MAKE is ignored in some places
exec_wrappers = [("/usr/bin/gmake", "make")]


def init_build(self):
    self.make_build_args += [f"EXTRA_CFLAGS={self.get_cflags(shell=True)}"]
    self.make_install_args += [f"EXTRA_CFLAGS={self.get_cflags(shell=True)}"]


def post_install(self):
    # relink hardlink
    self.uninstall("usr/bin/trace")
    self.install_link("usr/bin/trace", "perf")
    # valid as both
    self.uninstall("etc/bash_completion.d")
    self.install_completion("perf-completion.sh", "bash")
    self.install_completion("perf-completion.sh", "zsh")
    # pointless tests
    self.uninstall("usr/libexec/perf-core/tests")
