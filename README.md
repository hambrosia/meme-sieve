# meme-sieve
Filter memes from your photo library.


## Usage


### API Setup
Set the Google API Key environment variable.
```shell
$ export GOOGLE_API_KEY="gabagool"
```


### Running
Run the program and it will print the names of files in the current folder that it identifies as memes.

```shell 
$ ../main.py 
beans.jpg
pizza_roll.jpg
simpsons.jpg
cat_comic.png
idgaf.png
```

To move or copy the memes out of the directory, pipe the results to the desired command.


### Copy
To copy the memes to another foloder, use the following:

```shell
./main.py | while read filename; do cp "$filename" "../output_folder/$filename"; done
```


### Move
To move the memes to another folder, use the following:
```shell
./main.py | while read filename; do cp "$filename" "../output_folder/$filename"; done
```

Always exercise caution, as the program can sometimes misidentify photos as memes, especially if they are humorous or contain meme-like text.


### Setting the delay

The model used is Google's Gemini Flash, which has a free-tier limit of 15 requests per minute. By default, the program will use a delay of four seconds to keep usage within the free tier. If you have a paid token, you can decrease the limit using the `-d` flag.

```shell
$ ./main.py -d 2
beans.jpg
pizza_roll.jpg
simpsons.jpg
cat_comic.png
idgaf.png
```
