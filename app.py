import os
from google.cloud import texttospeech
import streamlit as st

st.set_page_config(
    page_title="My  App",
    page_icon="🎵",
)

google_credentials_path = st.secrets["GOOGLE_APPLICATION_CREDENTIALS_PATH"]

# Set the environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials_path

def synthesize_speech(text,lang='日本語',gender='default'):
    lang_code = {'英語':"en-US",'日本語':'ja-JP'}
    
    gender_type = {'default':'ja-JP-Neural2-C','male':'ja-JP-Neural2-D','female':'ja-JP-Neural2-B'}
    
    gender_type_e = {'default':"en-US-Neural2-A",'male':"en-US-Neural2-D",'female':"en-US-Neural2-E"}

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    if lang_code[lang] == 'ja-JP':
        voice = texttospeech.VoiceSelectionParams(language_code=lang_code[lang],name=gender_type[gender])
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    else:
        voice = texttospeech.VoiceSelectionParams(language_code=lang_code[lang],name=gender_type_e[gender])
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    return response

#--------見た目部分----------------

st.title('音声出力アプリ')
st.markdown('### データ準備')

input_option = st.selectbox('入力データの選択',['直接入力','ファイルアップロード★テキストファイルのみ'])
input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力してください')

else:
    uploaded_file = st.file_uploader('こちらにファイルをアップロードしてください',['txt'])
    if uploaded_file is not None:
        #read()は、バイナリ形式でデータを読み込む。pythonだとopen('file.bin', 'rb') の方。デフォはテキスト
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.markdown('## 入力データ')
    st.code(input_data)
    st.markdown('## パラメータ設定')
    st.subheader('言語と話者の選択')

    lang = st.selectbox('言語を選択して',('日本語','英語'))
    if lang == '日本語':
        gender_type =st.selectbox('性別選択',['default','male','female'])

st.markdown('## 音声生成')
st.write('それでは音声を作りますか？')
if st.button('作成'):
   comment = st.empty()
   comment.write('音声出力を開始')
   response = synthesize_speech(text=input_data,lang=lang,gender=gender_type)
   st.audio(response.audio_content)
   comment.write('完了')