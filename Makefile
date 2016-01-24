all: check build

build: genproject compilelib build-libs build-mods

build-libs: connectorlib iclib powerlib

build-mods: chipmod icmod jstpamod

check: libcheck modcheck genproject-verify compilelib-verify

genproject:
	python3 scripts/genproject.py lib/ agg-kicad.pro

compilelib:
	python3 scripts/compilelib.py lib/ agg-kicad.lib

connectorlib:
	python3 scripts/connectorlib.py lib/connector/conn.lib

iclib:
	python3 scripts/iclib.py lib/

powerlib:
	python3 scripts/powerlib.py lib/power/power.lib

chipmod:
	python3 scripts/chipmod.py agg.pretty/

icmod:
	python3 scripts/icmod.py agg.pretty/

jstpamod:
	python3 scripts/jstpamod.py agg.pretty/

libcheck:
	python3 scripts/libcheck.py lib/

modcheck:
	python3 scripts/modcheck.py agg.pretty/

genproject-verify:
	python3 scripts/genproject.py lib/ agg-kicad.pro --verify

compilelib-verify:
	python3 scripts/compilelib.py lib/ agg-kicad.lib --verify
