# meme-sieve
Filter memes from your photo library.


## Usage


### Development Setup

Install in editable mode using the `Makefile`

```console
$ make install-dev
```

The dev installation will install the program in a virtual environment by default. Activate it as follows.
```console
$ source venv/bin/activate
```

To confirm the installation was successfull, use `which` to reveal the location of the development installation.
```console
$ which memesieve
/home/memeuser/git/hambrosia/meme-sieve/venv/bin/memesieve
```

With the virtual environment activated, you can use the `memesieve` command in any directory for testing.


### Display Help Prompt

```console
$ memesieve --help
usage: memesieve [-h] [-s SOURCE_FOLDER] [-d DELAY] [-e EXTENSIONS [EXTENSIONS ...]] [-m {moondream,gemini}]

Returns a list of filepaths for memes in the specified folder.

options:
  -h, --help            show this help message and exit
  -s SOURCE_FOLDER, --source_folder SOURCE_FOLDER
                        The source folder path containing the files to be checked for memes.
  -d DELAY, --delay DELAY
                        The amount of seconds to wait between each examined file.
  -e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]
                        The extensions to include in the searched files.
  -m {moondream,gemini}, --model {moondream,gemini}
                        The name of the model to use.
```


### Running
Run the program and it will print the names of files in the current folder that it identifies as memes. This simple output is intended to be used as input for other programs, in the spirit of the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy).

```console 
$ memesieve 
beans.jpg
pizza_roll.jpg
simpsons.jpg
cat_comic.png
idgaf.png
```

To move or copy the memes out of the directory, pipe the results to the desired command.


### Copy
To copy the memes to another foloder, use a variation of the following:

```console
$ memesieve | while read filename; do cp "$filename" "../output_folder/$filename"; done
```

### Move
To move the memes to another folder, use something similar to the following:
```console
$ memesieve | while read filename; do mv "$filename" "../output_folder/$filename"; done
```

Always exercise caution, since the program can sometimes misidentify photos as memes, especially if they are humorous or contain meme-like text.

### Model Selection

The tool supports multiple models to detect memes. By default, the program uses the [Moondream](https://github.com/vikhyat/moondream) package, a small vision language model that runs locally and can use either CPU or GPU.

To use another model, select it by name.

```console
$ memesieve -m gemini
porkchop.jpg
bezos.png
ham_salad.jpg
```


### API Setup
If you select the Gemini model, you will need to set the Google API key environment variable. To get a new API key, visit [Google AI Studio](https://aistudio.google.com/app/apikey). When testing the tool, it is recommended to make a new token in the unpaid free tier to avoid any costs. The user is responsible for any costs incurred for Google API usage.

```console
$ export GOOGLE_API_KEY="gabagool"
```


### Setting the delay

Some models may benefit from a longer delay between calls, others may be need a shorter delay. When using Google's Gemini Flash, for example, the free-tier has a limit of 15 requests per minute. By default the program will use a delay deemed appropriate for the model. You can override the delay using the `-d` flag specifying an integer value in seconds.

```console
$ memesieve -d 2
beans.jpg
pizza_roll.jpg
simpsons.jpg
cat_comic.png
idgaf.png
```
