ifeq ("$(V)", "1")
	verboseflag = --verbose
else
	verboseflag =
endif

all: build compile check verify

build: build-libs build-mods

build-libs: build-lib-connector build-lib-ic build-lib-power build-lib-switch

build-mods: build-mod-chip build-mod-ic build-mod-jstpa build-mod-sil-dil build-mod-jsteh build-mod-picoblade build-mod-tfml-sfml

build-verify: verify-libs verify-mods

verify-libs: verify-lib-connector verify-lib-ic verify-lib-power

verify-mods: verify-mod-chip verify-mod-ic verify-mod-jstpa verify-mod-sil-dil verify-mod-jsteh verify-mod-picoblade

compile: compile-lib compile-sym-lib-table

compile-verify: verify-lib verify-sym-lib-table

check: check-lib check-mod

verify: build-verify compile-verify

build-lib-connector:
	python3 scripts/build_lib_connector.py lib/connector/conn.kicad_sym

verify-lib-connector:
	python3 scripts/build_lib_connector.py lib/connector/conn.kicad_sym --verify

build-lib-switch:
	python3 scripts/build_lib_switch.py lib/ui/switch.kicad_sym

verify-lib-switch:
	python3 scripts/build_lib_switch.py lib/ui/switch.kicad_sym --verify $(verboseflag)

build-lib-ic:
	python3 scripts/build_lib_ic.py lib/

verify-lib-ic:
	python3 scripts/build_lib_ic.py lib/ --verify $(verboseflag)

build-lib-power:
	python3 scripts/build_lib_power.py lib/power/power.kicad_sym

verify-lib-power:
	python3 scripts/build_lib_power.py lib/power/power.kicad_sym --verify

build-mod-chip:
	python3 scripts/build_mod_chip.py agg.pretty/ mod/chip

verify-mod-chip:
	python3 scripts/build_mod_chip.py agg.pretty/ mod/chip --verify $(verboseflag)

build-mod-ic:
	python3 scripts/build_mod_ic.py agg.pretty/ mod/ic

verify-mod-ic:
	python3 scripts/build_mod_ic.py agg.pretty/ mod/ic --verify $(verboseflag)

build-mod-jstpa:
	python3 scripts/build_mod_jstpa.py agg.pretty/

verify-mod-jstpa:
	python3 scripts/build_mod_jstpa.py agg.pretty/ --verify $(verboseflag)

build-mod-jsteh:
	python3 scripts/build_mod_jsteh.py agg.pretty/

verify-mod-jsteh:
	python3 scripts/build_mod_jsteh.py agg.pretty/ --verify $(verboseflag)

build-mod-sil-dil:
	python3 scripts/build_mod_sil_dil.py agg.pretty/

verify-mod-sil-dil:
	python3 scripts/build_mod_sil_dil.py agg.pretty/ --verify $(verboseflag)

build-mod-picoblade:
	python3 scripts/build_mod_picoblade.py agg.pretty/

verify-mod-picoblade:
	python3 scripts/build_mod_picoblade.py agg.pretty/ --verify $(verboseflag)

build-mod-tfml-sfml:
	python3 scripts/build_mod_tfml_sfml.py agg.pretty/

verify-mod-tfml-sfml:
	python3 scripts/build_mod_tfml_sfml.py agg.pretty/ --verify $(verboseflag)

compile-lib:
	python3 scripts/compile_lib.py lib/ agg-kicad.kicad_sym

verify-lib:
	python3 scripts/compile_lib.py lib/ agg-kicad.kicad_sym --verify

compile-sym-lib-table:
	python3 scripts/compile_sym_lib_table.py lib/ sym-lib-table

verify-sym-lib-table:
	python3 scripts/compile_sym_lib_table.py lib/ sym-lib-table --verify

check-lib:
	python3 scripts/check_lib.py lib/ agg.pretty/ $(verboseflag)

check-mod:
	python3 scripts/check_mod.py agg.pretty/ $(verboseflag)
