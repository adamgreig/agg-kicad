ifeq ("$(V)", "1")
	verboseflag = --verbose
else
	verboseflag =
endif

all: build compile check verify python

python:
ifeq (, $(shell which python3))
ifeq (, $(shell which python))
$(error "No python found -- install python2 or python3?")
else
PYTHON=python
endif
else
PYTHON=python3
endif

build: build-libs build-mods

build-libs: build-lib-connector build-lib-ic build-lib-power build-lib-switch

build-mods: build-mod-chip build-mod-ic build-mod-jstpa build-mod-sil-dil

build-verify: verify-libs verify-mods

verify-libs: verify-lib-connector verify-lib-ic verify-lib-power

verify-mods: verify-mod-chip verify-mod-ic verify-mod-jstpa verify-mod-sil-dil

compile: compile-lib compile-pro

compile-verify: verify-lib verify-pro

check: check-lib check-mod

verify: build-verify compile-verify

build-lib-connector:
	${PYTHON} scripts/build_lib_connector.py lib/connector/conn.lib

verify-lib-connector:
	${PYTHON} scripts/build_lib_connector.py lib/connector/conn.lib --verify

build-lib-switch:
	${PYTHON} scripts/build_lib_switch.py lib/ui/switch.lib

verify-lib-switch:
	${PYTHON} scripts/build_lib_switch.py lib/ui/switch.lib --verify $(verboseflag)

build-lib-ic:
	${PYTHON} scripts/build_lib_ic.py lib/

verify-lib-ic:
	${PYTHON} scripts/build_lib_ic.py lib/ --verify $(verboseflag)

build-lib-power:
	${PYTHON} scripts/build_lib_power.py lib/power/power.lib

verify-lib-power:
	${PYTHON} scripts/build_lib_power.py lib/power/power.lib --verify

build-mod-chip:
	${PYTHON} scripts/build_mod_chip.py agg.pretty/

verify-mod-chip:
	${PYTHON} scripts/build_mod_chip.py agg.pretty/ --verify $(verboseflag)

build-mod-ic:
	${PYTHON} scripts/build_mod_ic.py agg.pretty/

verify-mod-ic:
	${PYTHON} scripts/build_mod_ic.py agg.pretty/ --verify $(verboseflag)

build-mod-jstpa:
	${PYTHON} scripts/build_mod_jstpa.py agg.pretty/

verify-mod-jstpa:
	${PYTHON} scripts/build_mod_jstpa.py agg.pretty/ --verify $(verboseflag)

build-mod-sil-dil:
	${PYTHON} scripts/build_mod_sil_dil.py agg.pretty/

verify-mod-sil-dil:
	${PYTHON} scripts/build_mod_sil_dil.py agg.pretty/ --verify $(verboseflag)

compile-lib:
	${PYTHON} scripts/compile_lib.py lib/ agg-kicad.lib

verify-lib:
	${PYTHON} scripts/compile_lib.py lib/ agg-kicad.lib --verify

compile-pro:
	${PYTHON} scripts/compile_pro.py lib/ agg-kicad.pro

verify-pro:
	${PYTHON} scripts/compile_pro.py lib/ agg-kicad.pro --verify

check-lib:
	${PYTHON} scripts/check_lib.py lib/ agg.pretty/ $(verboseflag)

check-mod:
	${PYTHON} scripts/check_mod.py agg.pretty/ $(verboseflag)
