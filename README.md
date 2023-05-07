# My personal assistant

## Welcome to this project

This project surpasses the length constraints of using OpenAI Chat-LLMs, such as ChatGPT, enabling you to converse with
any long document. It expedites comprehension of the content and facilitates the acquisition of valuable insights.
Compared with ChatPDF, it accommodates various file formats, including PDF, doc, docx, txt, web URLs, and audio.
The implementation of this project is straightforward to follow, expand, and efficient for integration into other
applications.

Based on https://github.com/webpilot-ai/ChatLongDoc

## Dependencies

Please execute the following command in the terminal to install the required dependencies:

Python>=3.8

```shell
cd ChatLongDoc
pip install -r requirements.txt
```

## Usage

### Local files

Remember to replace path to your file :)

```shell
export OPEN_API_TOKEN=YOUR_TOKEN
python3 ./main.py /Users/awesome/testing.pdf
```

```shell
brew install ffmpeg
export OPEN_API_TOKEN=YOUR_TOKEN
python3 ./main.py /Users/awesome/audio.mp3
```

### Web URLs

```shell
export OPEN_API_TOKEN=YOUR_TOKEN
python3 ./main.py https://www.mattprd.com/p/the-complete-beginners-guide-to-autonomous-agents
```