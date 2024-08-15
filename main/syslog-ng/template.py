pkgname = "syslog-ng"
pkgver = "4.8.0"
pkgrel = 1
build_style = "gnu_configure"
configure_args = [
    "--sysconfdir=/etc/syslog-ng",
    "--with-python-packages=system",
    "--with-ivykis=system",
    "--with-jsonc=system",
    "--with-librabbitmq-client=system",
    "--disable-cpp",
    "--disable-systemd",
    "--disable-mongodb",
    "--disable-riemann",
    "--disable-geoip2",
    "--disable-smtp",
    "--disable-java",
    "--disable-java-modules",
    "--disable-linux-caps",
    "--disable-python-modules",
    "--enable-extra-warnings",
    "--enable-manpages",
    "--enable-native",
    "--enable-python",
    "--enable-ipv6",
    "--enable-redis",
    "--enable-stomp",
    "--enable-amqp",
    "--enable-json",
    "--enable-http",
    "--enable-sql",
]
make_cmd = "gmake"
make_install_args = ["-j1"]
hostmakedepends = [
    "automake",
    "bison",
    "file",
    "flex",
    "glib-devel",
    "gmake",
    "libtool",
    "pkgconf",
    "python-setuptools",
]
makedepends = [
    "glib-devel",
    "hiredis-devel",
    "ivykis-devel",
    "json-c-devel",
    "libcurl-devel",
    "libdbi-devel",
    "linux-headers",
    "openssl-devel",
    "pcre2-devel",
    "python-devel",
    "rabbitmq-c-devel",
]
depends = ["cmd:ugetopt!ugetopt"]
pkgdesc = "Next generation logging daemon"
maintainer = "q66 <q66@chimera-linux.org>"
license = "LGPL-2.1-or-later AND GPL-2.0-or-later"
url = "https://www.syslog-ng.com/products/open-source-log-management"
source = f"https://github.com/syslog-ng/syslog-ng/releases/download/syslog-ng-{pkgver}/syslog-ng-{pkgver}.tar.gz"
sha256 = "f2035546af5fcc0c03a8d03f5f0e929ce19131a428d611c982a5fea608a5d9d6"
# tests need https://github.com/Snaipe/Criterion
options = ["!check"]


def post_install(self):
    # service file
    self.install_service(self.files_path / "syslog-ng")

    # taken from Alpine
    self.rm(self.destdir / "etc/syslog-ng/syslog-ng.conf")
    self.install_file(self.files_path / "syslog-ng.conf", "etc/syslog-ng")

    # getent module will not work correctly on musl as musl does
    # not provide reentrant getprotoby(name|number)
    self.rm(self.destdir / "usr/lib/syslog-ng/libtfgetent.so")

    # precompile python bytecode
    from cbuild.util import python

    python.precompile(self, "etc/syslog-ng/python")
    python.precompile(self, "usr/lib/syslog-ng/python")


@subpackage("syslog-ng-scl")
def _scl(self):
    self.subdesc = "configuration library"

    return ["usr/share/syslog-ng/include/scl"]


@subpackage("syslog-ng-devel")
def _devel(self):
    return self.default_devel(
        extra=[
            "usr/share/syslog-ng/tools",
            "usr/share/syslog-ng/xsd",
        ]
    )


@subpackage("syslog-ng-python")
def _python(self):
    self.subdesc = "python module"

    return [
        "etc/syslog-ng/python",
        "usr/lib/syslog-ng/libmod-python.so",
        "usr/lib/syslog-ng/python",
    ]


def _genmod(modn, modl):
    @subpackage(f"syslog-ng-{modn}_module")
    def _mod(self):
        nonlocal modn, modl

        self.subdesc = f"{modn} module"

        if not modl:
            modl = modn

        return [f"usr/lib/syslog-ng/lib{modl}.so"]


for _modn, _modl in [
    ("add-contextual-data", None),
    ("amqp", "afamqp"),
    ("examples", None),
    ("graphite", None),
    ("http", None),
    ("json", "json-plugin"),
    ("map-value-pairs", None),
    ("redis", None),
    ("sql", "afsql"),
    ("stardate", None),
    ("stomp", "afstomp"),
    ("tags-parser", None),
    ("xml", None),
]:
    _genmod(_modn, _modl)
