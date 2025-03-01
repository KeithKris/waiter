import ollama

response = ollama.chat(
    model='deepseek-r1',
    messages=[
        {'role': 'user', 'content': ' what is the probability of pulling 4 ace of spades from a deck of cards?'}
    ]
)

# Print the response
print(response['message']['content'])