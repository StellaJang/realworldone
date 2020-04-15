def sent_analysis(text : str) -> str:

    from ibm_watson import ToneAnalyzerV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    import json
    import re

    authenticator = IAMAuthenticator('dpzKQbDVq8kXiNnUOTlmGd-rDMvYt8WfumDNTQsnQ-FW')
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url('https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/35e62421-4af9-419e-9d5f-54f04d007614')

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='text/plain'
    ).get_result()

    analysis = json.dumps(tone_analysis, indent=2)

    #extract the emotions and put them into variables
    analytical = re.search("analytical", analysis)
    sadness = re.search("sadness", analysis)
    anger = re.search("anger", analysis)
    fear = re.search("fear", analysis)
    joy = re.search("joy", analysis)
    confident = re.search("confident", analysis)
    tentative = re.search("tentative", analysis)

    emotions = [analytical, sadness, anger, fear, joy, confident, tentative]   #put the emotions into a list
    emotions = list(dict.fromkeys(emotions)) #remove duplicates

    #remove Nonetypes as to avoid problems with iteration
    for emotion in emotions:
        if emotion is None:
            emotions.remove(None)

    #remove similar emotions as only 3 categories of emotions are needed
    if analytical in emotions and tentative in emotions:
        emotions.remove(analytical)
    if sadness in emotions and anger in emotions and fear in emotions:
        emotions.remove(anger)
        emotions.remove(fear)
    if sadness in emotions and anger in emotions:
        emotions.remove(anger)
    if sadness in emotions and fear in emotions:
        emotions.remove(fear)
    if joy in emotions and confident in emotions:
        emotions.remove(confident)

    if not emotions:
        return text + " :|"
    if emotions:
        for emotion in emotions:
            if "joy" in emotion.string or "confident" in emotion.string:
                return text + " :)"
            elif "sadness" in emotion.string or "anger" in emotion.string or "fear" in emotion.string:
                return text + " :("
            else:
                return text + " :|"



