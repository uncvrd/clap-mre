import laion_clap

def main():
    model = laion_clap.CLAP_Module(enable_fusion=False, amodel='HTSAT-base')
    model.load_ckpt("/clap-data/music_speech_audioset_epoch_15_esc_89.98.pt")

main()