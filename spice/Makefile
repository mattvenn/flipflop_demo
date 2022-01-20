setup:
	mkdir csv

feedback: feedback_demo.spice
	ngspice $^

sim: simulation.spice
	rm -f csv/*
	# run the simulation
	ngspice $^

png:
	\ls pss/ | while read ps ; do convert -density 100 pss/$$ps pngs/$$ps.png ; done

# will probably fail due to imagemagic's policy.xml not allowing enough memory/disk
animation.gif: pngs/*
	convert -delay 1 $$(\ls -v pngs/*) $@

clean:
	rm -f pngs/* pss/* animation.gif

phony: clean png setup
