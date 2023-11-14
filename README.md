Download the checkpoint and store it in `/clap-data` directory (you may need to create this directory in the root of your project folder)

Link https://huggingface.co/lukewys/laion_clap/resolve/main/music_speech_audioset_epoch_15_esc_89.98.pt?download=true

After that:

1. Run `docker-compose up` from the project directory

Notes:

When running the application, you'll see a whole bunch of parameters listed to the the terminal. You'll see that it stops on a `text_branch` like:

`text_branch.encoder.layer.9.output.dense.bias 	 Loaded` (if it's a memory issue I imagine might stop on a different one, but this is where it always stops for me)

It SHOULD continue and finish on `audio_projection.2.bias 	 Loaded`

If you change a letter in the `main.py` file. this will trigger a "fast refresh" and what you'll notice is that the rest of the model is loaded before the full restart of FastAPI happens. 

WHY.

Here's a video showing this problem and how you can recreate: https://streamable.com/2h5dem
