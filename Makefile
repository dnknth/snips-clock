BIN = $(PWD)/venv/bin

run: venv
	$(BIN)/python3 action-datetime.py -v3

venv: requirements.txt
	[ -d $@ ] || python3 -m venv $@
	$(BIN)/pip3 install -U pip
	$(BIN)/pip3 install wheel
	$(BIN)/pip3 install -r $<
	touch $@

clean:
	rm -rf __pycache__
