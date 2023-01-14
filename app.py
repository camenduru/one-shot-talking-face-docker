import gradio as gr
import os, subprocess, torchaudio
from PIL import Image

block = gr.Blocks()

def calculate(image_in, audio_in):
    waveform, sample_rate = torchaudio.load(audio_in)
    torchaudio.save("/content/audio.wav", waveform, sample_rate, encoding="PCM_S", bits_per_sample=16)
    image = Image.open(image_in)
    image.save("image.png")

    pocketsphinx_run = subprocess.run(['pocketsphinx', '-phone_align', 'yes', 'single', '/content/audio.wav'], check=True, capture_output=True)
    jq_run = subprocess.run(['jq', '[.w[]|{word: (.t | ascii_upcase | sub("<S>"; "sil") | sub("<SIL>"; "sil") | sub("\\\(2\\\)"; "") | sub("\\\(3\\\)"; "") | sub("\\\(4\\\)"; "") | sub("\\\[SPEECH\\\]"; "SIL") | sub("\\\[NOISE\\\]"; "SIL")), phones: [.w[]|{ph: .t | sub("\\\+SPN\\\+"; "SIL") | sub("\\\+NSN\\\+"; "SIL"), bg: (.b*100)|floor, ed: (.b*100+.d*100)|floor}]}]'], input=pocketsphinx_run.stdout, capture_output=True)
    with open("test.json", "w") as f:
        f.write(jq_run.stdout.decode('utf-8').strip())

    os.system(f"cd /content/one-shot-talking-face && python3 -B test_script.py --img_path /content/image.png --audio_path /content/audio.wav --phoneme_path /content/test.json --save_dir /content/train")
    return "/content/train/image_audio.mp4"
    
def run():
  with block:
    with gr.Group():
      with gr.Box():
        with gr.Row().style(equal_height=True):
          image_in = gr.Image(show_label=False, type="filepath")
          audio_in = gr.Audio(show_label=False, type='filepath')
          video_out = gr.Video(show_label=False)
        with gr.Row().style(equal_height=True):
          btn = gr.Button("Calculate")          
    btn.click(calculate, inputs=[image_in, audio_in], outputs=[video_out])
    block.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    run()
