'申请github学生包，然后去微软官网申请，可以免费用一年'
# https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts

import azure.cognitiveservices.speech as speechsdk


async def download_audio(text, audio_path, conf):
    """_summary_

    Args:
        text (_type_): _description_
        audio_path (_type_): _description_
        conf (_type_): _description_

    Returns:
        _type_: _description_
    """

    if len(conf["key"]) == 0:
        print("请在配置文件中填写Azure的key")
        return "请在配置文件中填写Azure的key"

    speech_config = speechsdk.SpeechConfig(
        subscription=conf["key"], region=conf["region"])

    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    # 使用SSML设置语音速度
    ssml_text = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
           xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="{conf['language']}">
        <voice name="{conf['voice']}">
            <prosody rate="{conf['rate']}">
                {text}
            </prosody>
        </voice>
    </speak>
    """
    result = speech_synthesizer.speak_ssml_async(ssml_text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesis failed: {result.reason}")
