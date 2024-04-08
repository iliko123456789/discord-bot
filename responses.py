import random

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'hey':
        return 'Hey'

    if p_message == 'what is string?':
        return "A string is a sequence of characters, like words or sentences. You can think of it as a piece of text. In programming, a string is used to store and work with text data."
    
    if p_message == 'what is variable?':
        return 'A variable is like a storage box in programming where you can keep information. You can store data, such as numbers or text, in a variable and then use it later in your program.'
    
    if p_message == 'what time is now?':
        return 'i am sorry. i cannot say what time is now next time i will be better'
    
    if p_message == 'who is best programmer?':
        return 'ilia'

    if p_message == 'how are you?':
        return 'I am a bot, so I don\'t have feelings, but thanks for asking! How can I assist you?'

    if p_message == 'roll':
        return str(random.randint(1, 100))

    if p_message == '!help':
        return '`This is a help message that you can modify.`'

    if p_message == 'bye':
        return 'Goodbye! Have a great day!'

    if p_message == 'what is your name?':
        return 'I am a bot, and you can call me Botuniaa.'

    if p_message == 'what can you do?':
        return 'I can perform various tasks such as rolling a dice, providing help, and having a simple chat.'

    if p_message == 'tell me a joke':
        return 'Sure! Here\'s a lovely joke for you: Why don\'t scientists trust atoms? Because they make up everything!'

    if p_message == 'you are amazing':
        return 'Thank you so much! You\'re amazing too!'

    if p_message == 'I love you':
        return 'Aww, that\'s so sweet! I love you too!'
        
    if p_message == 'what is the meaning of life?':
        return 'The meaning of life is subjective and can vary from person to person. It\'s a question that has puzzled humanity for ages.'

    if p_message == 'tell me a fun fact':
        fun_facts = [
            'The average person walks the equivalent of three times around the world in a lifetime.',
            'Cats sleep for about 70% of their lives.',
            'The shortest war in history was between Britain and Zanzibar in 1896. It lasted only 38 minutes.',
            'Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.'
        ]
        return random.choice(fun_facts)

    if p_message == 'what is your favorite color?':
        return 'As a bot, I don\'t have preferences, including favorite colors but astartas fav color is red'

    if p_message == 'tell me a riddle':
        riddles = [
            'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I? (Answer: An echo)',
            'I am taken from a mine, and shut up in a wooden case, from which I am never released, and yet I am used by almost every person. What am I? (Answer: A pencil)',
            'What can you catch but not throw? (Answer: A cold)',
            'What has keys but can\'t open locks? (Answer: A piano)'
        ]
        return random.choice(riddles)

    if p_message == 'tell me a quote':
        quotes = [
            'The only way to do great work is to love what you do. - Steve Jobs',
            'In the midst of difficulty lies opportunity. - Albert Einstein',
            'Believe you can and you\'re halfway there. - Theodore Roosevelt',
            'Don\'t watch the clock; do what it does. Keep going. - Sam Levenson'
        ]
        return random.choice(quotes)

    if p_message == 'what is the meaning of life?':
        return 'The meaning of life is subjective and can vary from person to person. It\'s a question that has puzzled humanity for ages.'
    
    if p_message == 'hi':
        return 'Hi'
    
    if p_message == 'calculatore':
        return
