BIN = $(PWD)/venv/bin
ROOM = study

run: venv
	$(BIN)/python3 action-clock.py -v3
	
time: venv
	$(BIN)/python3 action-clock.py --site $(ROOM) -v3

chime: venv
	$(BIN)/python3 action-clock.py --site $(ROOM) --chime DEFAULT -v3

chimes: venv
	$(BIN)/python3 action-clock.py --site $(ROOM) --chime chimes

venv: requirements.txt
	[ -d $@ ] || python3 -m venv $@
	ln -sf $@ .venv3
	$(BIN)/pip3 install -U pip
	$(BIN)/pip3 install wheel
	$(BIN)/pip3 install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
	$(BIN)/pip3 install -r $<
	touch $@

clean:
	rm -rf __pycache__

tidy: clean
	rm -rf venv