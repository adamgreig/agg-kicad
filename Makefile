all: check build

build: genproject compilelib build-libs build-mods

build-libs: connectorlib iclib powerlib

build-mods: chipmod icmod jstpamod

check: libcheck modcheck genproject-verify compilelib-verify

genproject:
	python scripts/genproject.py lib/ agg-kicad.pro

compilelib:
	python scripts/compilelib.py lib/ agg-kicad.lib

connectorlib:
	python scripts/connectorlib.py lib/connector/conn.lib

iclib:
	python scripts/iclib.py lib/

powerlib:
	python scripts/powerlib.py lib/power/power.lib

chipmod:
	python scripts/chipmod.py agg.pretty/

icmod:
	python scripts/icmod.py agg.pretty/

jstpamod:
	python scripts/jstpamod.py agg.pretty/

libcheck:
	python scripts/libcheck.py lib/

modcheck:
	python scripts/modcheck.py agg.pretty/

genproject-verify:
	python scripts/genproject.py lib/ agg-kicad.pro --verify

compilelib-verify:
	python scripts/compilelib.py lib/ agg-kicad.lib --verify
