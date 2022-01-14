setup:
	mkdir pngs pss

sim: simulation.spice
	# run the simulation
	ngspice $^

png:
	\ls pss/ | while read ps ; do convert -density 100 pss/$$ps pngs/$$ps.png ; done

animation.gif: pngs/*
	convert -delay 1 $$(\ls -v pngs/*) $@

clean:
	rm -f pngs/* pss/* animation.gif

phony: clean png setup
