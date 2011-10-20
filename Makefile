PKG_NAME := alsa-utils
SPECFILE = $(addsuffix .spec, $(PKG_NAME))
YAMLFILE = $(addsuffix .yaml, $(PKG_NAME))


include /usr/share/packaging-tools/Makefile.common
