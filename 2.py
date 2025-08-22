from openai import OpenAI

client = OpenAI(
    api_key="ms-f10303bd-329f-40ae-9b12-ed5b233b3d82", # 请替换成您的ModelScope Access Token
    base_url="https://api-inference.modelscope.cn/v1/"
)


response = client.chat.completions.create(
    model="Qwen/Qwen2.5-Coder-32B-Instruct", # ModleScope Model-Id
    messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': '今天天气怎么样？'
        }
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end='', flush=True)