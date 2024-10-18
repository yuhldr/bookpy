'申请github学生包，然后去微软官网申请，可以免费用一年'
# https://learn.microsoft.com/zh-cn/azure/ai-services/speech-service/language-support?tabs=tts
import asyncio

import azure.cognitiveservices.speech as speechsdk


async def tts_main(text, audio_path, conf):
    """_summary_

    Args:
        text (_type_): _description_
        audio_path (_type_): _description_
        conf (_type_): _description_

    Returns:
        _type_: _description_
    """
    speech_config = speechsdk.SpeechConfig(
        subscription=conf["key"], region=conf["region"])
    speech_config.speech_synthesis_language = conf["language"]
    speech_config.speech_synthesis_voice_name = conf["voice"]
    speech_config.speech_synthesis_voice_rate = "50"  # 默认速度为1.0

    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    # result = speech_synthesizer.speak_text_async(text).get()

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

    return result


def download_audio(text, audio_path, conf):
    """下载音频文件

    Args:
        audio_path (str): 保存音频文件的路径
        text (str): 文本
        conf (dict): 配置 conf["tts"]["download"]["azure"]

    Returns:
        str: 保存音频文件的路径
    """

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(tts_main(text, audio_path, conf))
    loop.close()

    return audio_path
