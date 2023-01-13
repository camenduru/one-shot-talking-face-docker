import gradio as gr
import os

block = gr.Blocks()

def calculate():
    os.system(f"python3 -B test_script.py --img_path /content/image.png --audio_path /content/audio.wav --phoneme_path /content/test.json --save_dir /content/train")
    return "done", "/content/train/image_audio.mp4"
    
def run():
    with block:
        btn = gr.Button("Calculate")
        text_out = gr.Textbox(show_label=False)
        video_out = gr.Video(show_label=False)
        btn.click(calculate, outputs=[text_out, video_out])
    block.launch(debug=True)

if __name__ == "__main__":
    run()