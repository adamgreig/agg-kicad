ifeq ("$(V)", "1")
	verboseflag = --verbose
else
	verboseflag =
endif

all: build compile check verify

build: build-libs build-mods

build-libs: build-lib-connector build-lib-ic build-lib-power build-lib-switch

build-mods: build-mod-chip build-mod-ic build-mod-jstpa build-mod-sil-dil build-mod-jsteh build-mod-picoblade

build-verify: verify-libs verify-mods

verify-libs: verify-lib-connector verify-lib-ic verify-lib-power

verify-mods: verify-mod-chip verify-mod-ic verify-mod-jstpa verify-mod-sil-dil verify-mod-jsteh verify-mod-picoblade

compile: compile-lib compile-pro

compile-verify: verify-lib verify-pro

check: check-lib check-mod

verify: build-verify compile-verify

build-lib-connector:
	python scripts/build_lib_connector.py lib/connector/conn.lib

verify-lib-connector:
	python scripts/build_lib_connector.py lib/connector/conn.lib --verify

build-lib-switch:
	python scripts/build_lib_switch.py lib/ui/switch.lib

verify-lib-switch:
	python scripts/build_lib_switch.py lib/ui/switch.lib --verify $(verboseflag)

build-lib-ic:
	python scripts/build_lib_ic.py lib/

verify-lib-ic:
	python scripts/build_lib_ic.py lib/ --verify $(verboseflag)

build-lib-power:
	python scripts/build_lib_power.py lib/power/power.lib

verify-lib-power:
	python scripts/build_lib_power.py lib/power/power.lib --verify

build-mod-chip:
	python scripts/build_mod_chip.py agg.pretty/

verify-mod-chip:
	python scripts/build_mod_chip.py agg.pretty/ --verify $(verboseflag)

build-mod-ic:
	python scripts/build_mod_ic.py agg.pretty/

verify-mod-ic:
	python scripts/build_mod_ic.py agg.pretty/ --verify $(verboseflag)

build-mod-jstpa:
	python scripts/build_mod_jstpa.py agg.pretty/

verify-mod-jstpa:
	python scripts/build_mod_jstpa.py agg.pretty/ --verify $(verboseflag)

build-mod-jsteh:
	python scripts/build_mod_jsteh.py agg.pretty/

verify-mod-jsteh:
	python scripts/build_mod_jsteh.py agg.pretty/ --verify $(verboseflag)

build-mod-sil-dil:
	python scripts/build_mod_sil_dil.py agg.pretty/

verify-mod-sil-dil:
	python scripts/build_mod_sil_dil.py agg.pretty/ --verify $(verboseflag)

build-mod-picoblade:
	python scripts/build_mod_picoblade.py agg.pretty/

verify-mod-picoblade:
	python scripts/build_mod_picoblade.py agg.pretty/ --verify $(verboseflag)

compile-lib:
	python scripts/compile_lib.py lib/ agg-kicad.lib

verify-lib:
	python scripts/compile_lib.py lib/ agg-kicad.lib --verify

compile-pro:
	python scripts/compile_pro.py lib/ agg-kicad.pro

verify-pro:
	python scripts/compile_pro.py lib/ agg-kicad.pro --verify

check-lib:
	python scripts/check_lib.py lib/ agg.pretty/ $(verboseflag)

check-mod:
	python scripts/check_mod.py agg.pretty/ $(verboseflag)
