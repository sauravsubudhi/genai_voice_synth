import openai
import os
import re
# #------------------------------------------------------------------------
openai.api_type = "azure"
openai.api_base = "https://rt-internal.openai.azure.com/"
openai.api_version = "2023-06-01-preview"
openai.api_key = "aa438d7cb1d94ef4bd01e1336d939614"
os.environ["OPENAI_API_KEY"] = openai.api_key
#-------------------------------------------------------------------------
def enhance_text(input_text):
    prompt = [
        {"role": "user", "content": f"Enhance the following text: {input_text}"}
    ]
    response = openai.ChatCompletion.create(
        engine="gpt-4-32k",
        messages=prompt
    )
    try:
        enhanced_text = response['choices'][0]['message']['content'].strip()
    except:
        enhanced_text = input_text
    return enhanced_text
#----------------------------------------------------------------------------
def convert_to_minutes_seconds(hours, minutes, seconds):
    total_minutes = hours * 60 + minutes
    total_seconds = total_minutes * 60 + seconds
    total_minutes = str(total_minutes)
    if len(total_minutes) < 2:
        total_minutes = "0"+ total_minutes
    total_seconds = str(total_seconds)
    if len(total_seconds)<2:
        total_seconds = total_seconds+".000"
    else:
         total_seconds = total_seconds+".000"
    return total_minutes+":"+total_seconds
# #----------------------------------------------------------------------------
def convert_string_to_tuple(time_duration):
    print(time_duration[0].split(':')[0])
    hours = int(float(time_duration[0].split(':')[0]))
    minutes = int(float(time_duration[0].split(':')[1]))
    total_seconds = int(float(time_duration[0].split(':')[2]))
    start_time = convert_to_minutes_seconds(hours, minutes, total_seconds)
    hours = int(float(time_duration[1].split(':')[0]))
    minutes = int(float(time_duration[1].split(':')[1]))
    total_seconds = int(float(time_duration[1].split(':')[2]))
    end_time = convert_to_minutes_seconds(hours, minutes, total_seconds)
    return start_time,end_time

# #-----------------------------------------------------------------------------
def get_splitted_text(transcript, start_time, end_time):
    splitted_text = []
    timestamp_pattern = re.compile(r'\[(\d+:\d+\.\d+) --> (\d+:\d+\.\d+)\]')
    for line in transcript:
        match = timestamp_pattern.search(line)
        if match:
            start_timestamp, end_timestamp = match.groups()
            if start_time <= start_timestamp <= end_time or start_time <= end_timestamp <= end_time:
                text = line.split("]", 1)[1].strip()
                splitted_text.append(text)
    return splitted_text
def final(time_range_list,transcript):
    print(time_range_list)
    print(transcript)
    final_enhanced_list = []
    for time_range in time_range_list:
        start_time,end_time = convert_string_to_tuple(time_range)
        #print(start_time,end_time)
        splitted_text = get_splitted_text(transcript, start_time, end_time)
        splitted_text_1 = ''.join(splitted_text)
        enhanced_text = enhance_text(splitted_text_1)
        final_enhanced_list.append(enhanced_text)
    return final_enhanced_list
#
#input_timestamps = [('00:00:00', '00:00:20'),('00:00:21','00:00:31')]
#
#transcript = ['[00:00.000 --> 00:15.600]  So, thanks everyone for joining. So, today, you know, we are going to showcase our RANOMAL',                '[00:15.600 --> 00:20.440]  and its features and capabilities. We are going to discuss about the features and capabilities',                '[00:20.440 --> 00:31.000]  and quick demo on how RANOMAL works, basically. So, what is RANOMAL is solving in the current', '[00:31.000 --> 00:38.400]  industry, basically? So, with our defining, you know, clients, how do we solve ML of platforms', '[00:38.400 --> 00:45.000]  you know, in terms of the deployments and monitoring and visibility, right? So, how do we']
#
# # transcript = [
# #     '"[00:00.000 --> 00:15.600]  So, thanks everyone for joining. So, today, you know, we are going to showcase our RANOMAL"',
# # '"[00:15.600 --> 00:20.440]  and its features and capabilities. We are going to discuss about the features and capabilities"',
# # '"[00:20.440 --> 00:31.000]  and quick demo on how RANOMAL works, basically. So, what is RANOMAL is solving in the current"',
# # '"[00:31.000 --> 00:38.400]  industry, basically? So, with our defining, you know, clients, how do we solve ML of platforms"',
# # '"[00:38.400 --> 00:45.000]  you know, in terms of the deployments and monitoring and visibility, right? So, how do we"'
# #]
#
#print(final(input_timestamps,transcript))

