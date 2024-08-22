pkgname = "parallel"
pkgver = "20240822"
pkgrel = 0
build_style = "gnu_configure"
hostmakedepends = ["automake"]
depends = ["perl"]
pkgdesc = "Shell tool for executing jobs in parallel"
maintainer = "psykose <alice@ayaya.dev>"
license = "GPL-3.0-or-later"
url = "https://www.gnu.org/software/parallel"
source = f"https://ftp.gnu.org/gnu/parallel/parallel-{pkgver}.tar.bz2"
sha256 = "d7bbd95b7631980b172be04cbd2138d5f7d8c063d6da5ad8f9f70dfd88c8309d"
