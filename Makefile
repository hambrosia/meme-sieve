.PHONY: install-dev clean

install-dev:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -e .

clean:
	rm -rf venv meme_sieve/meme_sieve.egg-info meme_sieve/__pycache__
	find -iname "*.pyc" -delete
